## Heart Rate Asymmetry Analysis

This repository contains Python code and RR intervals for reproducing results presented in the manuscript titled "Mapping the Heart Rhythm: Leveraging Poincaré Plot Asymmetry to Detect Congestive Heart Failure and Age-related Changes", that is currently under review and authored by [Mijat Paunović](https://orcid.org/0009-0006-4642-4695), [Marko Ćosić](https://orcid.org/0000-0002-4338-0555), [Nikola N. Radovanović](https://orcid.org/0000-0002-6545-2230), [Mirjana M. Platiša](https://orcid.org/0000-0002-0915-2823), and [Nadica Miljković](https://orcid.org/0000-0002-3933-6076).

# Brief Manuscript Overview
This study investigates the ability of various measures to quantify asymmetry in Poincaré plots (PP) derived from Heart Rate Variability (HRV) recordings across different subject groups and short-term timescales. For each timescale (1-, 5-, 10-, and 20-minute HRV segments), the performance of the newly proposed Kernel Density Estimation–based Asymmetry Magnitude Index (KDE AMI) is assessed alongside established asymmetry measures — Histogram-based AMI (HB AMI), Guzik Index (GI), Porta Index (PI), Asymmetric Spread Index (ASI), Slope Index (SI), and Area Index (AI) — in their ability to discriminate between subject groups. All Heart Rate Asymmetry (HRA) measures are benchmarked against the standard (non-HRA) Poincaré plot descriptors, SD1 and SD2.

---
## Repository Structure Overview

The repository is organized into **pipeline units**, each placed in a numbered directory. Ordinal numbers of directories (and their subdirectories) determine the execution sequence of scripts:
1. Data Preparation, Preprocessing and RR Interval Extraction
2. Application of Inclusion Criteria
3. Computation of Nonlinear Measures
4. Statistical Analyisis
5. Visualization

### 1️⃣ Data Preparation, Preprocessing and RR Interval Extraction

#### **_1.1 Data preparation_**

This directory is divided into subdirectories corresponding to two electrocardiogram (ECG) datasets:

- **Healthy Subjects (HS)** group  
- **Patients with Congestive Heart Failure (CHF)** group  

Given the different data formats, the two datasets are prepared separately with specialized scripts as **MAT row vectors** of integer values representing consecutive RR-interval durations (in milliseconds). After preparation, both datasets pass through identical processing scripts, differing only in relative paths and descriptive naming.

####  Inserting a Dataset into the Pipeline

For reproducibility, obtain and store the datasets in the following locations:

1. [**autonomic-aging-cardiovascular/1.0.0**](https://doi.org/10.13026/mwad-va85) [1-2]
   → Place in: `0_data_preparation/hs/1_raw_ecg`

2. **Patients with Congestive Heart Failure (CHF)**  
   (Available from: *[insert link once available]*)  
   → Place in: `0_data_preparation/chf/2_raw_ecg_prepared`  
   *(Note: `1_raw_ecg` is skipped because the provided files are already in the required format.)*

For custom datasets:

- Prepare recordings as **MAT row vectors** of RR-interval durations.  
- Ensure filenames use **3- or 4-digit zero-padded numbers** (e.g., `0023.mat`, `0008.mat`, …).  
- Place files into the corresponding directories (`hs` or `chf`).  
- **Do not rename** directories or Python scripts — many relative paths are hardcoded.  
- Dataset labeling is handled automatically through **USER CONFIGURATION** blocks in subsequent scripts.

---

#### **_1.2 Preprocessing and RR Interval Extraction_**

The following subdirectories contain Python scripts for:

- **Preprocessing raw ECG data**  
- **Obtaining HRV from an ECG**  
- **Extracting the first 1, 5, 10, and 20 minutes of HRV** into separate *timescale* directories  

each processing the output from the preceding one.

Refer to the script descriptions for detailed instructions on changes to be made in the **USER CONFIGURATION** blocks in order to run the scripts.

---

### 2️⃣ Application of Inclusion Criteria

Subject metadata are provided in different formats for the analyzed datasets:

- `1_hs_data.csv` (renamed from the original `subject-info.csv`) — for the HS group  
- `2_dcm_data.csv` — for the CHF group  

Each dataset requires its own Python script to extract subject IDs meeting the inclusion criteria:

- 1_extract_hs_ids.py — for the HS group
- 2_extract_chf_ids.py — for the CHF group

---

#### Reproducibility Notes

Refer to the **script descriptions** for detailed instructions on changes to be made in the **USER CONFIGURATION** blocks to adapt the script for different dataset comparisons.  

When applying the pipeline to other datasets:

- Define inclusion criteria appropriate to your dataset.  
- Save the resulting ID list as a **single-column CSV** named `ID`.  
  This ensures compatibility with downstream scripts.

---

### 3️⃣ Computation of Nonlinear Measures

This stage computes:

- **Standard Poincaré plot descriptors:** `SD1`, `SD2`  
- **Heart Rate Asymmetry (HRA) measures:**  
  - Guzik Index (GI)  
  - Porta Index (PI)  
  - Asymmetric Spread Index (ASI)  
  - Histogram-based Asymmetry Magnitude Index (HB AMI)  
  - Slope Index (SI)  
  - Area Index (AI)  
  - Kernel Density Estimation-based AMI (KDE AMI)

All are computed for each HRV signal and short-term timescale using  
`2_calculate_pp_measures.py`.

---

#### Reproducibility Notes

Before running this stage review the **USER CONFIGURATION** block within the script.   

---

### 4️⃣ Statistical Analysis

Statistical testing is conducted via `3_run_statistical_analysis.py`.

This step performs:

- **Normality testing**  
- **Effect size computation (Cohen’s d or Cliff’s δ)**  
- **CSV export of group-wise results**

---

#### Reproducibility Notes

Before execution:

- Modify paths and group names inside the **USER CONFIGURATION** block.  
- The script is compatible with outputs generated by the nonlinear measure computation step.

---

### 5️⃣ Visualization

This directory contains scripts for visualizing results:

1. **Grouped bar plots** comparing effect sizes of nonlinear measures across short-term timescales.  
2. **3D surface plots** illustrating how histogram resolution influences the performance of the HB AMI across timescales.  

---

#### Output

Figures are automatically saved in the same directory as their respective scripts, following descriptive naming conventions.

---


# Disclaimer
The Python code is provided without any guarantee and it is not intended for medical purposes.

# License
Unless otherwise stated, shared scripts are free software: anyone can redistribute them and/or modify them under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (optionally) any later version. These programs are distributed in the hope that they will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. For more details, see the GNU General Public License. Anyone accessing this code should have received a copy of the GNU General Public License along with these programs. If not, the license is available at: https://www.gnu.org/licenses/.

Please, report any bugs to the Author listed in the [Contacts](https://github.com/mijatpaunovic/HRA/tree/main?tab=readme-ov-file#contacts) section.

# Contacts
Mijat Paunović (paunovicjata@gmail.com) or Nadica Miljković (e-mail: nadica.miljkovic@etf.bg.ac.rs).

# Funding
Nadica Miljković acknowledges the support from Grant No. 451-03-137/2025-03/200103 funded by the Ministry of Science,Technological Development and Innovation of the Republic of Serbia. Marko Ćosić acknowledges the support from Grant No. 451-03-136/2025-03/20001 funded by the Ministry of Science,Technological Development and Innovation of the Republic of Serbia. Mirjana M. Platiša acknowledges the support from Grant No. 451-03-137/2025-03/200110 funded by the Ministry of Science,Technological Development and Innovation of the Republic of Serbia.

# References
1. Schumann, A., & Bär, K. (2021). Autonomic Aging: A dataset to quantify changes of cardiovascular autonomic function during healthy aging (version 1.0.0). PhysioNet. RRID:SCR_007345. [https://doi.org/10.13026/2hsy-t491](https://doi.org/10.13026/2hsy-t491)
2. Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220. RRID:SCR_007345. [https://doi.org/10.1161/01.cir.101.23.e215](https://doi.org/10.1161/01.cir.101.23.e215)

# How to cite this repository?
If you find Heart Rate Asymmetry index and Python code useful for your own research and teaching class, please cite the following references:
1. Paunović, M., Ćosić, M., Radovanović, N.N., Platiša, M.M., & Miljković, N. (2025). Mapping the Heart Rhythm: Leveraging Poincaré Plot Asymmetry to Detect Congestive Heart Failure and Age-related Changes, under review.
2. Paunović, M., Ćosić, M., Radovanović, N.N., Platiša, M.M., & Miljković, N. (2025). Software for Heart Rate Asymmetry Analysis, (Version 1.1) [Computer software]. Available at [https://github.com/mijatpaunovic/HRA](https://github.com/mijatpaunovic/HRA), Accessed on November 6, 2025. [https://doi.org/10.5281/zenodo.17544604](https://doi.org/10.5281/zenodo.17544604)
