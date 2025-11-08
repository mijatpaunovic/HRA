## Heart Rate Asymmetry Analysis
This repository contains Python code and RR intervals for reproducing results presented in the manuscript titled "Mapping the Heart Rhythm: Leveraging Poincaré Plot Asymmetry to Detect Congestive Heart Failure and Age-related Changes", that is currently under review and authored by [Mijat Paunović](https://orcid.org/0009-0006-4642-4695), [Marko Ćosić](https://orcid.org/0000-0002-4338-0555), [Nikola N. Radovanović](https://orcid.org/0000-0002-6545-2230), [Mirjana M. Platiša](https://orcid.org/0000-0002-0915-2823), and [Nadica Miljković](https://orcid.org/0000-0002-3933-6076).

### Brief Manuscript Overview
This study investigates the ability of various measures to quantify asymmetry in Poincaré plots (PP) derived from Heart Rate Variability (HRV) recordings across different subject groups and short-term timescales. For each timescale (1-, 5-, 10-, and 20-minute HRV segments), the performance of the newly proposed Kernel Density Estimation–based Asymmetry Magnitude Index (KDE AMI) is assessed alongside established asymmetry measures - Histogram-based AMI (HB AMI), Guzik Index (GI), Porta Index (PI), Asymmetric Spread Index (ASI), Slope Index (SI), and Area Index (AI) - in their ability to discriminate between subject groups. All Heart Rate Asymmetry (HRA) measures are benchmarked against the standard (non-HRA) Poincaré plot descriptors, SD1 and SD2.

### Repository Structure
All files necessary to reproduce the results of the study are provided, including the complete codebase, input data, and intermediate outputs. The included HRV recordings result from the preprocessing raw electrocardiogram (ECG) signals used in the study, and therefore require no further modifications. Executing the scripts for specific subject groups involves only a one-line adjustment (specifying which groups are to be compared), as outlined in the description sections at the beginning of each script. The repository is organized as follows:

#### 1. Python code
- `nonlinear_measures.py` - Computes nonlinear measures across short-term timescales for specified subject groups.  
- `statistical_tests.py` - Performs statistical tests to assess the differences between specified groups.

#### 2. Input data (`input_data/`)
- `HRV/` - HRV recordings segmented into 1-, 5-, 10-, and 20-minute intervals for:  
  - Healthy Subjects (HS)  
  - Patients with Congestive Heart Failure (CHF)  
- `IDs/` - CSV files listing subject IDs that satisfy the study inclusion criteria.

#### 3. Results
- `nonlinear_measures/` - Stores the computed indices for all recordings.  
- `statistical_analysis/` - Contains the outputs of statistical tests, including RMDs, p-values, and effect sizes.

### Disclaimer
The Python code is provided without any guarantee and it is not intended for medical purposes.

### License
Unless otherwise stated, shared scripts are free software: anyone can redistribute them and/or modify them under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (optionally) any later version. These programs are distributed in the hope that they will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. For more details, see the GNU General Public License. Anyone accessing this code should have received a copy of the GNU General Public License along with these programs. If not, the license is available at: https://www.gnu.org/licenses/.

Please, report any bugs to the Author listed in the [Contacts](https://github.com/mijatpaunovic/HRA/tree/main?tab=readme-ov-file#contacts) section.

### Contacts
Mijat Paunović (paunovicjata@gmail.com) or Nadica Miljković (e-mail: nadica.miljkovic@etf.bg.ac.rs).

### Funding
Nadica Miljković acknowledges the support from Grant No. 451-03-137/2025-03/200103 funded by the Ministry of Science,Technological Development and Innovation of the Republic of Serbia. Marko Ćosić acknowledges the support from Grant No. 451-03-136/2025-03/20001 funded by the Ministry of Science,Technological Development and Innovation of the Republic of Serbia. Mirjana M. Platiša acknowledges the support from Grant No. 451-03-137/2025-03/200110 funded by the Ministry of Science,Technological Development and Innovation of the Republic of Serbia.

### References
1. Schumann, A., & Bär, K. (2021). Autonomic Aging: A dataset to quantify changes of cardiovascular autonomic function during healthy aging (version 1.0.0). PhysioNet. RRID:SCR_007345. [https://doi.org/10.13026/2hsy-t491](https://doi.org/10.13026/2hsy-t491)
2. Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220. RRID:SCR_007345. [https://doi.org/10.1161/01.cir.101.23.e215](https://doi.org/10.1161/01.cir.101.23.e215)

### How to cite this repository?
If you find Heart Rate Asymmetry index and Python code useful for your own research and teaching class, please cite the following references:
1. Paunović, M., Ćosić, M., Radovanović, N.N., Platiša, M.M., & Miljković, N. (2025). Mapping the Heart Rhythm: Leveraging Poincaré Plot Asymmetry to Detect Congestive Heart Failure and Age-related Changes, under review.
2. Paunović, M., Ćosić, M., Radovanović, N.N., Platiša, M.M., & Miljković, N. (2025). Software for Heart Rate Asymmetry Analysis, (Version 1.1) [Computer software]. Available at [https://github.com/mijatpaunovic/HRA](https://github.com/mijatpaunovic/HRA), Accessed on November 6, 2025. [https://doi.org/10.5281/zenodo.17544604](https://doi.org/10.5281/zenodo.17544604)
