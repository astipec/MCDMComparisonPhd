import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import gridspec

def Create_Heatmap(DataFrameMatrix: pd.DataFrame, Path, Name, Cmap):
    plt.figure(figsize=(5, 4))
    ax = sns.heatmap(DataFrameMatrix,
                     cmap=Cmap,
                     annot=True,
                     fmt=".2f",
                     linewidths=.5,
                     vmin=0,
                     vmax=9,
                     annot_kws={"size": 16})

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=10)

    ax.tick_params(axis='x', labelsize=12)  # fontsize za X os
    ax.tick_params(axis='y', labelsize=12)  # fontsize za Y os

    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(Path + "/" + Name + ".png")
    plt.clf()
    plt.close()

directory = './Results'
if not os.path.exists(directory):
    os.makedirs(directory)

criteria_names = {
    'C1': 'Available positions',
    'C2': 'SKPvsESCO',
    'C3': 'Languages',
    'C4': 'Driving license',
    'C5': 'Age appropriateness',
    'C6': 'Disability appropriateness',
    'C7': 'SKP Wish',
    'C8': 'JS wishes for contract type',
    'C9': 'Job contract type',
    'C10': 'JS career wishes',
    'C11': 'Job career advancement',
    'C12': 'Job working hours',
    'C13': 'JS working hours wishes',
    'C14': 'Distance to job position',
    'C15': 'JS wish location'
}

#Load all critera preferece scales and draw heatmaps
for i in range(1, 16):
    key = f'C{i}'
    path = f'./AHP Preference scale {key}.csv'

    if os.path.isfile(path):
        df = pd.read_csv(path, index_col=0, delimiter=';')
        title = criteria_names[key]  # koristi ime kriterija kao naslov
        Create_Heatmap(df, directory, title, 'Greens')
    else:
        print(f'File not found: {path}')