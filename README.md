## Heart Rate Asymmetry Analysis

This repository contains Python code for reproducing results presented in the unpublished manuscript  
**"Mapping the Heart Rhythm: Leveraging Poincaré Plot Asymmetry to Detect Congestive Heart Failure and Age-related Changes"**,  
authored by [Mijat Paunović](https://orcid.org/0009-0006-4642-4695), [Marko Ćosić](https://orcid.org/0000-0002-4338-0555), [Nikola N. Radovanović](https://orcid.org/0000-0002-6545-2230), [Mirjana M. Platiša](https://orcid.org/0000-0002-0915-2823), and [Nadica Miljković](https://orcid.org/0000-0002-3933-6076).

---

## 📁 Repository Structure Overview

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

#### 📦 Inserting a Dataset into the Pipeline

For reproducibility, obtain and store the datasets in the following locations:

1. [**Autonomic Aging: A dataset to quantify changes of cardiovascular autonomic function during healthy aging**](https://physionet.org/content/autonomic-aging-cardiovascular/1.0.0/)  
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

#### ⚙️  **_1.2 Preprocessing and RR Interval Extraction_**

The following subdirectories contain Python scripts for:

- **Preprocessing raw ECG data**  
- **Obtaining HRV from ECG**  
- **Extracting the first 1, 5, 10, and 20 minutes of HRV** into separate *timescale* directories  

---

### 2️⃣ Application of Inclusion Criteria

Subject metadata are provided in different formats:

- `1_hs_data.csv` (renamed from the original `subject-info.csv`) — for the HS group  
- `2_dcm_data.csv` — for the CHF group  

Each dataset requires its own Python script to extract subject IDs meeting the inclusion criteria.

---

#### 🔁 Reproducibility Notes

Refer to the **script descriptions** for detailed instructions on changes needed in the **USER CONFIGURATION** blocks.  

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

#### 🔁 Reproducibility Notes

Before running this stage:

- Review the **USER CONFIGURATION** block within the script.  
- Adjust group labels and timescale directories as necessary.  
- Ensure the preprocessed datasets follow the expected directory hierarchy.

---

### 4️⃣ Statistical Analysis

Statistical testing is conducted via `3_run_statistical_analysis.py`.

This step performs:

- **Normality testing**  
- **Selection of parametric or non-parametric tests**  
- **Effect size computation (Cohen’s d or Cliff’s δ)**  
- **CSV export of group-wise results**

---

#### 🔁 Reproducibility Notes

Before execution:

- Modify paths and group names inside the **USER CONFIGURATION** block.  
- The script is compatible with outputs generated by the nonlinear measure computation step.

---

### 5️⃣ Visualization

This directory contains scripts for visualizing results:

1. **Grouped bar plots** comparing effect sizes of nonlinear measures across short-term timescales.  
2. **3D surface plots** illustrating how histogram resolution influences the performance of the HB AMI across timescales.  

---

#### 📊 Output

Figures are automatically saved in the same directory as their respective scripts,  
following descriptive and reproducible naming conventions.

---


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
