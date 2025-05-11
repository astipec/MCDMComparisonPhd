import pandas as pd
from pymcdm.methods import PROMETHEE_II
import warnings
from numpy import *

def PROMETHEEReplaceValues(AlterPROMETHEE: pd.DataFrame):
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
    AlterPROMETHEE['JS wishes for contract type'] = AlterPROMETHEE['JS wishes for contract type'].replace(['part time', 'full time', 'not important'],
                                                                                                      [1, 2, 3])
    AlterPROMETHEE['Job contract type'] = AlterPROMETHEE['Job contract type'].replace(['part time', 'full time'],
                                                                                  [1, 2])
    AlterPROMETHEE['JS career wishes'] = AlterPROMETHEE['JS career wishes'].replace(['downgrade', 'same', 'not important', 'upgrade career'],
                                                                                [1, 2, 3, 4])
    AlterPROMETHEE['Job career advancement'] = AlterPROMETHEE['Job career advancement'].replace(['down', 'same', 'up'],
                                                                                            [1, 2, 3])
    AlterPROMETHEE['Job working hours'] = AlterPROMETHEE['Job working hours'].replace(['daily/night shift', 'two-shift', 'afternoon shift', 'morning shift'],
                                                                                  [1, 2, 3, 4])
    AlterPROMETHEE['JS working hours wishes'] = AlterPROMETHEE['JS working hours wishes'].replace(['daily/night shift', 'two-shift', 'afternoon shift', 'morning shift'],
                                                                                              [1, 2, 3, 4])
    AlterPROMETHEE['Distance to job position'] = AlterPROMETHEE['Distance to job position'].replace(['> 20 km', '10 - 20 km', '< 10 km'],
                                                                                                [1, 2, 3])
    AlterPROMETHEE['JS wish location'] = AlterPROMETHEE['JS wish location'].replace(['no', 'yes'],
                                                                                [1, 2])

    return AlterPROMETHEE

def GetPROMETHEERankingResults(AlterPROMETHEE: pd.DataFrame):
    warnings.filterwarnings("ignore", category=UserWarning)

    # Weights of the criteria
    weights = array([9.82, 19.64, 4.42, 4.42, 13.68, 13.68, 4.56, 7.15, 4.77, 0, 4.47, 2.23, 2.23, 7.31, 1.62])

    print('Weights of the criteria')
    print(weights)
    print('----------------------------------------------------------')

    # Convert DataFrame to NumPy array
    AlterArray = AlterPROMETHEE.to_numpy()

    # Extract the index as a NumPy array
    index_array = AlterPROMETHEE.index.to_numpy()

    # Define types (e.g., positive or negative impact)
    types = array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    # Create an object of the PROMETHEE II method
    prom = PROMETHEE_II(preference_function='usual')
    prefs = prom(AlterArray, weights, types)

    # Create a Pandas dataframe for better visualization
    df = pd.DataFrame(prefs, index=index_array, columns=['PROMETHEE'])

    # Print final ranking
    print('PROMETHEE II final ranking results:')
    print(df)
    print('----------------------------------------------------------')

    return df