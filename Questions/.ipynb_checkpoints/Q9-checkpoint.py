import pandas as pd
from scipy.stats import ks_2samp
import matplotlib.pyplot as plt


movies = pd.read_csv("../movieReplicationSet.csv", usecols=["Home Alone (1990)", "Finding Nemo (2003)"])
homeAlone = movies["Home Alone (1990)"].dropna()
findingNemo = movies["Finding Nemo (2003)"].dropna()
homeAlonePdf = homeAlone.value_counts(normalize=True).sort_index()
findingNemoPdf = findingNemo.value_counts(normalize=True).sort_index()

# Plotting probability densities side by side
fig, axs = plt.subplots(1, 2)
fig.suptitle("Normalized histograms For Home Alone and Finding Nemo")
axs[0].bar(homeAlonePdf.index, homeAlonePdf, color="lightblue", alpha=0.6, width=0.5)
axs[0].set_title("Home Alone")
axs[1].bar(findingNemoPdf.index, findingNemoPdf, color="lightgreen", alpha=0.6, width=0.5)
axs[1].set_title("Finding Nemo")
test = ks_2samp(homeAlone, findingNemo)
print(-1)