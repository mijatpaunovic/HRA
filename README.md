## Heart Rate Asymmetry Analysis

This repository contains Python code for reproducing results presented in the unpublished manuscript  
**"Mapping the Heart Rhythm: Leveraging Poincaré Plot Asymmetry to Detect Congestive Heart Failure and Age-related Changes"**,  
authored by [Mijat Paunović](https://orcid.org/0009-0006-4642-4695), [Marko Ćosić](https://orcid.org/0000-0002-4338-0555), [Nikola N. Radovanović](https://orcid.org/0000-0002-6545-2230), [Mirjana M. Platiša](https://orcid.org/0000-0002-0915-2823), and [Nadica Miljković](https://orcid.org/0000-0002-3933-6076).

---

## Repository Structure Overview

The repository is divided into pipeline units, placed in separate directories.  
Ordinal numbers of directories (and of their respective subdirectories) determine the sequence in which the scripts should be executed.

### Data Preparation and Preprocessing

**_Data preparation_**

This directory is separated into subdirectories corresponding to two electrocardiogram (ECG) datasets:

- Healthy Subjects (HS) group
- Patients with Congestive Heart Failure (CHF) group

Given the different forms in which the datasets were obtained, they are prepared separately with specialized scripts as MAT row vectors of integer values indicating consecutive RR-interval durations (in milliseconds). Subsequently, throughout the entire pipeline, both prepared datasets flow through the same scripts, with only minor variations - mainly related to relative paths and descriptive naming.

---
For reproducibility, obtain the two datasets and store them in the following locations within the repository structure:

1. [**Autonomic Aging: A dataset to quantify changes of cardiovascular autonomic function during healthy aging**](https://physionet.org/content/autonomic-aging-cardiovascular/1.0.0/)  
   → Place in: `0_data_preparation/hs/1_raw_ecg`

2. **Patients with Congestive Heart Failure (CHF)**  
   (Available from: *[insert link once available]*)  
   → Place in: `0_data_preparation/chf/2_raw_ecg_prepared`  
   *(Note: `1_raw_ecg` is skipped because the provided files are already in the required format.)*

---
To perform the analysis on different datasets:

- Prepare them as MAT row vectors of RR-interval durations.
- Make sure that the MAT files are named with 3- or 4-digit numbers, padded with zeros (_eg._ 0023.mat, 0008.mat ...)  
- Place them in the same directories (`hs` or `chf`) as above.  
- **Do not rename** the directories or Python scripts, since many relative paths are hardcoded. Dataset labeling is handled through **USER CONFIGURATION** blocks inside subsequent Python scripts.

---
**_Preprocessing and HRV Preparation_**
The following subdirectories contain Python scripts for:

- Preprocessing
- Obtaining HRV from ECG
- Extracting the first 1, 5, 10, and 20 minutes of HRV** into separate timescale directories

---

### 1. Application of Inclusion Criteria

Subject information are provided in different file formats:

- 1_hs_data.csv (renamed from the original subject-info.csv) for HS group
- 2_dcm_data.csv for CHF group

Respectively, two different scripts are required for the extraction of subject IDs which meet the inclusion criteria.

---
For reproducibility, refer to the script descriptions which will direct you to specific changes you should make within the USER CONFIGURATION blocks

---
To perform the analysis on a different dataset, you will need to apply the desired inclusion criteria based on the available subject information. To be able to continue through the pipeline, make sure that the ID list is stored as a column CSV file with the column named ID.

### 2. Computation of Nonlinear Measures
The standard Poincaré plot descriptors (SD1 and SD2) and Heart Rate Asymmetry (HRA) measures - Guzik Index, Porta Index, Asymmetric Spread Index, Histogram-based Asymmetry Magnitude Index (AMI), Slope Index, Area Index, and Kernel Density Estimation-based AMI - are computed for each HRV and for each short-term timescale using the 2_calculate_pp_measures.py script.

---
For reproducibility, as well as for application to a different dataset, refer to the script description which will direct you to specific changes you should make within the USER CONFIGURATION blocks.

### 3. Statistical Analysis

Statistical test are performed using the 3_run_statistical_analysis.py script.

---
For reproducibility, as well as for application to a different dataset, refer to the script description which will direct you to specific changes you should make within the USER CONFIGURATION blocks.

### 4. Visualization

This directory contains visualization scripts for:

1. Bar plot comparison of effect sizes achieved when employing nonlinear measures to distinguish between different subject groups across short-term timescales.
2. A three-dimensional surface plot which illustrates how histogram resolution affects the performance of HB AMI across short-term timescales.  

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
