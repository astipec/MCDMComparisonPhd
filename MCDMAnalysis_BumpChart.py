import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

#def CreateBumpChart(DEX_df, AHP_df, TOPSIS_df, PROMETHEE_df, PAPRIKA_df: pd.DataFrame, path, name, count, size):
def CreateBumpChart(DEX_df, AHP_df, TOPSIS_df, PROMETHEE_df, PAPRIKA_df):
    DEXRankingScores_desc = DEX_df.sort_values(by='DEX', ascending=False)
    AHPRankingScores_desc = AHP_df.sort_values(by='AHP', ascending=False)
    TOPSISRankingScores_desc = TOPSIS_df.sort_values(by='TOPSIS', ascending=False)
    PROMETHEERankingScores_desc = PROMETHEE_df.sort_values(by='PROMETHEE', ascending=False)
    PAPRIKARankingScores_desc = PAPRIKA_df.sort_values(by='PAPRIKA', ascending=False)

    DEXRankingScores_desc['DEXRang'] = range(1, len(DEXRankingScores_desc) + 1)
    AHPRankingScores_desc['AHPRang'] = range(1, len(AHPRankingScores_desc) + 1)
    TOPSISRankingScores_desc['TOPSISRang'] = range(1, len(TOPSISRankingScores_desc) + 1)
    PROMETHEERankingScores_desc['PROMETHEERang'] = range(1, len(PROMETHEERankingScores_desc) + 1)
    PAPRIKARankingScores_desc['PAPRIKARang'] = range(1, len(PAPRIKARankingScores_desc) + 1)

    DEXRankingScoresBump = pd.DataFrame(columns=['DEX'])

    for i in range(10):
        DEXRankingScoresBump = DEXRankingScoresBump._append(DEXRankingScores_desc.iloc[i])

    index_list = DEXRankingScoresBump.index.tolist()

    print("Sorted first 10 DEX rankings:")
    print(DEXRankingScoresBump)
    print("----------------------------------------------------------")

    AHPRankingScoresBump = pd.DataFrame(columns=['AHP'])

    for i in range(len(index_list)):
        alternativeID = AHPRankingScores_desc.loc[[index_list[i]]]

        AHPRankingScoresBump = AHPRankingScoresBump._append(alternativeID)

    print("10 AHP rankings:")
    print(AHPRankingScoresBump)
    print("----------------------------------------------------------")

    TOPSISRankingScoresBump = pd.DataFrame(columns=['TOPSIS'])

    for i in range(len(index_list)):
        alternativeID = TOPSISRankingScores_desc.loc[[index_list[i]]]

        TOPSISRankingScoresBump = TOPSISRankingScoresBump._append(alternativeID)

    print("10 TOPSIS rankings:")
    print(TOPSISRankingScoresBump)
    print("----------------------------------------------------------")

    PROMETHEERankingScoresBump = pd.DataFrame(columns=['PROMETHEE'])

    for i in range(len(index_list)):
        alternativeID = PROMETHEERankingScores_desc.loc[[index_list[i]]]

        PROMETHEERankingScoresBump = PROMETHEERankingScoresBump._append(alternativeID)

    print("10 PROMETHEE rankings:")
    print(PROMETHEERankingScoresBump)
    print("----------------------------------------------------------")

    PAPRIKARankingScoresBump = pd.DataFrame(columns=['PAPRIKA'])

    for i in range(len(index_list)):
        alternativeID = PAPRIKARankingScores_desc.loc[[index_list[i]]]

        PAPRIKARankingScoresBump = PAPRIKARankingScoresBump._append(alternativeID)

    print("10 PAPRIKA rankings:")
    print(PAPRIKARankingScoresBump)
    print("----------------------------------------------------------")

    # Combine rankings dataframes into one
    MCDMRankings_df = pd.concat(
        [DEXRankingScoresBump['DEXRang'], AHPRankingScoresBump['AHPRang'], TOPSISRankingScoresBump['TOPSISRang'], PROMETHEERankingScoresBump['PROMETHEERang'],
         PAPRIKARankingScoresBump['PAPRIKARang']], axis=1)

    # Print combined rankings
    print('Complete ranking results:')
    print(MCDMRankings_df)
    print("----------------------------------------------------------")

    # Save the DataFrame to a text file
    MCDMRankings_df.to_csv(directory + '/First10Rankings.csv', sep=';', index=True)

    # Transpose the DataFrame for plotting
    df_plot = MCDMRankings_df

    # Rename the columns for better readability
    df_plot.rename(columns={
        "DEXRang": "DEX",
        "AHPRang": "AHP",
        "TOPSISRang": "TOPSIS",
        "PROMETHEERang": "PROMETHEE",
        "PAPRIKARang": "PAPRIKA"
    }, inplace=True)

    # Plot the bump chart
    plt.figure(figsize=(12, 8))
    for index, row in df_plot.iterrows():
        plt.plot(row.index, row.values, marker='o', label=index)

    # Styling the chart
    plt.title("Rankings of first 10 DEX alternatives", fontsize=16)
    plt.xlabel("MCDM Rankings", fontsize=12)
    plt.ylabel("Ranking place", fontsize=12)
    plt.gca().invert_yaxis()  # Invert y-axis as lower rank is better
    plt.legend(title="Alternative ID", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    #plt.show()

    plt.savefig(directory + "/BumpChart.png")
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

DEXRanking_df = pd.read_csv('./Results/' + DEXRanking, index_col=0, delimiter=';')
AHPRanking_df = pd.read_csv('./Results/' + AHPRanking, index_col=0, delimiter=';')
TOPSISRanking_df = pd.read_csv('./Results/' + TOPSISRanking, index_col=0, delimiter=';')
PROMETHEERanking_df = pd.read_csv('./Results/' + PROMETHEERanking, index_col=0, delimiter=';')
PAPRIKARanking_df = pd.read_csv('./Results/' + PAPRIKARanking, index_col=0, delimiter=';')

CreateBumpChart(DEXRanking_df, AHPRanking_df, TOPSISRanking_df, PROMETHEERanking_df, PAPRIKARanking_df)