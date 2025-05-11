import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

def LoadRankings(MCDM_Name):
    file_map = {
        'DEX': 'DEX_Results.csv',
        'AHP': 'AHP_Results.csv',
        'TOPSIS': 'TOPSIS_Results.csv',
        'PROMETHEE': 'PROMETHEE_Results.csv',
        'PAPRIKA': 'PAPRIKA_Results.csv'
    }

    filename = file_map.get(MCDM_Name)
    if filename:
        path = './Results/' + filename
        df = pd.read_csv(path, index_col=0, delimiter=';')
        print(f"Loaded dataset for method '{MCDM_Name}':\n")
        print(df)
        return df

    return None

def extract_skp_evaluation(row):
    match = re.search(r"'SKP Evaluation': array\(\[([0-9.]+)\]\)", row)
    return float(match.group(1)) if match else None

def CombineRankings(DEXRanking_df, AHPRanking_df, TOPSISRanking_df, PROMETHEERanking_df, PAPRIKARanking_df):
    df_filtered = pd.DataFrame({'DEX': DEXRanking_df['0'].apply(extract_skp_evaluation)}, index=DEXRanking_df.index)

    MCDMRankings_df = pd.concat([df_filtered['DEX'],
                                      AHPRanking_df['AHP'],
                                      TOPSISRanking_df['TOPSIS'],
                                      PROMETHEERanking_df['PROMETHEE'],
                                      PAPRIKARanking_df['PAPRIKA']], axis=1)

    # Print combined rankings
    print('Complete ranking results:')
    print(MCDMRankings_df)
    print("----------------------------------------------------------")

    return MCDMRankings_df

def CalcCorrCoef(Rankings_df: pd.DataFrame, Method, Name):
    correlation_matrix = Rankings_df.corr(method=Method)

    print(Method+'\'s correlation coefficient matrix:')
    print(correlation_matrix)
    print("----------------------------------------------------------")

    # Save the DataFrame to a text file
    correlation_matrix.to_csv('./Results/' + Name + '.csv', sep=';', index=True)

    return correlation_matrix

def Create_Heatmap(DataFrameMatrix: pd.DataFrame, Method, name, Cmap):
    g = sns.clustermap(DataFrameMatrix, annot=True, fmt='.2f', method="single", dendrogram_ratio=0.15, figsize=(8, 8), row_cluster=True, col_cluster=True, cmap = Cmap, vmin = 0, vmax = 1)

    # Center the y-axis labels
    g.ax_heatmap.yaxis.set_ticks_position("left")

    # Hide the row and column dendrograms
    g.ax_row_dendrogram.set_visible(False)
    g.ax_col_dendrogram.set_visible(False)

    # Move the colorbar to the left
    g.ax_cbar.set_position((0.02, 0.2, 0.03, 0.4))
    g.fig.suptitle("Heatmap of the " + Method + "'s correlation coefficient for the " + name)

    plt.savefig("./Results/Heatmap_"+name+".png")
    plt.clf()
    plt.close()

    print("Created heatmap: " + Method+"_Heatmap for the " + name)
    print("----------------------------------------------------------")

def CalcCorrelations():
    # Load all ranking results from all five MCDM methods
    DEXRanking_df = LoadRankings('DEX')
    AHPRanking_df = LoadRankings('AHP')
    TOPSISRanking_df = LoadRankings('TOPSIS')
    PROMETHEERanking_df = LoadRankings('PROMETHEE')
    PAPRIKARanking_df = LoadRankings('PAPRIKA')

    print(f"All datasets are loaded successfully.")

    directory = './Results'

    MCDMRankings_df = CombineRankings(DEXRanking_df, AHPRanking_df, TOPSISRanking_df, PROMETHEERanking_df, PAPRIKARanking_df)
    MCDMRankings_df.to_csv(directory + '/CompleteRankings.csv', sep=';', index=True)

    # Calculate the ranking coefficients
    Pearson_df = CalcCorrCoef(MCDMRankings_df, "pearson", "Pearson_MCDMRankings")
    Spearman_df = CalcCorrCoef(MCDMRankings_df, "spearman", "Spearman_MCDMRankings")
    Kendall_df = CalcCorrCoef(MCDMRankings_df, "kendall", "Kendall_MCDMRankings")

    # Create heatmaps
    Create_Heatmap(Pearson_df, "Pearson", "Pearson_MCDMRankings", "coolwarm")
    Create_Heatmap(Spearman_df, "Spearman", "Spearman_MCDMRankings", "coolwarm")
    Create_Heatmap(Kendall_df, "Kendall", "Kendall_MCDMRankings", "coolwarm")