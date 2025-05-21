import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

def CalculateCorrelation(Rankings_df: pd.DataFrame, Method, Path, Name):
    correlation_matrix = Rankings_df.corr(method=Method)

    print(Method+'\'s correlation coefficient matrix:')
    print(correlation_matrix)
    print('-' * 58)

    # Save the DataFrame to a text file
    correlation_matrix.to_csv(directory + '/' + Name + '.csv', sep=';', index=True)

    return correlation_matrix

def Create_Heatmap(DataFrameMatrix: pd.DataFrame, Method, Path, name, Cmap):
    g = sns.clustermap(DataFrameMatrix, annot=True, fmt='.2f', method="single", dendrogram_ratio=0.15, figsize=(8, 8), row_cluster=True, col_cluster=True, cmap = Cmap, vmin = 0, vmax = 1)

    # Center the y-axis labels
    g.ax_heatmap.yaxis.set_ticks_position("left")

    # Hide the row and column dendrograms
    g.ax_row_dendrogram.set_visible(False)
    g.ax_col_dendrogram.set_visible(False)

    # Move the colorbar to the left
    g.ax_cbar.set_position((0.02, 0.2, 0.03, 0.4))
    g.fig.suptitle("Heatmap of the " + Method + "'s correlation coefficient for the " + name)

    plt.savefig(Path + "/Heatmap_"+name+".png")
    plt.clf()
    plt.close()

    print("Created heatmap: " + Method+"_Heatmap for the " + name)
    print('-' * 58)

directory = './Results'
if not os.path.exists(directory):
    os.makedirs(directory)

#Load all ranking results from all five MCDM methods
# Before this step it is necessary to rank same dataset using DEX and other four MCDM methods
ranking_files = {
    'DEX': 'DEX_Results.csv',
    'AHP': 'AHP_Results.csv',
    'TOPSIS': 'TOPSIS_Results.csv',
    'PROMETHEE': 'PROMETHEE_Results.csv',
    'PAPRIKA': 'PAPRIKA_Results.csv'
}

ranking_dfs = {}

for method, filename in ranking_files.items():
    df = pd.read_csv(directory + '/' + filename, index_col=0, delimiter=';')
    ranking_dfs[method] = df
    print(f'{method} Ranking results:')
    print(df)
    print('-' * 58)

#Combine rankings dataframes into one dataframe for correlation coefficients
MCDMRankings_df = pd.concat(
    [df[method] for method, df in ranking_dfs.items()],
    axis=1)

#Print combined rankings
print('Complete ranking results:')
print(MCDMRankings_df)
print('-' * 58)

# Save the DataFrame to a text file
MCDMRankings_df.to_csv(directory + '/CompleteRankings.csv', sep=';', index=True)

#Calculate the ranking coefficients
Pearson_df = CalculateCorrelation(MCDMRankings_df, "pearson", directory, "Pearson_MCDMRankings")
Spearman_df = CalculateCorrelation(MCDMRankings_df, "spearman", directory, "Spearman_MCDMRankings")
Kendall_df = CalculateCorrelation(MCDMRankings_df, "kendall", directory, "Kendall_MCDMRankings")

#Create heatmaps
Create_Heatmap(Pearson_df, "Pearson", directory, "Pearson_MCDMRankings", "coolwarm")
Create_Heatmap(Spearman_df, "Spearman", directory, "Spearman_MCDMRankings", "coolwarm")
Create_Heatmap(Kendall_df, "Kendall", directory, "Kendall_MCDMRankings", "coolwarm")