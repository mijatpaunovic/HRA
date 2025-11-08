"""
Statistical Analysis
==================================================================================

This code conducts statistical analysis on the nonlinear measures (standard Poincaré
plot descriptors and Heart Rate Asymmetry Measures) for the purposes of the study:

    “Mapping the Heart Rhythm: Leveraging Poincaré Plot Asymmetry to Detect
    Congestive Heart Failure and Age-related Changes”
    by Mijat Paunović, Marko Ćosić, Nikola N. Radovanović,
    Mirjana M. Platiša, and Nadica Miljković

==================================================================================
User Instructions

To reproduce the results presented in the above study, configure the following
parameters in the **USER CONFIGURATION** block:

    Set choice value to perform statistical analysis for appropriate subject groups:
     - '1' for oHS vs. CHF
     - '2' for yHS vs. oHS

Optionally, the user may modify parameters in the **OPTIONAL SETTINGS** block
to experiment with different analysis configurations.

==================================================================================
Input: Path to the directory containing computed nonlinear measures.

Output: CSV files containing statistical analysis results for each short-term timescale.

==================================================================================
For inquiries or bug reports, please contact:

    • M. Paunović — paunovicjata@gmail.com
    • N. Miljković — nadica.miljkovic@etf.bg.ac.rs
"""
# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                         USER CONFIGURATION                                 ║
# ╚════════════════════════════════════════════════════════════════════════════╝

choice = 1 

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                             OPTIONAL                                       ║
# ╚════════════════════════════════════════════════════════════════════════════╝

if choice == 1:
    # Cohort abbreviations ensure descriptive output file naming
    g1 = 'oHS'
    g2 = 'CHF'
elif choice == 2:
        # Cohort abbreviations ensure descriptive output file naming
    g1 = 'yHS'
    g2 = 'oHS'

# --- Timescales (minutes) -----------------------------------------------------
TIMESCALES_MIN = [1, 5, 10, 20]
NUM_BINS_LIST  = [25, 50, 100, 150, 200, 300, 500, 1000]

# --- Plot y-axis limits -------------------------------------------------------
FIXED_YLIM = None

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                   END OF USER CONFIGURATION (DO NOT EDIT)                  ║
# ╚════════════════════════════════════════════════════════════════════════════╝
# Output base directory (results are grouped into per-timescale subfolders)
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_BASE_DIR = os.path.join(SCRIPT_DIR, "results", "statistical_analysis", f"{g1}_vs_{g2}")

# path to the base directory containing nonlinear measures for the respective groups
IDS_DIR = f"results/nonlinear_measures/{g1}_vs_{g2}"

# Input file name template (ensured by the previous scripts)
g1_FILENAME_TEMPLATE = "g1_{minutes}min_{num_bins}bins.csv"
g2_FILENAME_TEMPLATE = "g2_{minutes}min_{num_bins}bins.csv"

# Optional fallback (used only if the preferred name isn't found):
g1_ALT_FILENAME_TEMPLATE = "g1_{num_bins}bins.csv"
g2_ALT_FILENAME_TEMPLATE = "g2_{num_bins}bins.csv"

# ─────────────────────────────────────────────────────────────────────────────
# Internal imports and logic
# ─────────────────────────────────────────────────────────────────────────────
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend (no figure windows)

import pandas as pd
import numpy as np
from helper_functions import (
    calculate_effect_sizes,
    plot_boxplots_fixed_with_pvals,
)

def resolve_csv_path(base_dir: str,
                     minutes: int,
                     num_bins: int,
                     main_tpl: str,
                     alt_tpl: str | None = None) -> str | None:
    """
    Build the expected CSV path inside the '{minutes}min' subfolder.
    Try the main template first; if not found and alt_tpl is provided, try the alt.
    Return the first existing path or None if nothing matches.
    """
    timescale_folder = f"{minutes}min"
    folder_path = os.path.join(base_dir, timescale_folder)

    # Main (minutes+bins) filename
    main_name = main_tpl.format(minutes=minutes, num_bins=num_bins)
    main_path = os.path.join(folder_path, main_name)
    if os.path.isfile(main_path):
        return main_path

    # Optional fallback: only bins in filename
    if alt_tpl is not None:
        alt_name = alt_tpl.format(num_bins=num_bins)
        alt_path = os.path.join(folder_path, alt_name)
        if os.path.isfile(alt_path):
            return alt_path

    return None


def main():
    """Main analysis loop: iterates over all timescale/bin combinations."""
    for minutes in TIMESCALES_MIN:
        for num_bins in NUM_BINS_LIST:

            # Construct paths to input CSVs inside the '{minutes}min/' subfolder
            g1_path = resolve_csv_path(
                IDS_DIR, minutes, num_bins,
                g1_FILENAME_TEMPLATE, g1_ALT_FILENAME_TEMPLATE
            )
            g2_path = resolve_csv_path(
                IDS_DIR, minutes, num_bins,
                g2_FILENAME_TEMPLATE, g2_ALT_FILENAME_TEMPLATE
            )

            # Skip if either file missing
            if not g1_path or not g2_path:
                print(f"  Missing file(s) in '{minutes}min' for {num_bins} bins. Skipping.")
                continue

            # Load both group CSVs
            group1_data = pd.read_csv(g1_path, header=0, dtype=float)
            group2_data = pd.read_csv(g2_path, header=0, dtype=float)
            index_names = list(group1_data.columns)

            # Statistical analysis ------------------------------------------------
            eff_df = calculate_effect_sizes(group1_data, group2_data, index_names, g1_label=g1, g2_label=g2)

            # Store raw p-values
            pvals_map = {row['Index']: row['raw_p_value'] for _, row in eff_df.iterrows()}

            # Compute Relative Median Differences
            rmd_vals = []
            for idx in eff_df['Index']:
                g1_med = group1_data[idx].median()
                g2_med = group2_data[idx].median()
                rmd_vals.append(np.nan if g1_med == 0 else round(abs((g2_med - g1_med) / g1_med) * 100, 1))

            export_df = eff_df.copy()
            export_df.insert(0, "RMD [%]", rmd_vals)
            raw_ps = export_df.pop("raw_p_value").tolist()
            
            # Prepare output directory
            results_dir = os.path.join(RESULTS_BASE_DIR, f"results_{minutes}min_{num_bins}bins")
            os.makedirs(results_dir, exist_ok=True)

            # Save results as CSV instead of Excel
            csv_name = f"effect_size_results__{minutes}min_{num_bins}bins.csv"
            csv_path = os.path.join(results_dir, csv_name)
            export_df.to_csv(csv_path, index=False, float_format="%.4f")

            # --- Generate and save exactly two plots (with p-values) -----------------
            # Convention: first two indices correspond to SD1/SD2; rest are HRA indices.
            group1_indexes = index_names[:2]
            group2_indexes = index_names[2:]

            fig_sd = plot_boxplots_fixed_with_pvals(
                group1_data, group2_data, group1_indexes, pvals_map,
                g1_label=g1, g2_label=g2, fixed_ylim=FIXED_YLIM
            )
            fig_hra = plot_boxplots_fixed_with_pvals(
                group1_data, group2_data, group2_indexes, pvals_map,
                g1_label=g1, g2_label=g2, fixed_ylim=FIXED_YLIM
            )

            fig_sd.savefig(os.path.join(results_dir, "sd1_sd2.png"), dpi=300)
            fig_hra.savefig(os.path.join(results_dir, "hra_indices.png"), dpi=300)

            import matplotlib.pyplot as plt
            plt.close('all')

    print("\nAll combinations of timescales and num_bins have been processed.")


if __name__ == "__main__":
    main()
