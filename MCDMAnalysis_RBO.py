import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from rbo import RankingSimilarity
from scipy.stats import rankdata

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
    plt.savefig(Path + "/Heatmap_" + name + ".png")
    plt.clf()
    plt.close()

    print("Created heatmap: " + Method+"_Heatmap for the " + name)
    print("----------------------------------------------------------")

def Create_Bargraph(DataFrameMatrix: pd.DataFrame, Name, Path):
    methods = ['DEX', 'AHP', 'TOPSIS', 'PROMETHEE', 'PAPRIKA']
    rbo_scores = [0.81052, 0.80025, 0.85504, 0.93973, 0.93857]

    # Plot
    plt.figure(figsize=(8, 5))
    plt.bar(methods, rbo_scores, color='skyblue')

    # Add titles and labels
    plt.title('RBO score between overall ranking and MCDM Methods', fontsize=14)
    plt.xlabel('MCDM Methods', fontsize=12)
    plt.ylabel('RBO Score', fontsize=12)

    # Display the plot
    #plt.show()

    plt.savefig(Path + "/" + Name + ".png")
    plt.clf()
    plt.close()

directory = './Results'
if not os.path.exists(directory):
    os.makedirs(directory)

#Load all ranking results from all five MCDM methods
DEXRanking = 'DEX_Results.csv'
AHPRanking = 'AHP_Results.csv'
TOPSISRanking = 'TOPSIS_Results.csv'
PROMETHEERanking = 'PROMETHEE_Results.csv'
PAPRIKARanking = 'PAPRIKA_Results.csv'

DEXRanking_df = pd.read_csv('./Results/' + DEXRanking, index_col=0, delimiter=';').reset_index(drop=True)
AHPRanking_df = pd.read_csv('./Results/' + AHPRanking, index_col=0, delimiter=';').reset_index(drop=True)
TOPSISRanking_df = pd.read_csv('./Results/' + TOPSISRanking, index_col=0, delimiter=';').reset_index(drop=True)
PROMETHEERanking_df = pd.read_csv('./Results/' + PROMETHEERanking, index_col=0, delimiter=';').reset_index(drop=True)
PAPRIKARanking_df = pd.read_csv('./Results/' + PAPRIKARanking, index_col=0, delimiter=';').reset_index(drop=True)

# Sort and export DataFrame to a csv file
DEXRankingScores_desc = DEXRanking_df.sort_values(by='DEX', ascending=False)
AHPRanking_desc = AHPRanking_df.sort_values(by='AHP', ascending=False)
TOPSISRanking_desc = TOPSISRanking_df.sort_values(by='TOPSIS', ascending=False)
PROMETHEERanking_desc = PROMETHEERanking_df.sort_values(by='PROMETHEE', ascending=False)
PAPRIKARanking_desc = PAPRIKARanking_df.sort_values(by='PAPRIKA', ascending=False)

# Dodavanje stupca s rangom
DEXRankingScores_desc['Rang'] = range(1, len(DEXRankingScores_desc) + 1)
AHPRanking_desc['Rang'] = range(1, len(AHPRanking_desc) + 1)
TOPSISRanking_desc['Rang'] = range(1, len(TOPSISRanking_desc) + 1)
PROMETHEERanking_desc['Rang'] = range(1, len(PROMETHEERanking_desc) + 1)
PAPRIKARanking_desc['Rang'] = range(1, len(PAPRIKARanking_desc) + 1)

#Print loaded and sorted rankings dataframes
print('DEX Ranking results:')
print(DEXRankingScores_desc)
print("----------------------------------------------------------")

print('AHP Ranking results:')
print(AHPRanking_desc)
print("----------------------------------------------------------")

print('TOPSIS Ranking results:')
print(TOPSISRanking_desc)
print("----------------------------------------------------------")

print('PROMETHEE Ranking results:')
print(PROMETHEERanking_desc)
print("----------------------------------------------------------")

print('PAPRIKA Ranking results:')
print(PAPRIKARanking_desc)
print("----------------------------------------------------------")

#Import ranking dataframes into lists
DEXRankingScores_list = DEXRankingScores_desc.index.tolist()
AHPRankingScores_list = AHPRanking_desc.index.tolist()
TOPSISRankingScores_list = TOPSISRanking_desc.index.tolist()
PROMETHEERankingScores_list = PROMETHEERanking_desc.index.tolist()
PAPRIKARankingScores_list = PAPRIKARanking_desc.index.tolist()

# Initialize an empty list to store rankings
ranked_lists = []

# Add each ranking list to the main list
ranked_lists.append(DEXRankingScores_list)
ranked_lists.append(AHPRankingScores_list)
ranked_lists.append(TOPSISRankingScores_list)
ranked_lists.append(PROMETHEERankingScores_list)
ranked_lists.append(PAPRIKARankingScores_list)

method_names = ["DEX", "AHP", "TOPSIS", "PROMETHEE", "PAPRIKA"]

#RBO
# Initialize an empty list to store RBO similarities
rbo_similarities = []

# Loop through each pair of rankings to calculate RBO
rbo_matrix = pd.DataFrame(np.ones((len(method_names), len(method_names))),
                          index=method_names, columns=method_names)

for i in range(len(ranked_lists)):
    for j in range(i + 1, len(ranked_lists)):
        ranking_1 = ranked_lists[i]
        ranking_2 = ranked_lists[j]

        rbo = RankingSimilarity(ranking_1, ranking_2)
        similarity = rbo.rbo(p=0.99)

        # Spremi u listu za ispis
        rbo_similarities.append((f'{method_names[i]} vs {method_names[j]}', similarity))

        # Upis u matricu na odgovarajuća mjesta (simetrična matrica)
        rbo_matrix.iloc[i, j] = similarity
        rbo_matrix.iloc[j, i] = similarity

# Ispiši rezultate
for pair, similarity in rbo_similarities:
    print(f'RBO similarity between {pair}: {similarity:.4f}')

rbo_matrix.to_csv(directory + '/RBO MCDM comparison.csv')

#Create heatmap for RBO between methods
Create_Heatmap(rbo_matrix, "RBO between each pair of the MCDM methods", directory, "RBO_MCDMComparison", "Blues")

#Calculate the rank aggregation using ScyPy
# Sort values by alternative ID
DEX_sorted = DEXRankingScores_desc.sort_index()
AHP_sorted = AHPRanking_desc.sort_index()
TOPSIS_sorted = TOPSISRanking_desc.sort_index()
PROMETHEE_sorted = PROMETHEERanking_desc.sort_index()
PAPRIKA_sorted = PAPRIKARanking_desc.sort_index()

#Import ranking dataframes into lists
DEX_list = DEX_sorted['Rang'].tolist()
AHP_list = AHP_sorted['Rang'].tolist()
TOPSIS_list = TOPSIS_sorted['Rang'].tolist()
PROMETHEE_list = PROMETHEE_sorted['Rang'].tolist()
PAPRIKA_list = PAPRIKA_sorted['Rang'].tolist()

# Create a DataFrame
RankPlaces_df = pd.DataFrame({
    'DEX': DEX_list,
    'AHP': AHP_list,
    'TOPSIS': TOPSIS_list,
    'PROMETHEE': PROMETHEE_list,
    'PAPRIKA': PAPRIKA_list
})

RankPlaces_df.to_csv(directory + '/RankPlaces.csv', sep=';', index=True)

print("RankPlaces_df DataFrame:")
print(RankPlaces_df)
print("----------------------------------------------------------")

aggregatedScyPy = rankdata([sum(r) for r in zip(DEX_list, AHP_list, TOPSIS_list, PROMETHEE_list, PAPRIKA_list)])

aggregatedScyPy_df = pd.DataFrame(aggregatedScyPy)
aggregatedScyPy_df.columns = ['AggregatedRank']
aggregatedScyPy_desc = aggregatedScyPy_df.sort_values(by='AggregatedRank', ascending=True)

print('Aggregated ScyPy ranking:')
print(aggregatedScyPy_desc)
print("----------------------------------------------------------")

aggregatedScyPy_desc.to_csv(directory + '/AggregatedRank.csv', sep=';', index=True)

# Compare each list to the aggregated rank
methods = ['DEX', 'AHP', 'TOPSIS', 'PROMETHEE', 'PAPRIKA']
aggregatedScyPy_list = aggregatedScyPy_desc.index.tolist()

# Izračun RBO sličnosti
rbo_values = [RankingSimilarity(aggregatedScyPy_list, ranked_list).rbo() for ranked_list in ranked_lists]

# Kreiranje DataFrame-a
df_rbo = pd.DataFrame(rbo_values, index=methods, columns=['RBO'])

# Prikaz DataFrame-a
print(df_rbo)

df_rbo.to_csv(directory + '/RBO Overall.csv', sep=';', index=True)

#Create overall bargraph
Create_Bargraph(df_rbo, "RBO Overall", directory)
