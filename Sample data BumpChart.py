import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

df = pd.read_csv("Sample data Project manager.csv", sep=";")
df = df.set_index("Candidate ID")

methods = df.columns
candidates = df.index

x = np.arange(len(methods))

plt.figure(figsize=(14, 8))

colors = plt.colormaps.get_cmap('tab20').resampled(len(candidates))

for i, candidate in enumerate(candidates):
    plt.plot(
        x,
        df.loc[candidate],
        marker='o',
        linewidth=2,
        color=colors(i),
        label=f"{candidate}"
    )

plt.gca().invert_yaxis()
plt.xticks(x, methods, fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("MCDM methods", fontsize=14)
plt.ylabel("rank", fontsize=14)
plt.legend(
    title="Candidates",
    bbox_to_anchor=(1.05, 1),
    loc='upper left',
    borderaxespad=0.,
    fontsize=10
)

plt.yticks(range(1, 16), range(1, 16))
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.subplots_adjust(right=0.80)

plt.savefig("bumpchart Project manager.png", dpi=300, bbox_inches="tight")
plt.show()