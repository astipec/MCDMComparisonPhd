import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 10,
    'axes.titlesize': 14,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'figure.titlesize': 16
})

N = 100

x1 = np.linspace(1, 10, N)
y1 = x1 + np.random.normal(0, 0.5, N)
r_s1, _ = spearmanr(x1, y1)
r_p1 = np.corrcoef(x1, y1)[0, 1]

x2 = np.linspace(1, 10, N)
y2 = -x2 + np.random.normal(0, 0.5, N)
r_s2, _ = spearmanr(x2, y2)
r_p2 = np.corrcoef(x2, y2)[0, 1]

x3 = np.linspace(-3, 3, N)
y3 = x3 ** 3 + np.random.normal(0, 3, N)
r_s3, _ = spearmanr(x3, y3)
r_p3 = np.corrcoef(x3, y3)[0, 1]

x4 = np.random.rand(N) * 10
y4 = np.random.rand(N) * 10
r_s4, _ = spearmanr(x4, y4)
r_p4 = np.corrcoef(x4, y4)[0, 1]

fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()

data_sets = [
    (x1, y1, r_s1, r_p1, "Strong Positive, Linear"),
    (x2, y2, r_s2, r_p2, "Strong Negative, Linear"),
    (x3, y3, r_s3, r_p3, "Monotonic, Non-linear (Cubic)"),
    (x4, y4, r_s4, r_p4, "No Relationship")
]

for i, (x, y, r_s, r_p, title) in enumerate(data_sets):
    ax = axes[i]
    ax.scatter(x, y, alpha=0.7, s=30, color='darkblue')

    ax.set_title(f'{title}\n'
                 f'Spearman $\\rho_s$ = {r_s:.2f}, Pearson $r$ = {r_p:.2f}',
                 fontsize=12)

    # Podešavanje osi za svaki graf
    ax.set_xlabel('x')
    ax.set_ylabel('y')

# Prilagođavanje izgleda
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('spearman_correlations.png', dpi=300)
plt.show()