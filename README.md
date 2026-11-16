# Treated dyslipidemia, lipid risk and access to care across Korean districts, 2011-2024

Analysis code for the manuscript

> *Does lipid-lowering treatment in Korea follow lipid risk or access to care? A nationwide district-level analysis of health screening, 2011–2024*

Archived version: Zenodo, https://doi.org/10.5281/zenodo.24281480 (v1.0.0). Released under the MIT license.

## Contents

This repository contains code only. The processed district-year data (master table, analytic panel, expected counts, result tables, adjacency graph and boundary file) are not included; they are available from the author on reasonable request. All source statistics are public (see Data sources).

| Path | What it is |
|---|---|
| `01_스크립트/` | Analysis scripts (below) |
| `04_분석/LIPT/sets_LIPT_*.json`, `config_LIPT_std3.json` | Covariates, expected directions, forced controls and model settings (principal model `std3`; sensitivity versions `s577`, `s2`, `s8`) |
| `04_분석/LIPT/MS/` | Scripts that read the result tables and write every number, table and figure in the manuscript and Supplementary Material, including `content_lipt.py` and `content_jla_lipt.py`, which generate the Methods and Results text (the draft source of the Introduction and Discussion is not included) |

Folder and some column names are in Korean because the source tables are Korean; each script has a header comment describing its inputs and outputs.

## Data sources

All inputs are public, aggregated statistics. No individual-level data are included.

- General health screening attendees (DT_35007_N098, N099) and judgment results by disease, district (N105) and by sex and age group (N106): National Health Insurance Service via KOSIS, 2011-2024. Outcome: attendees in the existing-disease category for dyslipidemia (already diagnosed and on drug treatment); comparison: the suspected-disease category.
- Population by sex and age group: Ministry of the Interior and Safety, resident registration statistics (Changwon 2023 corrected; `population_override`).
- District covariates: KOSIS, the Community Health Survey, National Health Insurance Service screening statistics, Health Insurance Review and Assessment Service specialist counts, the census (tertiary education) and public sports facility surveys. Comparison outcomes (people treated for gastric cancer and for infectious diseases) come from National Health Insurance regional statistics.
- Reference district-year dataset used to verify outcome and denominator values (region-year key): set `ST_REF_SQLITE`.

## Pipeline

Run from the repository root (set `ST_DATA_ROOT`, `ST_FBDZIP_CORRECTED`, `ST_REF_SQLITE` and, for downloading, `KOSIS_KEY`). R jobs are run through `01_스크립트/rslot.sh`, which limits the number of concurrent single-threaded INLA fits.

| Step | Script | Output |
|---|---|---|
| 1 | `99N_fetch_lipt_age_sex.py` | National attendees and treated dyslipidemia by sex and age group |
| 2 | `99L2_build_Estd3_lipt.py` (uses `38_build_Estd_all.py`, `40_region_crosswalk.py`, `50_build_master_panel.py`) | District counts, expected numbers standardized by sex and age among attendees, resident-based expected numbers |
| 3 | `99c_extra_canonical_pool_lipt.py` | Specialists, tertiary education, basic livelihood security (2021-2023 two-sided correction), joined by district code |
| 4 | `80_build_disease_panel_v.py LIPT` (`ST_VER=std3`) | Analytic panel |
| 5 | `81_fit_inla.R LIPT` (`ST_VER=std3`, `ST_GRAPH=04_분석/LIPT/graph_593.graph`, `ST_THREADS=1`; see `04_분석/LIPT/run_std3_chain.sh`) | Principal model, set comparison, 200-subset multiverse, window models |
| 6 | `82L_core_report_nwin.py`, `83_check_report.py`, `85_window_maps.R`, `86_yearly_maps_ehsa.py`, `87_window_grid.py` | Core report, maps and emerging hot spot analysis |
| 7 | `88g_sens_prep.py LIPT std3 INFECT,GCA`, `88g_sens_suite.R` (`GROUP=1..6`), `88h_ppc_varpart.R`, `88k_struct_kh.R` (nb, struct, review), `88k_struct_kh_lipt.R` with `kh_constraints_lipt.R` (kh), `89g_sens_combine.py` | Sensitivity analyses, comparison outcomes, Knorr-Held models, review outputs |
| 8 | `88L_lipt_reverse_posthoc.R`, `88L2_lipt_mpa_precise.R` | Post hoc examination of specialist density; unrounded interval for physical activity |
| 9 | `99L3_lipt_suspect_gap.py` | Treated versus suspected dyslipidemia |
| 10 | `04_분석/LIPT/MS/build/run_all_jla.sh` (`build_refs_lipt.py`, `figs_lipt.py`, `build_jla_lipt.py`, `esm_jla_lipt.py`) | Manuscript, title page, Supplementary Material and figures |

The boundary file is found at `data/boundary/final.shp` by default; set `ST_SHP` to use another path.

## Software

R 4.6.0 with R-INLA 25.10.19, spdep and sf; Python 3.9 with pandas, geopandas, numpy, scipy, matplotlib and python-docx.
