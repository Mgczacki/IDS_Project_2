import pandas as pd
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt


movies = pd.read_csv("../movieReplicationSet.csv")

shrek_on_gender = movies[["Shrek (2001)", "Gender identity (1 = female; 2 = male; 3 = self-described)"]]
shrek_on_gender = shrek_on_gender[shrek_on_gender["Gender identity (1 = female; 2 = male; 3 = self-described)"] != 3]
genderCount = shrek_on_gender["Gender identity (1 = female; 2 = male; 3 = self-described)"].value_counts()
ShrekMaleRatings = shrek_on_gender[shrek_on_gender["Gender identity (1 = female; 2 = male; 3 = "
                                                   "self-described)"] == 2]
MalesNotShrek = ShrekMaleRatings["Shrek (2001)"].isna().sum()

ShrekFemaleRatings = shrek_on_gender[shrek_on_gender["Gender identity (1 = female; 2 = male; 3 = "
                                                     "self-described)"] == 1]
FemalesNotShrek = ShrekFemaleRatings["Shrek (2001)"].isna().sum()

ShrekMaleRatings = (ShrekMaleRatings.drop(columns="Gender identity (1 = female; 2 = male; 3 = self-described)")
                    .dropna().reset_index(drop=True))
ShrekFemaleRatings = (ShrekFemaleRatings.drop(columns="Gender identity (1 = female; 2 = male; 3 = self-described)")
                      .dropna().reset_index(drop=True))

testResults = mannwhitneyu(ShrekFemaleRatings, ShrekMaleRatings)
ShrekFemaleRatingsPdf = ShrekFemaleRatings["Shrek (2001)"].value_counts(normalize=True).sort_index()
ShrekMaleRatingsPdf = ShrekMaleRatings["Shrek (2001)"].value_counts(normalize=True).sort_index()
fig, axs = plt.subplots(1, 2)
fig.suptitle("Normalized Histograms of the Male & Female Ratings Distribution (For Shrek (2001))")
axs[0].bar(ShrekMaleRatingsPdf.index, ShrekMaleRatingsPdf, color="lightblue", alpha=0.6, width=0.5)
axs[0].set_title("Males")
axs[0].set_xlabel("Ratings")
axs[0].set_ylabel("Probability")
axs[1].bar(ShrekFemaleRatingsPdf.index, ShrekFemaleRatingsPdf, color="lightgreen", alpha=0.6, align="center", width=0.5)
axs[1].set_title("Females")
axs[1].set_xlabel("Ratings")
axs[1].set_ylabel("Probability")

print(-1)
