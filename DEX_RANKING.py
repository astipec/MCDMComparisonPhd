import numpy as np
import pandas as pd
from dex import DEXModel
from gini_population import DEXFunctionGiniPop

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
    print("----------------------------------------------------------")

    dexmodel = DEXModel('SKP Evaluation version 3.xml', function_class=DEXFunctionGiniPop)

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
        counter += 1

        RankingScores = np.append(RankingScores, res)

    AlterRankings_df = pd.DataFrame(RankingScores, index=index_array)

    # Print final ranking
    print('DEX final ranking results:')
    print(AlterRankings_df)
    print('----------------------------------------------------------')

    return AlterRankings_df

