import pandas as pd

def SortandExporttoCSV(df: pd.DataFrame, path):
    df_desc = df.sort_values(by='DEX', ascending=False)
    df_ranked = df_desc.assign(DEXRank=range(1, size + 1))

    df_ranked.to_csv(path + '/DEX_Results.csv', sep=';', index=True, header=True)