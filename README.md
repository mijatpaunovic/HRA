## Heart Rate Asymmetry Analysis

This repository contains Python code for reproducing results presented in the unpublished manuscript 
**"Mapping the Heart Rhythm: Leveraging Poincaré Plot Asymmetry to Detect Congestive Heart Failure and Age-related Changes"**,  
authored by [Mijat Paunović](https://orcid.org/0009-0006-4642-4695), [Marko Ćosić](https://orcid.org/0000-0002-4338-0555), [Nikola N. Radovanović](https://orcid.org/0000-0002-6545-2230), [Mirjana M. Platiša](https://orcid.org/0000-0002-0915-2823), and [Nadica Miljković](https://orcid.org/0000-0002-3933-6076).

---

## Repository Structure Overview

The repository is divided into **pipeline units**, placed in separate directories.  
Ordinal numbers of directories (and of their respective subdirectories) determine the sequence in which the scripts should be executed.

### 1. Data Preparation and Preprocessing

**_Data preparation_**

This directory is separated into subdirectories corresponding to two electrocardiogram (ECG) datasets:

- **Healthy Subjects (HS) group**
- **Patients with Congestive Heart Failure (CHF) group**

Given the different forms in which the datasets were obtained, they are prepared separately with specialized scripts as **MAT row vectors** of integer values indicating consecutive RR-interval durations (in milliseconds).  

Subsequently, throughout the entire pipeline, both prepared datasets flow through the same scripts, with only minor variations — mainly related to relative paths and descriptive naming.

---
### Dataset Placement

For reproducibility, obtain the two datasets and store them in the following locations within the repository structure:

1. [**Autonomic Aging: A dataset to quantify changes of cardiovascular autonomic function during healthy aging**](https://physionet.org/content/autonomic-aging-cardiovascular/1.0.0/)  
   → Place in: `0_data_preparation/hs/1_raw_ecg`

2. **Patients with Congestive Heart Failure (CHF)**  
   (Available from: *[insert link once available]*)  
   → Place in: `0_data_preparation/chf/2_raw_ecg_prepared`  
   *(Note: `1_raw_ecg` is skipped because the provided files are already in the required format.)*

---
To perform the analysis on your own datasets:

- Prepare them as **MAT row vectors** of RR-interval durations.  
- Place them in the same directories (`hs` or `chf`) as above.  
- **Do not rename** the directories or Python scripts, since many relative paths are hardcoded. Dataset labeling is handled through **USER CONFIGURATION** blocks inside subsequent Python scripts.

---
### Subsequent Subdirectories 

The following subdirectories contain Python scripts for:

- **Preprocessing**
- **Obtaining HRV from ECG**
- **Extracting the first 1, 5, 10, and 20 minutes of HRV** into separate **timescale directories**


---


        
    
  3. Application of inclusion criteria.
  4. Computation of nonlinear measures.
  5. Statistical analysis.
  6. Visualization.




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
