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
    index_labels = ['DEX', 'AHP', 'TOPSIS', 'PROMETHEE', 'PAPRIKA']

    df = pd.DataFrame(DataFrameMatrix, index=index_labels)

    sorted_indices = df.mean(axis=1).sort_values().index
    df_sorted_auto = df.loc[sorted_indices, sorted_indices]

    plt.figure(figsize=(8, 7))
    ax = sns.heatmap(df_sorted_auto,
                     cmap=Cmap,
                     annot=True,
                     fmt=".2f",
                     linewidths=.5,
                     vmin=0,
                     vmax=1,
                     annot_kws={"size": 18})

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=14)

    ax.tick_params(axis='x', labelsize=14)  # fontsize za X os
    ax.tick_params(axis='y', labelsize=14)  # fontsize za Y os

    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(Path + "/Heatmap_"+name+".png")
    plt.clf()
    plt.close()

def Create_ScatterPlots(Kendall_df: pd.DataFrame, Spearman_df: pd.DataFrame, Pearson_df: pd.DataFrame, directory):
    kendall = Kendall_df.loc['DEX'].drop('DEX')
    spearman = Spearman_df.loc['DEX'].drop('DEX')
    pearson = Pearson_df.loc['DEX'].drop('DEX')

    df = pd.DataFrame({
        "Kendall's Tau": kendall,
        "Spearman's Rho": spearman,
        "Pearson's R": pearson,
        "Method": kendall.index
    })

    # Pairwise scatter plot of correlation metrics
    sns.pairplot(df, vars=["Kendall's Tau", "Spearman's Rho", "Pearson's R"], diag_kind="auto")
    plt.suptitle("Pairwise Scatter Plot of Correlations", y=1.02)
    plt.savefig(directory + "/Pairwise_Scatter_DEX_Methods.png")
    plt.clf()
    plt.close()

    # Line plot
    plt.plot(["AHP", "TOPSIS", "PROMETHEE", "PAPRIKA"], df["Kendall's Tau"], label="Kendall's Tau")
    plt.plot(["AHP", "TOPSIS", "PROMETHEE", "PAPRIKA"], df["Spearman's Rho"], label="Spearman's Rho")
    plt.plot(["AHP", "TOPSIS", "PROMETHEE", "PAPRIKA"], df["Pearson's R"], label="Pearson's R")
    plt.legend()
    plt.title("Comparison of Correlation Metrics between DEX and other methods")
    plt.savefig(directory + "/Comparison_DEX_Methods.png")
    plt.clf()
    plt.close()

    # Bar plot for correlations
    df.plot(kind="bar", figsize=(10, 6), alpha=0.8)
    plt.title("Correlation metrics between DEX and MCDM methods")
    plt.ylabel("Correlation Coefficient")
    plt.xlabel("MCDM methods")
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)  # Reference line for zero
    plt.legend(title="Metrics", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(directory + "/Bar_Plot_DEX_Methods.png")
    plt.clf()
    plt.close()


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

#Create scatter line plot to display correlation metrics between DEX and other MCDM methods
# Create_ScatterPlots(Kendall_df, Spearman_df, Pearson_df, directory)