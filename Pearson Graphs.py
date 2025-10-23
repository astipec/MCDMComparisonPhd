import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 10,
    'axes.titlesize': 14,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 10,
    'figure.titlesize': 16
})


def generate_correlated_data(n_samples=100, correlation_coefficient=0.0):
    mean = [0, 0]
    std_dev = [1, 1]
    covariance = correlation_coefficient * std_dev[0] * std_dev[1]

    cov_matrix = [
        [std_dev[0] ** 2, covariance],
        [covariance, std_dev[1] ** 2]
    ]

    data = np.random.multivariate_normal(mean, cov_matrix, n_samples)
    return data[:, 0], data[:, 1]

correlation_values = [
    1.0, 0.8, 0.4,
    0.0, -0.4, -0.8,
    -1.0, 0.2, 0.6
]

fig, axes = plt.subplots(3, 3, figsize=(12, 12))
axes = axes.flatten()

for i, r_val in enumerate(correlation_values):
    ax = axes[i]

    x, y = generate_correlated_data(n_samples=100, correlation_coefficient=r_val)

    ax.scatter(x, y, alpha=0.7, s=20)

    calculated_r = np.corrcoef(x, y)[0, 1]
    ax.set_title(f'r = {calculated_r:.2f}', fontsize=12)

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal', adjustable='box')

    # ax.set_xticks([])
    # ax.set_yticks([])

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('pearson_correlations.png', dpi=300)
plt.show()