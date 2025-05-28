# === Code taken from GitHub ===
# Author: Jason Papathanasiou, Nikolaos Ploskas
# Repository: https://github.com/springer-math/Multiple-Criteria-Decision-Aid
# Accessed on: 11.10.2022.

import pandas as pd
import numpy as np
import os

from numpy import *
from scipy.sparse import lil_matrix, csr_matrix
from joblib import Parallel, delayed

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

def PROMETHEEReplaceValues(AlterPROMETHEE: pd.DataFrame):
    # Replace qualitative values with quantitative
    # Simply begin with 1 for the lowest category and for each more valuable increase value by 1 (same as TOPSIS)

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
        AlterPROMETHEE[column] = AlterPROMETHEE[column].replace(value_map)

    return AlterPROMETHEE


def prometheeMC(x, p, c, d, w):
    # === START OF THIRD-PARTY CODE ===
    """Perform PROMETHEE analysis to compute net flows.

    Args:
        x (ndarray): Action performances array.
        p (ndarray): Preference parameters.
        c (ndarray): Criteria optimization array (0 for min, 1 for max).
        d (list): Preference function array.
        w (ndarray): Weights array.

    Returns:
        ndarray: Final net flows after applying PROMETHEE method.
    """


    weighted_uni_net_flows = np.zeros((x.shape[1], x.shape[0]))  # Preallocate array

    for i in range(x.shape[1]):
        weighted_uni_net_flows[i] = w[i] * uni_cal(x[:, i], p[:, i], c[i], d[i])

    # Calculate total net flows by summing the weighted flows across all criteria
    total_net_flows = np.sum(weighted_uni_net_flows, axis=0)

    return np.round(total_net_flows, decimals=4)
    # === END OF THIRD-PARTY CODE ===

# === START OF THIRD-PARTY CODE ===
def calculate_uni_for_pair(i, x, p):
    """Calculate preference values for a specific pair."""
    n = x.shape[0]
    results = np.zeros(n, dtype=np.float32)  # Initialize the result for this row
    for j in range(n):
        diff = x[i] - x[j]
        if diff > p[1]:
            results[j] = 1
        elif p[0] < diff <= p[1]:
            results[j] = (diff - p[0]) / (p[1] - p[0])
    return results
# === END OF THIRD-PARTY CODE ===

#This part of code (uni_cal function) is modified to support parallelization to speed up the process
def uni_cal(x, p, c, f):
    n = x.shape[0]
    uni = lil_matrix((n, n), dtype=np.float32)  # Use lil_matrix for construction

    if f == 'li':
        # Use joblib to parallelize the computation of each row
        uni_data = Parallel(n_jobs=-1)(delayed(calculate_uni_for_pair)(i, x, p) for i in range(n))

        # Fill the sparse matrix with results from each row
        for i in range(n):
            uni[i, :] = uni_data[i]

    # Convert to csr_matrix once construction is complete
    uni_csr = uni.tocsr()

    # Transpose if necessary (flip pos/neg flows accordingly)
    if c == 1:
        uni_csr = uni_csr.transpose()
        pos_flows = np.array(uni_csr.sum(axis=0)).flatten() / (n - 1)  # Transposed: axis=0 for positive flows
        neg_flows = np.array(uni_csr.sum(axis=1)).flatten() / (n - 1)
    else:
        pos_flows = np.array(uni_csr.sum(axis=1)).flatten() / (n - 1)  # Default case: axis=1 for negative flows
        neg_flows = np.array(uni_csr.sum(axis=0)).flatten() / (n - 1)

    # Calculate net flows
    net_flows = pos_flows - neg_flows

    return net_flows

# === START OF THIRD-PARTY CODE ===
def save_results_to_csv(results, filename):
    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)

    # Check if the file already exists
    if os.path.isfile(filename):
        # Append the results to the existing file
        results_df.to_csv(filename, mode='a', header=False, index=False)
    else:
        # Create a new file with header
        results_df.to_csv(filename, mode='w', header=True, index=False)
# === END OF THIRD-PARTY CODE ===

def main():
    filename = 'AHP_test.csv'  # load test sample (this is small sample of data for testing purposes)
    #filename = 'TotalSKPData.csv'  #load complete TotalSKPData (first run MCDMAnalysis_SKPdata.py to generate the dataset)

    directory = './Results'
    if not os.path.exists(directory):
        os.makedirs(directory)

    TotalSKPData_df = pd.read_csv('./' + filename, index_col=0, delimiter=';')

    index_array = TotalSKPData_df.index.to_numpy()

    print("TotalSKPData dataframe:")
    print(TotalSKPData_df)
    print('-' * 58)

    # PROMETHEE II Ranking
    print("PROMETHEE II RANKING:")
    print('-' * 58)

    TotalSKPData_RepVal = PROMETHEEReplaceValues(TotalSKPData_df)
    print("TotalSKPData numeric dataframe:")
    print(TotalSKPData_RepVal)
    print('-' * 58)

    # Convert the DataFrame to a NumPy array
    TotalSKPData_np = TotalSKPData_RepVal.to_numpy(dtype='int8')
    print(TotalSKPData_np)
    print('-' * 58)
    print("TotalSKPData_np datatype:")
    print(TotalSKPData_np.dtype)
    print('-' * 58)

    # PROMETHEE II Ranking
    print("PROMETHEE II RANKING:")
    print('-' * 58)

    # Weights of the criteria (global weights from the dexi model)
    weights = array([9.82, 19.64, 4.42, 4.42, 13.68, 13.68, 4.56, 7.15, 4.77, 0, 4.47, 2.23, 2.23, 7.31, 1.62],
                    dtype='float16')

    # Print weights of the criteria
    print('')
    print('Weights of the criteria')
    print(weights)
    print('-' * 58)

    # Maximum and minimum values for each criterion
    pv = array(amax(TotalSKPData_np, axis=0), dtype='int8')
    nv = array(amin(TotalSKPData_np, axis=0), dtype='int8')

    # Print the maximum values for each criterion
    print('')
    print('Maximum values for each criterion:')
    print(pv)

    # Print the minimum values for each criterion
    print('')
    print('Minimum values for each criterion:')
    print(nv)
    print('-' * 58)

    # preference parameters of all criteria array
    p = array([pv, nv], dtype='int8')

    # Print the preference parameters of all criteria array
    print('')
    print('Preference parameters of all criteria array:')
    print(p)
    print('-' * 58)

    # Criteria optimization array (0 for min, 1 for max)
    c = np.ones(TotalSKPData_np.shape[1], dtype=int8)

    # Preference function array
    d = ['li'] * TotalSKPData_np.shape[1]

    print('')
    print('Preference function array:')
    print(d)
    print('-' * 58)

    # final results
    final_net_flows = prometheeMC(TotalSKPData_np, p, c, d, weights)

    with open('./Results/PROMETHEE_Results.csv', 'w') as f:
        f.write('alternatives;PROMETHEE')
        f.write('\n')

        for i in range(0, len(final_net_flows)):
            print(str(index_array[i]) + ': ' + str(final_net_flows[i]))
            f.write(str(index_array[i]) + ';' + str(final_net_flows[i]))
            f.write('\n')

if __name__ == '__main__':
    main()