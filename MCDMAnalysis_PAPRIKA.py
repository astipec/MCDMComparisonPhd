import pandas as pd
import os
from numpy import *

col_available_positions = 'Available positions'
col_skp_vs_esco = 'SKPvsESCO'
col_languages = 'Languages'
col_driving_license = 'Driving license'
col_age = 'Age appropriateness'
col_disability = 'Disability appropriateness'
col_skp_wish = 'SKP Wish'
col_js_contract_wish = 'JS wishes for contract type'
col_job_contract = 'Job contract type'
col_js_career = 'JS career wishes'
col_job_advancement = 'Job career advancement'
col_job_hours = 'Job working hours'
col_js_hours = 'JS working hours wishes'
col_distance = 'Distance to job position'
col_location = 'JS wish location'

def PAPRIKAReplaceValues(AlterPAPRIKA: pd.DataFrame):
    # For PAPRIKA values I used 1000 minds to set criteria weights to be the same as local criteria from the DEX model
    # Based on the criteria values 1000 minds calculated the preference values for the PAPRIKA model
    # By doing so, first step of PAPRIKA, in which the decision makers answer questions to pairwise compare, is avoided,
    # this way of ranking simulates if the same decision makers answer these questions to get the same weights of the criteria
    # and importance values for criteria categories.

    replacement_maps_paprika = {
        col_available_positions: {'small': 0, 'medium': 4.9, 'large': 9.8},
        col_skp_vs_esco: {'>10': 0, '5 - 10': 9.8, '< 5 new competences': 19.6},
        col_languages: {'no': 0, 'yes': 4.4},
        col_driving_license: {'no': 0, 'yes': 4.4},
        col_age: {'no': 0, 'yes': 13.7},
        col_disability: {'no': 0, 'yes': 13.7},
        col_skp_wish: {'no': 0, 'yes': 4.6},
        col_js_contract_wish: {'part time': 0, 'full time': 3.6, 'not important': 7.1},
        col_job_contract: {'part time': 0, 'full time': 4.8},
        col_js_career: {'downgrade': 0, 'same': 0, 'not important': 0, 'upgrade career': 0},
        col_job_advancement: {'down': 0, 'same': 2.4, 'up': 4.8},
        col_job_hours: {'daily/night shift': 0, 'two-shift': 0.7, 'afternoon shift': 1.5, 'morning shift': 2.2},
        col_js_hours: {'daily/night shift': 0, 'two-shift': 0.7, 'afternoon shift': 1.5, 'morning shift': 2.2},
        col_distance: {'> 20 km': 0, '10 - 20 km': 3.7, '< 10 km': 7.3},
        col_location: {'no': 0, 'yes': 1.6}
    }

    pd.set_option('future.no_silent_downcasting', True)

    for column, value_map in replacement_maps_paprika.items():
        AlterPAPRIKA[column] = AlterPAPRIKA[column].replace(value_map)

    return AlterPAPRIKA

def GetPAPRIKARankingResults(Alter: pd.DataFrame):
    #Weights of the criteria (global weights from the dexi model)
    weights = array([9.82, 19.64, 4.42, 4.42, 13.68, 13.68, 4.56, 7.15, 4.77, 0, 4.47, 2.23, 2.23, 7.31, 1.62])

    print('Weights of the criteria')
    print(weights)
    print('-' * 58)

    row_sums = Alter.sum(axis=1)

    AlterRankingsPAPRIKA_df = row_sums.to_frame('PAPRIKA')

    return AlterRankingsPAPRIKA_df

filename = 'AHP_test.csv'  # load test sample (this is small sample of data for testing purposes)
#filename = 'TotalSKPData.csv'  #load complete TotalSKPData (first run MCDMAnalysis_SKPdata.py to generate the dataset)

directory = './Results'
if not os.path.exists(directory):
    os.makedirs(directory)

TotalSKPData_df = pd.read_csv('./'+filename, index_col=0, delimiter=';')

print("TotalSKPData dataframe:")
print(TotalSKPData_df)
print('-' * 58)

# PAPRIKA Ranking
print("PAPRIKA RANKING:")
print('-' * 58)

TotalSKPData_RepVal = PAPRIKAReplaceValues(TotalSKPData_df)

print("TotalSKPData Criteria categories values dataframe:")
print(TotalSKPData_RepVal)
print('-' * 58)

PAPRIKARanking_df = GetPAPRIKARankingResults(TotalSKPData_RepVal)

# Print final ranking
print('PAPRIKA final ranking results:')
print(PAPRIKARanking_df)
print('-' * 58)

PAPRIKARanking_df.to_csv(directory + '/PAPRIKA_Results.csv', sep=';', index=True, header=True)