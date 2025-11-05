# HRA

## GitHub repository contents
The repository is structured in the following way:
1. Data prepa

## Heart Rate Asymmetry Analysis
This repository contains Python code for reproducing results presented in the manuscript "Mapping the Heart Rhythm: Leveraging Poincaré Plot Asymmetry to Detect Congestive Heart Failure and Age-related Changes
" and authored by [Mijat Paunović](https://orcid.org/0009-0006-4642-4695), [Marko Ćosić](https://orcid.org/0000-0002-4338-0555), [Nikola N. Radovanović](https://orcid.org/0000-0002-6545-2230), [Mirjana M. Platiša](https://orcid.org/0000-0002-0915-2823), and [Nadica Miljković](https://orcid.org/0000-0002-3933-6076).

## Code for HRA Analysis
The Python code for data preparation, preprocessing, and Heart Rate Asymmetry analysis is given in the following scripts:

### Project Code Overview
This workspace is structured as a sequential pipeline, moving from raw signal preparation through statistical analysis and figure generation. Each top-level directory corresponds to one stage of the workflow.

#### `0_data_preparation/`
- Houses subject-specific preprocessing pipelines for chronic heart failure (`chf/`) and healthy subjects (`hs/`).
- Subdirectories (`1_raw_ecg` → `5_extract_timescales`) track the evolution from raw ECG pulls to derived heart-rate variability (HRV) features and scale-dependent metrics.

#### `1_apply_inclusion_criteria/`
- Scripts (`1_extract_hs_ids.py`, `2_extract_chf_ids.py`) filter subject IDs that meet study criteria.
- `1_all_IDs/` and `2_extracted_IDs/` store intermediate CSV/JSON lists for healthy and CHF cohorts.

#### `2_compute_nonlinear_measures/`
- `calculate_pp_measures.py` aggregates processed signals and computes nonlinear point-process measures.
- Result folders (`results_oHS_vs_CHF/`, `results_yHS_vs_oHS/`) hold exports comparing cohorts (older vs. younger healthy subjects, healthy vs. CHF).

#### `3_statistical_analysis/`
- `run_statistical_analysis.py` conducts group-level statistical tests on the computed metrics.
- `hra/` includes auxiliary routines (e.g., heart rate asymmetry utilities); `results/` caches statistical summaries.

#### `4_visualization/`
- Contains plotting scripts for publication-ready figures; current focus is `effect_size_comparison/`.
- `effect_size_comparison_composite_bar_plot.py` recreates grouped bar charts like `grouped_bar_plot__oHS_vs_CHF.png`.

Use the directory numbers to follow the standard analysis order (0 → 4) when reproducing or extending the workflow.


# Data

# Disclaimer
The Python code is provided without any guarantee and it is not intended for medical purposes.

# Acknowledgements

# Contacts
Mijat Paunović (paunovicjata@gmail.com) or Nadica Miljković (e-mail: nadica.miljkovic@etf.bg.ac.rs).
# Funding
Nadica Miljković acknowledges the support from Grant No. 451-03-137/2025-03/200103 funded by the Ministry of Science,Technological Development and Innovation of the Republic of Serbia. Marko Ćosić acknowledges the support from Grant No. 451-03-136/2025-03/20001 funded by the Ministry of Science,Technological Development and Innovation of the Republic of Serbia. Mirjana M. Platiša acknowledges the support from Grant No. 451-03-137/2025-03/200110 funded by the Ministry of Science,Technological Development and Innovation of the Republic of Serbia.




# How to cite this repository?
If you find Heart Rate Asymmetry feature and Python code useful for your own research and teaching class, please cite the following references:
1. 
