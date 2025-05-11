import pandas as pd
import os
from numpy import *

def PAPRIKAReplaceValues(AlterPAPRIKA: pd.DataFrame):
    # For PAPRIKA values I used 1000 minds to set criteria weights to be the same as local criteria from the DEX model
    # Based on the criteria values 1000 minds calculated the preference values for the PAPRIKA model
    # By doing so, first step of PAPRIKA, in which the decision makers answer questions to pairwise compare, is avoided
    # this way of ranking simulates if the same decision makers answer these questions to get the same weights of the criteria
    # and importance values for criteria categories.

    pd.set_option('future.no_silent_downcasting', True)

    AlterPAPRIKA['Available positions'] = AlterPAPRIKA['Available positions'].replace(['small', 'medium', 'large'],
                                                                                      [0, 4.9, 9.8])
    AlterPAPRIKA['SKPvsESCO'] = AlterPAPRIKA['SKPvsESCO'].replace(['>10', '5 - 10', '< 5 new competences'],
                                                                  [0, 9.8, 19.6])
    AlterPAPRIKA['Languages'] = AlterPAPRIKA['Languages'].replace(['no', 'yes'],
                                                                  [0, 4.4])
    AlterPAPRIKA['Driving license'] = AlterPAPRIKA['Driving license'].replace(['no', 'yes'],
                                                                              [0, 4.4])
    AlterPAPRIKA['Age appropriateness'] = AlterPAPRIKA['Age appropriateness'].replace(['no', 'yes'],
                                                                                      [0, 13.7])
    AlterPAPRIKA['Disability appropriateness'] = AlterPAPRIKA['Disability appropriateness'].replace(['no', 'yes'],
                                                                                                    [0, 13.7])
    AlterPAPRIKA['SKP Wish'] = AlterPAPRIKA['SKP Wish'].replace(['no', 'yes'],
                                                                [0, 4.6])
    AlterPAPRIKA['JS wishes for contract type'] = AlterPAPRIKA['JS wishes for contract type'].replace(['part time', 'full time', 'not important'],
                                                                                                      [0, 3.6, 7.1])
    AlterPAPRIKA['Job contract type'] = AlterPAPRIKA['Job contract type'].replace(['part time', 'full time'],
                                                                                  [0, 4.8])
    AlterPAPRIKA['JS career wishes'] = AlterPAPRIKA['JS career wishes'].replace(['downgrade', 'same', 'not important', 'upgrade career'],
                                                                                [0, 0, 0, 0])
    AlterPAPRIKA['Job career advancement'] = AlterPAPRIKA['Job career advancement'].replace(['down', 'same', 'up'],
                                                                                            [0, 2.4, 4.8])
    AlterPAPRIKA['Job working hours'] = AlterPAPRIKA['Job working hours'].replace(['daily/night shift', 'two-shift', 'afternoon shift', 'morning shift'],
                                                                                  [0, 0.7, 1.5, 2.2])
    AlterPAPRIKA['JS working hours wishes'] = AlterPAPRIKA['JS working hours wishes'].replace(['daily/night shift', 'two-shift', 'afternoon shift', 'morning shift'],
                                                                                              [0, 0.7, 1.5, 2.2])
    AlterPAPRIKA['Distance to job position'] = AlterPAPRIKA['Distance to job position'].replace(['> 20 km', '10 - 20 km', '< 10 km'],
                                                                                                [0, 3.7, 7.3])
    AlterPAPRIKA['JS wish location'] = AlterPAPRIKA['JS wish location'].replace(['no', 'yes'],
                                                                                [0, 1.6])

    return AlterPAPRIKA

def GetPAPRIKARankingResults(Alter: pd.DataFrame):
    # Weights of the criteria
    weights = array([9.82, 19.64, 4.42, 4.42, 13.68, 13.68, 4.56, 7.15, 4.77, 0, 4.47, 2.23, 2.23, 7.31, 1.62])

    print('Weights of the criteria')
    print(weights)
    print('----------------------------------------------------------')

    row_sums = Alter.sum(axis=1)

    AlterRankingsPAPRIKA_df = row_sums.to_frame('PAPRIKA')

    return AlterRankingsPAPRIKA_df

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

# PAPRIKA Ranking
print("PAPRIKA RANKING:")
print("----------------------------------------------------------")

TotalSKPData_RepVal = PAPRIKAReplaceValues(TotalSKPData_df)

print("TotalSKPData Criteria categories values dataframe:")
print(TotalSKPData_RepVal)
print("---------------------------")

PAPRIKARanking_df = GetPAPRIKARankingResults(TotalSKPData_RepVal)

# Print final ranking
print('PAPRIKA final ranking results:')
print(PAPRIKARanking_df)
print('----------------------------------------------------------')

PAPRIKARanking_df.to_csv(directory + '/PAPRIKARanking_' + filename, sep=';', index=True, header=True)