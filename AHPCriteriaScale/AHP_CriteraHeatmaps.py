import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import gridspec

def Create_Heatmap(DataFrameMatrix: pd.DataFrame, Path, Name, Cmap):
    # Create a new figure with a custom grid layout for the colorbar position
    fig = plt.figure(figsize=(10, 7))
    gs = gridspec.GridSpec(1, 2, width_ratios=[0.1, 1], wspace=0.3)

    # Create the colorbar axis on the left
    cbar_ax = fig.add_subplot(gs[0])

    # Create the heatmap on the main axis
    ax = fig.add_subplot(gs[1])
    sns.heatmap(DataFrameMatrix, annot=True, cmap=Cmap, fmt=".2f", cbar=True, cbar_ax=cbar_ax, annot_kws={"size": 12})

    # Customize the colorbar and axis
    cbar_ax.yaxis.set_ticks_position('left')
    cbar_ax.yaxis.set_label_position('left')
    #cbar_ax.set_ylabel('Values', rotation=90, labelpad=10)

    # Remove x and y labels on the main heatmap
    ax.set_title('Heatmap of the "' + Name + '" criterion', fontsize=14, pad=20)
    ax.set_xlabel("")
    ax.set_ylabel("")

    #plt.show()

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