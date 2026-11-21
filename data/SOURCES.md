# Data sources and reuse terms

All series below are either downloaded from Eurostat or the European Commission (DESI), or derived from them. Reuse is permitted with acknowledgement of the source; Eurostat's copyright notice also asks that changes to the data be indicated. Eurostat states that it is not responsible for the reuse or interpretation of its data (see https://ec.europa.eu/eurostat/help/copyright-notice).

| File | Source | Dataset code / table | Last update in source file | Derived? | Used in |
|---|---|---|---|---|---|
| `ICA_27_members_until_2023.xlsx` | Eurostat national accounts, gross value added by detailed industry (NACE Rev. 2), custom selection of ICA industries | nama_10_a64 (custom table 20836965) | Accessed April 2026 | Yes: ICA index compiled by the authors | All clustering analyses |
| `external/estat_rd_e_gerdtot_filtered_en.csv` | Eurostat | RD_E_GERDTOT (gross domestic expenditure on R&D, % of GDP) | 03/11/26 | No (filtered extract) | §4.8 covariates |
| `external/estat_nama_10_pc_filtered_en.csv` | Eurostat | NAMA_10_PC (GDP per capita, CP_EUR_HAB) | 11/11/26 | No (filtered extract) | §4.8 covariates |
| `external/desi-2022-data.csv` | European Commission, Digital Economy and Society Index (DESI) 2022 | DESI dimension and indicator scores | not stated in file | Possibly reformatted; verify against the DESI release | §4.8 covariates |
| `external/nama_10r_2gdp_pps_nuts2.csv` | Eurostat | NAMA_10R_2GDP (GDP per head in PPS, NUTS 2) | 10/02/26 | No | RD analysis |
| `external/demo_r_d2jan_2015_2017.csv` | Eurostat | DEMO_R_D2JAN (population on 1 January, NUTS 2) | 15/11/26 | No | RD analysis |
| `external/isoc_r_iuse_i_nuts2.csv` | Eurostat | ISOC_R_IUSE_I (internet use by individuals, NUTS 2) | 17/04/26 | No | RD analysis |
| `external/isoc_r_broad_h_nuts2.csv` | Eurostat | ISOC_R_BROAD_H (household broadband access, NUTS 2) | 16/06/24 | No | Robustness (if used) |
| `external/nuts2_gdp_pps_index_2015_2017.csv` | Derived by the authors from the Eurostat NAMA_10R_2GDP and DEMO_R_D2JAN files, using `external/compute_regional_gdp_index.py` | — | — | Yes | RD analysis (running variable) |

Reproduce a Eurostat extract by downloading the dataset code above from https://ec.europa.eu/eurostat/databrowser and keeping the same filter. Cite as: Eurostat (year), dataset title and code, accessed [date].
