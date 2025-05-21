# === Code taken from repository ===
# Author: Biljana Mileva Boshkoska
# Repository: https://repo.ijs.si/bmileva/dexpy/-/tree/gini/dex?ref_type=heads
# Accessed on: 12.01.2022.

import pandas as pd
import os
import numpy as np
import re

# === START OF THIRD-PARTY CODE ===
from DEX.dex import DEXModel
from DEX.gini_population import DEXFunctionGiniPop
# === END OF THIRD-PARTY CODE ===

class MyDictionary(dict):
    def add(self, key, value):
        self[key] = value

def sort_by_level(obj):
    return obj.level

def GetDEXRankingResults(AlterDEX: pd.DataFrame):
    # Extract the index as a NumPy array
    index_array = AlterDEX.index.to_numpy()

    AlterDEX['ID'] = AlterDEX.index

    #Set 'ID' column as the index and transpose the DataFrame
    result_dict = AlterDEX.set_index('ID').T.to_dict('list')

    print("Input dictionary for DEX ranking:")
    print(result_dict)
    print('-' * 58)

    # === START OF THIRD-PARTY CODE ===
    dexmodel = DEXModel('./DEX/SKP Evaluation version 3.xml', function_class=DEXFunctionGiniPop)

    possible_attr = ['Available positions',
                     'SKPvsESCO',
                     'Languages',
                     'Driving licence',
                     'Age appropriateness',
                     'Disability appropriateness',
                     'SKP Wish',
                     'BO wishes for contract type',
                     'Job contract type',
                     'BO career wishes',
                     'Job career advancement',
                     'Job working hours',
                     'BO working hours wishes',
                     'MSO Upravna Enota',
                     'BO wish location']

    optim_space = list(result_dict.values())
    data_optim = MyDictionary()

    x = sorted(dexmodel.functions.values(), key=sort_by_level)
    output_attribute = x[-1].name
    RankingScores = np.empty((0, 1))
    counter = 0

    for row in optim_space:
        for i in range(len(possible_attr)):
            data_optim.add(possible_attr[i], row[i])

        res = dexmodel.evaluate_model(data_optim)

        RankingScores = np.append(RankingScores, res)
    # === END OF THIRD-PARTY CODE ===

    DEX_df = pd.DataFrame(RankingScores, index=index_array)
    skp_series = DEX_df[0].apply(extract_skp_evaluation)
    AlterRankings_df = pd.DataFrame({"DEX": skp_series})

    # Print final ranking
    print('DEX final ranking results:')
    print(AlterRankings_df)
    print('-' * 58)

    return AlterRankings_df

def extract_skp_evaluation(text):
    match = re.search(r"'SKP Evaluation'\s*:\s*array\(\[([\d\.]+)\]\)", str(text))
    if match:
        return float(match.group(1))
    return None

filename = 'AHP_test.csv'  # load test sample
#filename = 'TotalSKPData.csv'  #load complete TotalSKPData

directory = './Results'
if not os.path.exists(directory):
    os.makedirs(directory)

TotalSKPData_df = pd.read_csv('./'+filename, index_col=0, delimiter=';')

print("TotalSKPData dataframe:")
print(TotalSKPData_df)
print('-' * 58)

# DEX RANKING
print("DEX RANKING:")
print('-' * 58)

DEXRankingScores = GetDEXRankingResults(TotalSKPData_df)

# Export DataFrame to a csv file
DEXRankingScores.to_csv(directory + '/DEX_Results.csv', sep=';', index=True, header=True)