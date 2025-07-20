import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

def Create_ScatterPlots(MCDMRankings_df, directory, sample_size=1000):
    if len(MCDMRankings_df) > sample_size:
        MCDMRankings_df = MCDMRankings_df.sample(n=sample_size, random_state=42)

    sns.set(style='darkgrid', palette='viridis')
    plt.figure(figsize=(8, 6))

    g = sns.pairplot(MCDMRankings_df, plot_kws={"alpha": 0.6, "s": 10})
    plt.tight_layout()
    g.savefig(f"{directory}/MCDMScatterPlot.png")
    plt.clf()
    plt.close()

#Load all ranking results from all five MCDM methods
# Before this step it is necessary to rank same dataset using DEX and other four MCDM methods
directory = './Results'
if not os.path.exists(directory):
    os.makedirs(directory)

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
    ranking_dfs[method]['Ranking Place'] = ranking_dfs[method][method].rank(ascending=False, method='min').astype(int)

    print(f'{method} Ranking results:')
    print(df)
    print('-' * 58)

dataframes_to_concat = [df[f'Ranking Place'].rename(method) for method, df in ranking_dfs.items()]
MCDMRankings_df = pd.concat(dataframes_to_concat, axis=1, join='outer')

#Print combined rankings
print('Complete ranking results:')
print(MCDMRankings_df)
print('-' * 58)

# Save the DataFrame to a text file
MCDMRankings_df.to_csv(directory + '/CompleteRankingScatter.csv', sep=';', index=True)

Create_ScatterPlots(MCDMRankings_df, directory)