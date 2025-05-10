import pandas as pd
import itertools
import os

def GenerateDataFrame():
    print("Generating dataset.\n")

    # Define lists
    c1 = ['small', 'medium', 'large']
    c2 = ['>10', '5 - 10', '< 5 new competences']
    c3 = ['no', 'yes']
    c4 = ['no', 'yes']
    c5 = ['no', 'yes']
    c6 = ['no', 'yes']
    c7 = ['no', 'yes']
    c8 = ['part time', 'full time', 'not important']
    c9 = ['part time', 'full time']
    c10 = ['downgrade', 'same', 'not important', 'upgrade career']
    c11 = ['down', 'same', 'up']
    c12 = ['daily/night shift', 'two-shift', 'afternoon shift', 'morning shift']
    c13 = ['daily/night shift', 'two-shift', 'afternoon shift', 'morning shift']
    c14 = ['> 20 km', '10 - 20 km', '< 10 km']
    c15 = ['no', 'yes']

    lists = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15]

    AlternativesAll = pd.DataFrame(list(itertools.product(*lists)),
                                   columns=['Available positions', 'SKPvsESCO', 'Languages', 'Driving license',
                                            'Age appropriateness', 'Disability appropriateness', 'SKP Wish',
                                            'JS wishes for contract type', 'Job contract type', 'JS career wishes',
                                            'Job career advancement', 'Job working hours', 'JS working hours wishes',
                                            'Distance to job position', 'JS wish location'
                                    ]
    )

    # Save the DataFrame to an CSV file
    file_name = './Results/TotalSKPData.csv'
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    AlternativesAll.to_csv(file_name)

    absolute_path = os.path.abspath(file_name)
    print(f'Dataset is saved to CSV file successfully at:\n{absolute_path}')