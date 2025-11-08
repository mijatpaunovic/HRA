from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


PVAL_FONT_SIZE = 16


def _format_p(p: float) -> str:
    return "<0.001" if np.isfinite(p) and p < 0.001 else (f"{p:.3f}" if np.isfinite(p) else "NA")


def _grid_shape(n: int) -> tuple[int, int]:
    if n <= 2:
        return (1, n)
    elif n <= 4:
        return (2, 2)
    elif n <= 6:
        return (2, 3)
    else:
        cols = int(np.ceil(np.sqrt(n)))
        rows = int(np.ceil(n / cols))
        return (rows, cols)


def _compute_fixed_ylim_if_needed(
    group1_data: pd.DataFrame, group2_data: pd.DataFrame, indices: list[str], fixed_ylim: tuple[float, float] | None
) -> tuple[float, float] | None:
    if fixed_ylim is not None:
        return fixed_ylim
    vals = []
    for idx in indices:
        vals.append(group1_data[idx].dropna().values)
        vals.append(group2_data[idx].dropna().values)
    if not vals:
        return (0.0, 1.0)
    vals = np.concatenate(vals)
    vmin, vmax = np.nanmin(vals), np.nanmax(vals)
    if not np.isfinite(vmin) or not np.isfinite(vmax):
        return (0.0, 1.0)
    pad = 0.05 * (vmax - vmin) if vmax != vmin else 1.0
    return (vmin - pad, vmax + pad)


def plot_boxplots_fixed_with_pvals(
    group1_data: pd.DataFrame,
    group2_data: pd.DataFrame,
    indices: list[str],
    pvals_map: dict[str, float],
    *,
    g1_label: str,
    g2_label: str,
    fixed_ylim: tuple[float, float] | None = None,
):
    """
    Multi-panel boxplots of indices for two groups with:
      • shared fixed y-limits (global per figure if None, computed from pooled data),
      • bold p-value badge per panel,
      • ONLY the bottom-most OCCUPIED subplot in each column shows x-axis labels,
      • y-ticks shown only on the first column to reduce clutter.
    """
    rows, cols = _grid_shape(len(indices))
    fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 4.5*rows))
    if not isinstance(axes, np.ndarray):
        axes = np.array([axes])
    axes = axes.flatten()

    shared_ylim = _compute_fixed_ylim_if_needed(group1_data, group2_data, indices, fixed_ylim)

    # Determine the bottom-most occupied row in each column
    bottom_row_by_col = {}
    for i in range(len(indices)):
        r, c = divmod(i, cols)
        bottom_row_by_col[c] = max(bottom_row_by_col.get(c, 0), r)

    for i, idx in enumerate(indices):
        ax = axes[i]
        g1_vals = group1_data[idx].dropna()
        g2_vals = group2_data[idx].dropna()

        ax.boxplot([g1_vals, g2_vals], labels=[g1_label, g2_label], widths=0.5, positions=[1, 2])
        if shared_ylim is not None:
            ax.set_ylim(shared_ylim)
        ax.grid(True, linestyle=':', linewidth=0.6, alpha=0.8)
        ax.tick_params(axis='x', labelsize=22)
        ax.tick_params(axis='y', labelsize=22)

        # Show x labels only on lowest OCCUPIED subplot in this column
        r, c = divmod(i, cols)
        if r != bottom_row_by_col.get(c, r):
            ax.set_xticklabels([])

        # p-value badge
        p = float(pvals_map.get(idx, np.nan))
        ax.text(
            0.98, 0.95, f"p={_format_p(p)}",
            transform=ax.transAxes,
            ha='right', va='top',
            fontsize=PVAL_FONT_SIZE, fontweight='bold',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        )

        # Optional: hide y-ticks/label for non-first columns
        if (i % cols) != 0:
            ax.set_ylabel("")
            ax.set_yticklabels([])

    # Hide any unused axes (if grid has extra slots)
    for j in range(len(indices), len(axes)):
        axes[j].set_visible(False)

    fig.tight_layout()
    return fig
