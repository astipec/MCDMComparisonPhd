import pandas as pd
import os
from numpy import *

def TOPSISReplaceValues(AlterTOPSIS: pd.DataFrame):
    pd.set_option('future.no_silent_downcasting', True)

    AlterTOPSIS['Available positions'] = AlterTOPSIS['Available positions'].replace(['small', 'medium', 'large'],
                                                                                      [1, 2, 3])
    AlterTOPSIS['SKPvsESCO'] = AlterTOPSIS['SKPvsESCO'].replace(['>10', '5 - 10', '< 5 new competences'],
                                                                  [1, 2, 3])
    AlterTOPSIS['Languages'] = AlterTOPSIS['Languages'].replace(['no', 'yes'],
                                                                  [1, 2])
    AlterTOPSIS['Driving license'] = AlterTOPSIS['Driving license'].replace(['no', 'yes'],
                                                                              [1, 2])
    AlterTOPSIS['Age appropriateness'] = AlterTOPSIS['Age appropriateness'].replace(['no', 'yes'],
                                                                                      [1, 2])
    AlterTOPSIS['Disability appropriateness'] = AlterTOPSIS['Disability appropriateness'].replace(['no', 'yes'],
                                                                                                    [1, 2])
    AlterTOPSIS['SKP Wish'] = AlterTOPSIS['SKP Wish'].replace(['no', 'yes'],
                                                                [1, 2])
    AlterTOPSIS['JS wishes for contract type'] = AlterTOPSIS['JS wishes for contract type'].replace(['part time', 'full time', 'not important'],
                                                                                                      [1, 2, 3])
    AlterTOPSIS['Job contract type'] = AlterTOPSIS['Job contract type'].replace(['part time', 'full time'],
                                                                                  [1, 2])
    AlterTOPSIS['JS career wishes'] = AlterTOPSIS['JS career wishes'].replace(['downgrade', 'same', 'not important', 'upgrade career'],
                                                                                [1, 2, 3, 4])
    AlterTOPSIS['Job career advancement'] = AlterTOPSIS['Job career advancement'].replace(['down', 'same', 'up'],
                                                                                            [1, 2, 3])
    AlterTOPSIS['Job working hours'] = AlterTOPSIS['Job working hours'].replace(['daily/night shift', 'two-shift', 'afternoon shift', 'morning shift'],
                                                                                  [1, 2, 3, 4])
    AlterTOPSIS['JS working hours wishes'] = AlterTOPSIS['JS working hours wishes'].replace(['daily/night shift', 'two-shift', 'afternoon shift', 'morning shift'],
                                                                                              [1, 2, 3, 4])
    AlterTOPSIS['Distance to job position'] = AlterTOPSIS['Distance to job position'].replace(['> 20 km', '10 - 20 km', '< 10 km'],
                                                                                                [1, 2, 3])
    AlterTOPSIS['JS wish location'] = AlterTOPSIS['JS wish location'].replace(['no', 'yes'],
                                                                                [1, 2])
    return AlterTOPSIS

def GetTOPSISRankingResults(AlterTOPSIS: pd.DataFrame):
    #Weights of the criteria
    weights = array([9.82, 19.64, 4.42, 4.42, 13.68, 13.68, 4.56, 7.15, 4.77, 0, 4.47, 2.23, 2.23, 7.31, 1.62])

    print('Weights of the criteria')
    print(weights)
    print('----------------------------------------------------------')

    # Convert DataFrame to NumPy array
    AlterArray = AlterTOPSIS.to_numpy()

    # Extract the index as a NumPy array
    index_array = AlterTOPSIS.index.to_numpy()

    # Step 1 (vector normalization): cumsum() produces the
    # cumulative sum of the values in the array and can also
    # be used with a second argument to indicate the axis to use
    k = array(cumsum(AlterArray ** 2, 0))
    norm_x = array([[AlterArray[i, j] / sqrt(k[AlterArray.shape[0] - 1, j]) for j in range(AlterArray.shape[1])]
                    for i in range(AlterArray.shape[0])])

    # Print the normalised matrix
    print('Normalised matrix:')
    print(norm_x)
    print('----------------------------------------------------------')

    # Step 2 (Multiply each evaluation by the associated weight):
    # wnx is the weighted normalized x matrix
    wnx = array([[norm_x[i, j] * weights[j]
                  for j in range(norm_x.shape[1])]
                 for i in range(norm_x.shape[0])])

    # Print the weighted normalised matrix
    print('Weighted normalised matrix:')
    print(wnx)
    print('----------------------------------------------------------')

    # Step 3 (positive and negative ideal solution)
    pis = array(amax(wnx, axis=0))
    nis = array(amin(wnx, axis=0))

    # Print the positive ideal soluton values
    print('Positive ideal solution:')
    print(pis)
    print('----------------------------------------------------------')

    # Print the negative ideal soluton values
    print('Negative ideal solution:')
    print(nis)
    print('----------------------------------------------------------')

    # Step 4a: determine the distance to the positive ideal
    # solution (dpis)
    a = array([[(wnx[i, j] - pis[j]) ** 2
                for j in range(wnx.shape[1])]
               for i in range(wnx.shape[0])])
    dpis = sqrt(sum(a, 1))

    # Step 4a: determine the distance to the negative ideal
    # solution (dnis)
    a = array([[(wnx[i, j] - nis[j]) ** 2
                for j in range(wnx.shape[1])]
               for i in range(wnx.shape[0])])
    dnis = sqrt(sum(a, 1))

    # Print the distance to the negative ideal solution
    print('Distance to the negative ideal solution')
    print(dnis)
    print('----------------------------------------------------------')

    # Step 5: calculate the relative closeness to the ideal
    # solution
    RankingScores = array([dnis[i] / (dpis[i] + dnis[i]) for i in range(0, len(dpis))])

    AlterRankings_df = pd.DataFrame(RankingScores, index=index_array, columns=['TOPSIS'])

    # Print final ranking
    print('TOPSIS final ranking results:')
    print(AlterRankings_df)
    print('----------------------------------------------------------')

    return AlterRankings_df

#Load TotalSKPData.csv
#filename = 'SKPData_sample100.csv'  #load sample of first 100
filename = 'TotalSKPData.csv'  #load complete TotalSKPData

directory = './Results'
if not os.path.exists(directory):
    os.makedirs(directory)

TotalSKPData_df = pd.read_csv('./'+filename, index_col=0, delimiter=';')

print("TotalSKPData dataframe:")
print(TotalSKPData_df)
print("----------------------------------------------------------")

# TOPSIS Ranking
print("TOPSIS RANKING:")
print("----------------------------------------------------------")

TotalSKPData_RepVal = TOPSISReplaceValues(TotalSKPData_df)

print("TotalSKPData Criteria categories values dataframe:")
print(TotalSKPData_RepVal)
print("---------------------------")

TOPSISRanking_df = GetTOPSISRankingResults(TotalSKPData_RepVal)

# Print final ranking
print('TOPSIS final ranking results:')
print(TOPSISRanking_df)
print('----------------------------------------------------------')

TOPSISRanking_df.to_csv(directory + '/TOPSISRanking_' + filename, sep=';', index=True, header=True)