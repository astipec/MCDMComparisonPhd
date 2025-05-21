# === Code taken from GitHub ===
# Author: Jason Papathanasiou, Nikolaos Ploskas
# Repository: https://github.com/springer-math/Multiple-Criteria-Decision-Aid
# Accessed on: 11.10.2022.

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

def TOPSISReplaceValues(AlterTOPSIS: pd.DataFrame):
    # Replace qualitative values with quantitative
    # Simply begin with 1 for the lowest category and for each more valuable increase value by 1

    map_three_topsis = {'small': 1, 'medium': 2, 'large': 3}
    map_competences_topsis = {'>10': 1, '5 - 10': 2, '< 5 new competences': 3}
    map_yes_no_topsis = {'no': 1, 'yes': 2}
    map_part_full_topsis = {'part time': 1, 'full time': 2, 'not important': 3}
    map_contract_topsis = {'part time': 1, 'full time': 2}
    map_career_topsis = {'downgrade': 1, 'same': 2, 'not important': 3, 'upgrade career': 4}
    map_advancement_topsis = {'down': 1, 'same': 2, 'up': 3}
    map_hours_topsis = {'daily/night shift': 1, 'two-shift': 2, 'afternoon shift': 3, 'morning shift': 4}
    map_distance_topsis = {'> 20 km': 1, '10 - 20 km': 2, '< 10 km': 3}

    replacement_maps_topsis = {
        col_available_positions: map_three_topsis,
        col_skp_vs_esco: map_competences_topsis,
        col_languages: map_yes_no_topsis,
        col_driving_license: map_yes_no_topsis,
        col_age: map_yes_no_topsis,
        col_disability: map_yes_no_topsis,
        col_skp_wish: map_yes_no_topsis,
        col_js_contract_wish: map_part_full_topsis,
        col_job_contract: map_contract_topsis,
        col_js_career: map_career_topsis,
        col_job_advancement: map_advancement_topsis,
        col_job_hours: map_hours_topsis,
        col_js_hours: map_hours_topsis,
        col_distance: map_distance_topsis,
        col_location: map_yes_no_topsis
    }

    pd.set_option('future.no_silent_downcasting', True)

    for column, value_map in replacement_maps_topsis.items():
        AlterTOPSIS[column] = AlterTOPSIS[column].replace(value_map)

    return AlterTOPSIS

def GetTOPSISRankingResults(AlterTOPSIS: pd.DataFrame):
    #Weights of the criteria (global weights from the dexi model)
    weights = array([9.82, 19.64, 4.42, 4.42, 13.68, 13.68, 4.56, 7.15, 4.77, 0, 4.47, 2.23, 2.23, 7.31, 1.62])

    print('Weights of the criteria')
    print(weights)
    print('-' * 58)

    # Convert DataFrame to NumPy array
    AlterArray = AlterTOPSIS.to_numpy()
    
    # Extract the index as a NumPy array
    index_array = AlterTOPSIS.index.to_numpy()

    # Step 1 (vector normalization): cumsum() produces the
    # cumulative sum of the values in the array and can also
    # be used with a second argument to indicate the axis to use

    # === START OF THIRD-PARTY CODE ===
    k = array(cumsum(AlterArray ** 2, 0))
    norm_x = array([[AlterArray[i, j] / sqrt(k[AlterArray.shape[0] - 1, j]) for j in range(AlterArray.shape[1])]
                    for i in range(AlterArray.shape[0])])
    # === END OF THIRD-PARTY CODE ===

    # Print the normalised matrix
    print('Normalised matrix:')
    print(norm_x)
    print('-' * 58)

    # Step 2 (Multiply each evaluation by the associated weight):
    # wnx is the weighted normalized x matrix

    # === START OF THIRD-PARTY CODE ===
    wnx = array([[norm_x[i, j] * weights[j]
                  for j in range(norm_x.shape[1])]
                 for i in range(norm_x.shape[0])])
    # === END OF THIRD-PARTY CODE ===

    # Print the weighted normalised matrix
    print('Weighted normalised matrix:')
    print(wnx)
    print('-' * 58)

    # Step 3 (positive and negative ideal solution)
    pis = array(amax(wnx, axis=0))
    nis = array(amin(wnx, axis=0))

    # Print the positive ideal soluton values
    print('Positive ideal solution:')
    print(pis)
    print('-' * 58)

    # Print the negative ideal soluton values
    print('Negative ideal solution:')
    print(nis)
    print('-' * 58)

    # Step 4a: determine the distance to the positive ideal
    # solution (dpis)

    # === START OF THIRD-PARTY CODE ===
    a = array([[(wnx[i, j] - pis[j]) ** 2
                for j in range(wnx.shape[1])]
               for i in range(wnx.shape[0])])
    dpis = sqrt(sum(a, 1))
    # === END OF THIRD-PARTY CODE ===

    # Step 4a: determine the distance to the negative ideal
    # solution (dnis)

    # === START OF THIRD-PARTY CODE ===
    a = array([[(wnx[i, j] - nis[j]) ** 2
                for j in range(wnx.shape[1])]
               for i in range(wnx.shape[0])])
    dnis = sqrt(sum(a, 1))
    # === END OF THIRD-PARTY CODE ===

    # Print the distance to the negative ideal solution
    print('Distance to the negative ideal solution')
    print(dnis)
    print('-' * 58)

    # Step 5: calculate the relative closeness to the ideal
    # solution
    RankingScores = array([dnis[i] / (dpis[i] + dnis[i]) for i in range(0, len(dpis))])

    AlterRankings_df = pd.DataFrame(RankingScores, index=index_array, columns=['TOPSIS'])

    return AlterRankings_df

filename = 'AHP_test.csv'  #load test sample (this is small sample of data for testing purposes)
#filename = 'TotalSKPData.csv'  #load complete TotalSKPData

directory = './Results'
if not os.path.exists(directory):
    os.makedirs(directory)

TotalSKPData_df = pd.read_csv('./'+filename, index_col=0, delimiter=';')

print("TotalSKPData dataframe:")
print(TotalSKPData_df)
print('-' * 58)

# TOPSIS Ranking
print("TOPSIS RANKING:")
print('-' * 58)

TotalSKPData_RepVal = TOPSISReplaceValues(TotalSKPData_df)

print("TotalSKPData Criteria categories values dataframe:")
print(TotalSKPData_RepVal)
print('-' * 58)

TOPSISRanking_df = GetTOPSISRankingResults(TotalSKPData_RepVal)

# Print final ranking
print('TOPSIS final ranking results:')
print(TOPSISRanking_df)
print('-' * 58)

TOPSISRanking_df.to_csv(directory + '/TOPSIS_Results.csv', sep=';', index=True, header=True)