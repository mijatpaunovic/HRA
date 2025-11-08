from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import shapiro, ttest_ind, mannwhitneyu


def cohen_d(x: np.ndarray, y: np.ndarray) -> float:
    nx, ny = len(x), len(y)
    dof = nx + ny - 2
    pooled_std = np.sqrt(
        ((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1)) / dof
    )
    return (np.mean(x) - np.mean(y)) / pooled_std


def cliffs_delta(x: np.ndarray, y: np.ndarray) -> float:
    n, m = len(x), len(y)
    total = 0
    for xi in x:
        total += np.sum(np.sign(xi - y))
    return total / (n * m)


def calculate_effect_sizes(
    group1_data: pd.DataFrame,
    group2_data: pd.DataFrame,
    index_names: list[str],
    *,
    g1_label: str,
    g2_label: str,
) -> pd.DataFrame:
    """
    Compute normality per-group/index, pick t-test or Mann–Whitney, and return a tidy DataFrame
    with test, p-values (formatted), effect size and interpretation. Also includes a raw_p_value
    column (float) for conditional formatting and plotting badges.
    """
    results_list = []
    normality_flags = {}

    # Shapiro–Wilk normality per group/index
    for label, data in zip([g1_label, g2_label], [group1_data, group2_data]):
        for idx in index_names:
            arr = data[idx].dropna()
            if len(arr) < 3:
                normality_flags[(label, idx)] = 'Not Normal'
            else:
                _, pval = shapiro(arr)
                normality_flags[(label, idx)] = 'Normal' if pval > 0.05 else 'Not Normal'

    for idx in index_names:
        arr1 = group1_data[idx].dropna()
        arr2 = group2_data[idx].dropna()
        norm1 = normality_flags[(g1_label, idx)]
        norm2 = normality_flags[(g2_label, idx)]

        if norm1 == 'Normal' and norm2 == 'Normal':
            test_name = "Student's t-test"
            stat, pval = ttest_ind(arr1, arr2, nan_policy='omit')
            eff = cohen_d(arr1.values, arr2.values)
            eff_label = 'Cohen'
            abs_eff = abs(eff)
            if abs_eff < 0.25:
                interp = 'Small'
            elif abs_eff < 0.50:
                interp = 'Medium'
            elif abs_eff < 0.90:
                interp = 'Large'
            else:
                interp = 'Very Large'
        else:
            test_name = 'Mann-Whitney U test'
            stat, pval = mannwhitneyu(arr1, arr2, alternative='two-sided')
            eff = cliffs_delta(arr1.values, arr2.values)
            eff_label = 'Cliff'
            abs_eff = abs(eff)
            if abs_eff < 0.15:
                interp = 'Negligible'
            elif abs_eff < 0.33:
                interp = 'Small'
            elif abs_eff < 0.47:
                interp = 'Medium'
            else:
                interp = 'Large'

        formatted_p = "<0.001" if np.isfinite(pval) and pval < 0.001 else (f"{pval:.3f}" if np.isfinite(pval) else "NA")
        signif = 'Yes' if (np.isfinite(pval) and pval < 0.05) else 'No'

        results_list.append({
            'Index': idx,
            'Test Used': test_name,
            'Statistic': f"{stat:.3f}",
            'p-value': formatted_p,
            'Significant': signif,
            'Effect Size Test Used': eff_label,
            'Effect Size': f"{abs_eff:.3f}",
            'Effect Size Interpretation': interp,
            'raw_p_value': float(pval) if np.isfinite(pval) else np.nan,
        })

    return pd.DataFrame(results_list)
