import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt


def preprocessing(moviedf):
    movie_on_gender = moviedf[moviedf["Gender identity (1 = female; 2 = male; 3 = self-described)"] != 3]  # remove
    # self-described individuals
    MovieMaleRatings = movie_on_gender[movie_on_gender["Gender identity (1 = female; 2 = male; 3 = "
                                                       "self-described)"] == 2]
    MovieFemaleRatings = movie_on_gender[movie_on_gender["Gender identity (1 = female; 2 = male; 3 = "
                                                         "self-described)"] == 1]
    didNotWatchFemale = didNotWatchCount(MovieFemaleRatings, "Females")
    didNotWatchMale = didNotWatchCount(MovieMaleRatings, "Males")
    didNotWatchList = [didNotWatchMale, didNotWatchFemale]
    MovieMaleRatings = (MovieMaleRatings.drop(columns="Gender identity (1 = female; 2 = male; 3 = self-described)")
                        .dropna())
    MovieFemaleRatings = (MovieFemaleRatings.drop(columns="Gender identity (1 = female; 2 = male; 3 = self-described)")
                          .dropna())
    return MovieFemaleRatings, MovieMaleRatings, didNotWatchList


def didNotWatchCount(genderSeries, genderCode):
    print(f"{genderCode} who did not see movie: {genderSeries.isna().sum()[1]}")
    didNotWatch = genderSeries.isna().sum()[1]
    return didNotWatch


def genderBreakdown(moviedf):
    genderCount = moviedf["Gender identity (1 = female; 2 = male; 3 = self-described)"].value_counts()
    print(f"Males: {genderCount[2]}\nFemales: {genderCount[1]}\nSelf-described: {genderCount[3]}")
    return genderCount


columns_to_use = np.append(np.arange(0, 400), 474)
movies = pd.read_csv("../movieReplicationSet.csv", usecols=columns_to_use)
genderNum = genderBreakdown(movies)
moviesRateDiffGender = []
didNotWatchGender = []
pvalues = []
for movie in range(len(columns_to_use) - 1):
    movieData = movies[["Gender identity (1 = female; 2 = male; 3 = self-described)", movies.columns[movie]]]
    maleRatings, femaleRatings, genderDidNotWatch = preprocessing(movieData)
    testResults = mannwhitneyu(femaleRatings, maleRatings)
    pvalue = testResults[1][0]
    if pvalue < 0.005:
        print(f"Male and Female ratings for {movies.columns[movie]} differ significantly.\n")
        moviesRateDiffGender.append(movies.columns[movie])
        didNotWatchGender.extend(genderDidNotWatch)
        pvalues.append(pvalue)
    else:
        continue

print(f"{len(moviesRateDiffGender)} movies out of 400 in the set are rated differently by male and female viewers.\n")
iterables = [moviesRateDiffGender, ["Male", "Female"]]
multiIndex = pd.MultiIndex.from_product(iterables, names=["Movies", "Gender"])
multDf = pd.DataFrame(didNotWatchGender, index=multiIndex, columns=["Did Not Watch"])
multDf.to_csv("genderPropQ4.csv")
print(-1)
