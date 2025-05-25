import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def Create_Heatmap(DataFrameMatrix: pd.DataFrame, Path, name, Cmap):
    g = sns.clustermap(
        DataFrameMatrix,
        annot=True,
        fmt='.2f',
        method="single",
        dendrogram_ratio=0.15,
        figsize=(8, 8),
        row_cluster=False,
        col_cluster=False,
        cmap=Cmap,
        vmin=0,
        vmax=9
    )

    g.ax_heatmap.yaxis.set_ticks_position("left")
    g.ax_heatmap.yaxis.set_label_position("left")
    g.ax_heatmap.set_ylim(len(DataFrameMatrix), 0)
    g.ax_heatmap.yaxis.tick_left()

    g.ax_row_dendrogram.set_visible(False)
    g.ax_col_dendrogram.set_visible(False)

    pos = g.ax_heatmap.get_position()
    g.ax_cbar.set_position([pos.x0 - 0.12, pos.y0, 0.02, pos.height])

    g.fig.suptitle(f'Heatmap of the AHP preference scale of "{name}" criterion', y=0.90)

    plt.savefig(Path + f"/Heatmap_{name}.png", bbox_inches='tight')

    plt.savefig(Path + "/Heatmap_" + name + ".png")
    plt.clf()
    plt.close()

    print("Created heatmap: " + name)
    print('-' * 58)

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