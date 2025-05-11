import pandas as pd
import numpy as np
import os

from numpy import *
from scipy.sparse import lil_matrix, csr_matrix
from joblib import Parallel, delayed


def PROMETHEEReplaceValues(AlterPROMETHEE: pd.DataFrame):
    #PROMETHEE requires all criteria values to be numeric, here SKP values of 15 criteria are replaced by numeric ones
    pd.set_option('future.no_silent_downcasting', True)

    AlterPROMETHEE['Available positions'] = AlterPROMETHEE['Available positions'].replace(['small', 'medium', 'large'],
                                                                                          [1, 2, 3])
    AlterPROMETHEE['SKPvsESCO'] = AlterPROMETHEE['SKPvsESCO'].replace(['>10', '5 - 10', '< 5 new competences'],
                                                                      [1, 2, 3])
    AlterPROMETHEE['Languages'] = AlterPROMETHEE['Languages'].replace(['no', 'yes'],
                                                                      [1, 2])
    AlterPROMETHEE['Driving license'] = AlterPROMETHEE['Driving license'].replace(['no', 'yes'],
                                                                                  [1, 2])
    AlterPROMETHEE['Age appropriateness'] = AlterPROMETHEE['Age appropriateness'].replace(['no', 'yes'],
                                                                                          [1, 2])
    AlterPROMETHEE['Disability appropriateness'] = AlterPROMETHEE['Disability appropriateness'].replace(['no', 'yes'],
                                                                                                        [1, 2])
    AlterPROMETHEE['SKP Wish'] = AlterPROMETHEE['SKP Wish'].replace(['no', 'yes'],
                                                                    [1, 2])
    AlterPROMETHEE['JS wishes for contract type'] = AlterPROMETHEE['JS wishes for contract type'].replace(
        ['part time', 'full time', 'not important'],
        [1, 2, 3])
    AlterPROMETHEE['Job contract type'] = AlterPROMETHEE['Job contract type'].replace(['part time', 'full time'],
                                                                                      [1, 2])
    AlterPROMETHEE['JS career wishes'] = AlterPROMETHEE['JS career wishes'].replace(
        ['downgrade', 'same', 'not important', 'upgrade career'],
        [1, 2, 3, 4])
    AlterPROMETHEE['Job career advancement'] = AlterPROMETHEE['Job career advancement'].replace(['down', 'same', 'up'],
                                                                                                [1, 2, 3])
    AlterPROMETHEE['Job working hours'] = AlterPROMETHEE['Job working hours'].replace(
        ['daily/night shift', 'two-shift', 'afternoon shift', 'morning shift'],
        [1, 2, 3, 4])
    AlterPROMETHEE['JS working hours wishes'] = AlterPROMETHEE['JS working hours wishes'].replace(
        ['daily/night shift', 'two-shift', 'afternoon shift', 'morning shift'],
        [1, 2, 3, 4])
    AlterPROMETHEE['Distance to job position'] = AlterPROMETHEE['Distance to job position'].replace(
        ['> 20 km', '10 - 20 km', '< 10 km'],
        [1, 2, 3])
    AlterPROMETHEE['JS wish location'] = AlterPROMETHEE['JS wish location'].replace(['no', 'yes'],
                                                                                    [1, 2])

    return AlterPROMETHEE


def promethee(x, p, c, d, w):
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
        print('Criterion: ' + str(i+1))
        weighted_uni_net_flows[i] = w[i] * uni_cal(x[:, i], p[:, i], c[i], d[i])

    # Calculate total net flows by summing the weighted flows across all criteria
    total_net_flows = np.sum(weighted_uni_net_flows, axis=0)

    # Save the results to CSV after processing all criteria
    results_filename = './Results/weighted_uni_net_flows.csv'
    save_results_to_csv(weighted_uni_net_flows.T, results_filename)  # Transpose to match expected output

    print(total_net_flows)

    return np.round(total_net_flows, decimals=4)

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

def uni_cal(x, p, c, f):
    n = x.shape[0]
    print('n: ' + str(n))

    uni = lil_matrix((n, n), dtype=np.float32)  # Use lil_matrix for construction

    if f == 'li':
        # Use joblib to parallelize the computation of each row
        uni_data = Parallel(n_jobs=-1)(delayed(calculate_uni_for_pair)(i, x, p) for i in range(n))

        # Fill the sparse matrix with results from each row
        for i in range(n):
            print('i: ' + str(i))
            uni[i, :] = uni_data[i]

    # Convert to csr_matrix once construction is complete
    uni_csr = uni.tocsr()

    # Transpose if necessary (flip pos/neg flows accordingly)
    if c == 1:
        uni_csr = uni_csr.transpose()
        pos_flows = np.array(uni_csr.sum(axis=0)).flatten() / (n - 1)  # Transposed: axis=0 for positive flows
        neg_flows = np.array(uni_csr.sum(axis=1)).flatten() / (n - 1)
    else:
        pos_flows = np.array(uni_csr.sum(axis=1)).flatten() / (n - 1)  # Default case: axis=1 for positive flows
        neg_flows = np.array(uni_csr.sum(axis=0)).flatten() / (n - 1)

    # Calculate net flows
    net_flows = pos_flows - neg_flows

    return net_flows

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

def main():
    #Load TotalSKPData.csv
    #filename = 'SKPData_sample5.csv'  #load sample of first 5
    #filename = 'SKPData_sample100.csv'  #load sample of first 100
    filename = 'TotalSKPData.csv'  #load complete TotalSKPData

    directory = './Results'
    if not os.path.exists(directory):
        os.makedirs(directory)

    TotalSKPData_df = pd.read_csv('./' + filename, index_col=0, delimiter=';')

    index_array = TotalSKPData_df.index.to_numpy()

    print("TotalSKPData dataframe:")
    print(TotalSKPData_df)
    print("----------------------------------------------------------")

    # PROMETHEE II Ranking
    print("PROMETHEE II RANKING:")
    print("----------------------------------------------------------")

    TotalSKPData_RepVal = PROMETHEEReplaceValues(TotalSKPData_df)
    print("TotalSKPData numeric dataframe:")
    print(TotalSKPData_RepVal)
    print("----------------------------------------------------------")

    # Convert the DataFrame to a NumPy array
    TotalSKPData_np = TotalSKPData_RepVal.to_numpy(dtype='int8')
    print(TotalSKPData_np)
    print("----------------------------------------------------------")
    print("TotalSKPData_np datatype:")
    print(TotalSKPData_np.dtype)
    print("----------------------------------------------------------")

    # PROMETHEE II Ranking
    print("PROMETHEE II RANKING:")
    print("----------------------------------------------------------")

    # weights of the criteria
    weights = array([9.82, 19.64, 4.42, 4.42, 13.68, 13.68, 4.56, 7.15, 4.77, 0, 4.47, 2.23, 2.23, 7.31, 1.62],
                    dtype='float16')

    # Print weights of the criteria
    print('')
    print('Weights of the criteria')
    print(weights)
    print('----------------------------------------------------------')

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
    print('----------------------------------------------------------')

    # preference parameters of all criteria array
    p = array([pv, nv], dtype='int8')

    # Print the preference parameters of all criteria array
    print('')
    print('Preference parameters of all criteria array:')
    print(p)
    print('----------------------------------------------------------')

    # Criteria optimization array (0 for min, 1 for max)
    c = np.ones(TotalSKPData_np.shape[1], dtype=int8)

    # Preference function array
    d = ['li'] * TotalSKPData_np.shape[1]

    # final results
    final_net_flows = promethee(TotalSKPData_np, p, c, d, weights)

    with open('./SKP_PROMETHEE_II_RESULTS_' + filename, 'w') as f:
        f.write('alternatives;PROMETHEE')
        f.write('\n')

        for i in range(0, len(final_net_flows)):
            print(str(index_array[i]) + ': ' + str(final_net_flows[i]))
            f.write(str(index_array[i]) + ';' + str(final_net_flows[i]))
            f.write('\n')

if __name__ == '__main__':
    main()