# esm_jla_lipt.py — J Lipid Atheroscler Supplementary Material(이중 익명·미국식 철자, 2026-11-16, esm_lipt.py에서 전환; 단일 파일: Section S1-S8, 본문 첫 인용 순서) + STROBE(S8). 수치는 결과 CSV에서만(2026-11-12, esm_cogn.py 구조 복제·전면 교체).
#  단일 익명이지만 보충은 저자 정보 없이 제목만. 영국식 철자(TX._emit에서 brit 적용). 표 번호 Table S1…, 그림 Fig. S1.
import os, json, subprocess, pandas as pd
from docx.shared import Cm
import content_jla_lipt as C
from shared_lipt import LABEL, GROUPS
from build_jla_lipt import TX, TITLE as DTITLE, foot_row, read_draft
from american import amer as brit
HERE = os.path.dirname(os.path.abspath(__file__)); MSD = os.path.dirname(HERE); OUT = os.path.join(MSD, "out"); B = os.path.dirname(MSD); RS = os.path.join(B, "results_std3")
N = C.N
f3 = lambda t: f"{t[0]:.3f} ({t[1]:.3f}–{C.fh(t[2]) if (len(t) > 3 and t[3]) else f'{t[2]:.3f}'})"
B1 = "Intervals with a bound shown as 1.000 were classified from unrounded values."
ROBV = [C.EDU, C.IMS, C.MPA]
SH = {C.EDU: "Tertiary education", C.IMS: "Specialists per population", C.MPA: "Moderate or vigorous activity"}
J = TX(cite="bracket")
_NB = [False]
def TF(title, header, rows, foot="", fs=8):
    title = brit(title); header = [brit(h) for h in header]; rows = [[brit(x) for x in r] for r in rows]
    (None if _NB[0] else J.page_break()); _NB[0] = False; J.table_fit(title, header, rows, "", fs_max=fs)
    if foot: foot_row(J, foot, 8, 12)
J.para("<b>Supplementary Material</b>"); J.para(f"Manuscript: {DTITLE}")
J.para("Contents: Section S1 (supplementary methods); Section S2 (covariates, Table S1); Section S3 (panel checks, Table S2); Section S4 (persistence, Fig. S1); Section S5 (windows and COVID-19 period, Table S3); Section S6 (robustness, comparison outcomes and model checks, Tables S4 and S5); Section S7 (post hoc analyses, Table S6); Section S8 (STROBE checklist, Table S7).")
_LK = C._LK; _MT = pd.read_csv(os.path.join(B, "panel_META_LIPT_std3.csv"), encoding="utf-8-sig").set_index("variable")
_imp = lambda v: int(_MT.loc[v, "n_imputed_interp"] + _MT.loc[v, "n_imputed_sgg_mean"] + _MT.loc[v, "n_imputed_year_mean"])
# S1
J.page_break(); J.head("Section S1. Supplementary methods", 2)
SM = [("Outcome and denominator.", f"The national statistics portal publishes, for each year, the number of general health screening attendees and the number placed in each judgement category by district, sex and 5-year age group. Attendees who report a physician diagnosis of dyslipidaemia and current drug treatment are placed in the existing-disease category for dyslipidaemia; attendees with abnormal lipid results and no treatment are placed in the suspected-disease category. District sums of attendees and of treated dyslipidaemia were 99.2–99.9% of national totals in every year. Seven district-years missing in the disease-by-district table were filled from the sum of the sex-by-age table for the same district and year. Sejong was reported separately in only 1 of the 14 years and was treated as unobserved (kept in the neighbourhood graph), leaving {N['n_districts']} districts and {N['n_rows']:,} district-years."),
      ("Standardisation.", f"Expected numbers E = Σ(attendees in sex s and age a) × (national share treated in s and a), with 15 age groups (19 years or younger, 5-year groups from 20–24 to 80–84 years, and 85 years or older), rescaled each year to the national number treated. The ratio of standardised to crude expected numbers ranged from {N['estd_ecrude'][0]:.2f} to {N['estd_ecrude'][1]:.2f}. A resident-based alternative applied the same national shares to the resident population; its district ratios correlated with the attendee-based ratios at Spearman's ρ {N['rho_std_pop']:.2f}."),
      ("Lipid-testing schedule.", f"From 2018 the lipid panel in general screening moved from every 2 years to every 4 years for most adults. The national share treated rose without a step through 2018 ({N['pos_y'][2017]:.2f}% in 2017, {N['pos_y'][2018]:.2f}% in 2018), and the calendar windows (2011–2017, 2018–2024) were chosen so that neither crosses the change."),
      ("Covariates.", "Community Health Survey indicators are age-standardised district estimates. Specialist density counts internal-medicine specialists working in the district. Uptake is the share of people invited to general screening who attended. Basic livelihood security values for 2021–2023 that were below 20% or above five times the mean of 2020 and 2024 in the same district (33 district-years in 11 cities divided into general districts, where the source table had collapsed or inflated values) were set to missing before filling."),
      ("Models.", f"Software: R 4.6.0 with R-INLA; Python 3.9 for data preparation, emerging hot spot analysis and figures. Negative binomial likelihood, chosen because its widely applicable information criterion (WAIC) for the forced-controls model ({_LK['nbinomial']:,.1f}) was lower than that of the Poisson model ({_LK['poisson']:,.1f}). District effect: BYM2 on an audited 593-edge contact graph of 229 districts with island districts linked to the nearest mainland district; penalised-complexity priors P(σ > 0.5) = 0.01 and P(φ < 0.5) = 2/3. Year effects: first-order random walk plus independent effects. The covariate set was fixed in advance by the author; a smaller lipid-risk-factor set had a slightly lower WAIC ({N['waic_rulebest']:,.1f} vs {N['waic_main']:,.1f}) and gave the same null results for lipid risk factors. Regions for region-specific slopes: Capital (Seoul, Incheon, Gyeonggi), Chungcheong, Honam, Yeongnam and Gangwon–Jeju."),
      ("Treated versus suspected dyslipidaemia.", "Suspected dyslipidaemia used the suspected-disease category of the same screening programme, standardised in the same way within each window because its definition changed in 2018. District ratios were pooled over 2011–2024; G, the log of the treated ratio over the suspected ratio, was tested for spatial autocorrelation with Moran's I (999 permutations)."),
      ("Post hoc analyses.", "The decomposition into district means and two-way-centred deviations was planned. After the principal results were seen, specialist density, associated against its expected direction, was examined with a single-covariate model, removal of physician density, tertiary education and urban share, one-way decomposition into district means and deviations, addition of unmet need and the shares of attendees treated for hypertension or diabetes, and replacement by, or addition of, log specialists per km².")]
for h, t in SM: J.para(f"<b>{h}</b> {t}")
# S2
J_SETS = json.load(open(os.path.join(B, "sets_LIPT_std3.json"), encoding="utf-8"))
DIRN = {k: v.split()[0].replace("-", "−") for k, v in J_SETS["expected_direction"].items()}
MAPV = {_MT.loc[v, "source_column"]: v for v in _MT.index}
DIR = {MAPV[k]: d for k, d in DIRN.items() if k in MAPV}
SRC = {"kchs": "KCHS", "chk": "NHIS screening", "eloc": "KOSIS", "fac": "MCST facilities", "nhis": "NHIS", "ext": "KOSIS"}
EXTSRC = {"ext__pop80_share": "Population registry", "ext__tertiary_educated_share": "Census", "ext__basic_livelihood_rate": "KOSIS", "ext__im_specialists_per100k": "HIRA", "chk__수검률": "NHIS screening"}
def unit(l): return "Std. rate, %" if "(SR %)" in l else ("per 100,000" if ("per 100k" in l or "per 100,000" in l) else ("per 1,000" if ("per 1000" in l or "per 1,000" in l) else ("ratio" if "per 100 women" in l else "%")))
rows = []
for g, vs in GROUPS:
    rows.append(["__H__", g])
    for v in vs:
        m = _MT.loc[v]; sc = str(m.source_column); src = EXTSRC.get(sc, SRC.get(sc.split("__")[0], sc.split("__")[0]))
        rows.append([f"  {LABEL[v]}", unit(str(m.label_en)), src, f"{int(m.obs_year_min)}–{int(m.obs_year_max)}", ("NA" if m.role == "forced" else DIR[v]), f"{_imp(v):,}"])
assert all(DIR.get(v) for g, vs in GROUPS[:-1] for v in vs)
J.page_break(); J.head("Section S2. Covariates", 2); _NB[0] = True
TF("Table S1. Source, observed years, expected direction and filled cells for each covariate", ["Covariate", "Unit", "Source", "Years", "Direction", "Filled"], rows,
   f"HIRA, Health Insurance Review and Assessment Service; KCHS, Community Health Survey; KOSIS, Korean Statistical Information Service; MCST, Ministry of Culture, Sports and Tourism; NHIS, National Health Insurance Service; NA, no direction specified (forced control). Filled, district-years filled by within-district interpolation, district mean or year mean, out of {N['n_rows']:,}; the 33 implausible basic livelihood values were replaced by within-district interpolation before panel construction and are not counted here. Comparison outcomes (patients treated for gastric cancer and for infectious disease, national health insurance statistics) and negative-control exposures (hit-and-run traffic accidents, fires per 10,000 residents, household waste recycling rate; KOSIS) covered 2011–2024.")
# S3
J.page_break(); J.head("Section S3. Panel checks before modelling", 2); _NB[0] = True
rows = [["Year means differ twofold or more", "Largest/smallest positive yearly mean ≥2", "Outcome and expected numbers (national share treated rose 1.7% to 12.6%); standardised columns with yearly means near 0", "Real trend absorbed by yearly national shares; retained"],
        ["Missing source years", "No observation in a year", "Single-person households before 2015", "Filled with district means; perturbation sensitivity"],
        ["Ratio-type column above 100", "Maximum >100 for a rate or ratio", "Sex ratio (men per 100 women)", "Retained (definition)"],
        ["Missing district-years", "No observation", f"{sum(json.load(open(os.path.join(RS, 'S41_imputed_cells.json'))).values()):,} cells", "Filled within districts; perturbation sensitivity"],
        ["Outcome reconstruction", "District sums equal national totals", "99.2–99.9% of national totals in all 14 years; 7 blank cells filled from sex-by-age sums", "None"],
        ["Implausible source value", "2021–2023 value <20% or >5 times adjacent mean", "Basic livelihood security, 33 cells", "Set to missing and interpolated"],
        ["Collinearity", "Variance inflation factor ≥10", "None (maximum 6.99, share aged 80+)", "None"]]
TF("Table S2. Panel checks: rules, thresholds, flags and actions", ["Check", "Threshold", "Flags in this panel", "Action"], rows, f"Checks were run on the analytic panel ({N['n_rows']:,} district-years) before any covariate model was fitted.", fs=8)
# S4
_T1 = N["T1"]; _eh = N["ehsa"]
J.page_break(); J.head("Section S4. Persistence of the district pattern", 2)
J.para(f"The 10th–90th percentile range of district treatment ratios was {_T1['W1_2011-17']['sir_p10']:.2f}–{_T1['W1_2011-17']['sir_p90']:.2f} in 2011–2017 and {_T1['W2_2018-24']['sir_p10']:.2f}–{_T1['W2_2018-24']['sir_p90']:.2f} in 2018–2024. "
       f"The window models identified {N['win_hot']['W1_2011-17']} hot and {N['win_cold']['W1_2011-17']} cold spots in 2011–2017 and {N['win_hot']['W2_2018-24']} hot and {N['win_cold']['W2_2018-24']} cold spots in 2018–2024 (equal counts in each window, checked against the classification output); {N['hot_all_windows']} districts were hot spots and {N['cold_all_windows']} cold spots in both. Kendall's W of annual district rankings of empirical Bayes-smoothed ratios was {N['kendall_W']:.2f}. "
       f"Emerging hot spot analysis classified {_eh['Persistent hot']} districts as persistent, {_eh['Consecutive hot']} as consecutive, {_eh['Intensifying hot']} as intensifying and {_eh['Diminishing hot']} as diminishing hot spots, and {_eh['Persistent cold']} as persistent, {_eh['Consecutive cold']} as consecutive and {_eh['Sporadic cold']} as sporadic cold spots; {_eh['No pattern']} districts showed no pattern, and the remaining districts fell into other categories (Fig. S1A).")
_pp = J.para(""); _pp.add_run().add_picture(os.path.join(HERE, "figs", "FigS1.png"), width=Cm(16))
J.para("<b>Fig. S1.</b> (A) Emerging hot spot analysis (Getis–Ord Gi* with Mann–Kendall trend) of empirical Bayes-smoothed treatment ratios, 2011–2024; numbers of districts in parentheses. (B) Number of calendar windows (2011–2017, 2018–2024) in which each district was a residual hot or cold spot in the principal model. Grey, no data (Sejong).")
# S5
WI = pd.read_csv(os.path.join(RS, "S4_window_IRR.csv")).set_index(["cov", "window"]); IT = pd.read_csv(os.path.join(RS, "S4_interaction.csv")).set_index("cov")
CV = pd.read_csv(os.path.join(RS, "S5_covid.csv")); CVX = CV[CV.term == "var_x_post"].set_index("cov")
rows = []
for g, vs in GROUPS[:-1]:
    rows.append(["__H__", g])
    for v in vs: rows.append([f"  {LABEL[v]}"] + [f3(tuple(WI.loc[(v, w), ["IRR", "lo", "hi", "cred"]])) for w in ("W1_2011-17", "W2_2018-24")] + [f3(tuple(IT.loc[v, ["IRR_ratio", "lo", "hi", "cred"]])), f3(tuple(CVX.loc[v, ["IRR", "lo", "hi", "cred"]]))])
J.page_break(); J.head("Section S5. Calendar windows and the COVID-19 period", 2); _NB[0] = True
TF("Table S3. Rate ratios for the hypothesis covariates by calendar window and interactions with the window and with the COVID-19 period", ["Covariate", "2011–2017", "2018–2024", "Ratio, 2018–2024 vs 2011–2017", "Interaction with 2020 onwards"], rows,
   "Rate ratio per 1 standard deviation (95% credible interval). Window columns: principal model structure fitted separately to each window with all forced controls. Ratio: window interaction in a single model. Interaction with 2020 onwards: ratio of the rate ratio from 2020 onwards to that before 2020. " + B1, fs=7)
# S6
LO = N["leaveout"]
def rrow(lab, fn): return [lab] + [fn(v) for v in ROBV]
rows = [rrow("Subsets credible / same sign, %", lambda v: f"{100*N['mv'][v]['cred_frac']:.0f} / {100*N['mv'][v]['sign_agree']:.0f}"),
        rrow(f"Alternative fits retained, including leave-one-out (of {N['retention'][C.EDU]['n_specs']})", lambda v: f"{N['retention'][v]['kept']}/{N['retention'][v]['n_specs']}"),
        rrow("Leave-one-province retained", lambda v: f"{LO[('province', v)][1]}/{LO[('province', v)][0]}"),
        rrow("Leave-one-year retained", lambda v: f"{LO[('year', v)][1]}/{LO[('year', v)][0]}"),
        rrow("Perturbed filled values, pooled RR", lambda v: f"{N['rubin'][v]['IRR_pooled']:.3f} ({N['rubin'][v]['lo']:.3f}–{N['rubin'][v]['hi']:.3f})"),
        rrow("Perturbed filled values, credible fits of 20", lambda v: f"{N['rubin'][v]['n_cred']}"),
        rrow("Eight age bands in expected numbers", lambda v: f3(N["sens_main"]["s8"][v])),
        rrow("Share aged 80+ omitted", lambda v: f3(N["sens_main"]["s2"][v])),
        rrow("Queen contiguity graph", lambda v: f3(N["sens_main"]["s577"][v])),
        rrow("Expected numbers from residents", lambda v: f"{N['epop'][v][0]:.3f} ({N['epop'][v][1]:.3f}–{N['epop'][v][2]:.3f})"),
        rrow("Knorr-Held type I", lambda v: f3(N["s43"][("KH_typeI", v)])),
        rrow("Knorr-Held type III", lambda v: f3(N["s43"][("KH_typeIII", v)])),
        rrow("District mean (between)", lambda v: f3(N["bw"][v + "__between"])),
        rrow("Two-way-centred deviation (within)", lambda v: f3(N["bw"][v + "__within"])),
        rrow("Gastric cancer care (comparison outcome)", lambda v: f3(N["nco"][("GCA", v)])),
        rrow("Infectious disease care (comparison outcome)", lambda v: f3(N["nco"][("INFECT", v)])),
        rrow("ΔWAIC, region-specific vs common slope", lambda v: f"{N['region_dwaic'][v]:+.1f}"),
        rrow("E-value, point / limit", lambda v: f"{N['evalue'][v]['E_point']:.2f} / {N['evalue'][v]['E_limit']:.2f}")]
J.page_break(); J.head("Section S6. Robustness, comparison outcomes and model checks", 2); _NB[0] = True
TF("Table S4. Robustness of the three subset-stable covariates", ["Analysis"] + [SH[v] for v in ROBV], rows,
   "RR, rate ratio per 1 standard deviation (95% credible interval). Retained = credible with the principal-model sign. Alternative fits: forced controls smoothed; Poisson with observation-level effect; second-order random-walk and first-order autoregressive year effects; province-by-year effect; Spatial+-type adjustment; unlagged fits restricted to the lag years; 1-year and 2-year lags; leave-one-province and leave-one-year fits; extreme values winsorised; 3-year moving-average survey covariates; even and odd years. With expected numbers from residents the activity interval is rounded; its posterior probability of RR above 1 was below 0.025. " + B1, fs=7.5)
NCN = {"hit_and_run_rate": "Hit-and-run accidents", "fires_per_10000": "Fires per 10,000", "waste_recycling_rate": "Household waste recycling"}
rows = [["__H__", "Negative-control exposures (added one at a time)"]] + [[f"  {NCN[k]}", f"{v['IRR']:.3f} ({v['lo']:.3f}–{v['hi']:.3f})"] for k, v in N["negctl"].items()]
rows += [["__H__", "Model checks"], ["  95% posterior predictive coverage, %", f"{100*N['ppc']['coverage95']:.1f}"], ["  50% posterior predictive coverage, %", f"{100*N['ppc']['coverage50']:.1f}"],
         ["  PIT Kolmogorov–Smirnov P", f"{N['ppc']['pit_ks_p']:.2g}"], ["  Held-out 2024 coverage (95%), %", f"{100*N['oos']['coverage95']:.1f}"],
         ["  Residual Moran's I (permutation P)", f"{N['moran_resid']:.2f} ({N['moran_resid_p']:.2f})"],
         ["  Linear predictor variance, structured spatial, %", f"{100*N['varpart']['spatial_structured']['share_of_linear_predictor_var']:.1f}"],
         ["  Linear predictor variance, hypothesis covariates, %", f"{100*N['varpart']['fixed_hypothesis']['share_of_linear_predictor_var']:.1f}"]]
TF("Table S5. Negative-control exposures and model checks", ["Analysis", "Result"], rows, "Rate ratios per 1 standard deviation (95% credible interval). PIT, probability integral transform. Variance shares are the variance of each linear-predictor component divided by the variance of the full linear predictor.")
# S7
V = C.IMS; S46 = N["s46"]
rows = [["Principal model", f3((N["main"][V]["IRR"], N["main"][V]["lo"], N["main"][V]["hi"], True))],
        ["Unmet need and treated hypertension and diabetes added", f3(S46[("P1_plus_access_dx", V)])],
        ["Single covariate with forced controls", f3(S46[("P2_alone", V)])],
        ["Physician density removed", f3(S46[("P3a_drop_physicians", V)])],
        ["Tertiary education removed", f3(S46[("P3b_drop_tertiary", V)])],
        ["Physician density and urban share removed", f3(S46[("P3c_drop_physicians_urban", V)])],
        ["District mean (one-way between)", f3(S46[("P4_between_within", V + "__B")])],
        ["Deviation from district mean (one-way within)", f3(S46[("P4_between_within", V + "__W")])],
        ["Specialists per km² (log) replacing per population", f3(S46[("P5_per_area", "spec_per_km2_log")])],
        ["Per population, with per km² added", f3(S46[("P5b_both", V)])],
        ["Per km² (log), with per population added", f3(S46[("P5b_both", "spec_per_km2_log")])]]
rows += [["__H__", "Region-specific slopes (per population)"]] + [[f"  {r.replace('_', ' and ')}", f3(N["region_slope"][f"{V}__{r}"])] for r in ("Capital", "Chungcheong", "Gangwon_Jeju", "Honam", "Yeongnam")]
J.page_break(); J.head("Section S7. Post hoc analyses", 2); _NB[0] = True
TF("Table S6. Examination of internal-medicine specialist density, associated against its expected direction", ["Analysis", "RR (95% CrI)"], rows,
   f"Rate ratios per 1 standard deviation (95% credible interval). Expected direction positive. All rows except the principal model and the region-specific slopes were added after the results were seen. Specialists per population correlated with the share aged 80 years or older (r {N['ims_pop80_r']:.2f}), urban share (r {N['ims_urban_r']:.2f}) and physician density (r {N['ims_phys_r']:.2f}).")
# S8 STROBE
MH = [h for h, _ in C.METHODS]; RH = [h for h, _ in C.RESULTS]; assert MH[0].startswith("Design") and MH[2] == "Covariates" and RH[0].startswith("Treated")
M_ = lambda *i: "Materials and Methods, " + " and ".join(str(x) for x in i); R_ = lambda *i: "Results, " + " and ".join(str(x) for x in i)
CK = [("Title and abstract", "1", "Title; Abstract"), ("Background/rationale", "2", "Introduction"), ("Objectives", "3", "Introduction, final paragraph"), ("Study design", "4", M_(1)), ("Setting", "5", M_(1)),
      ("Participants", "6", M_(1) + " (district aggregates; ecological)"), ("Variables", "7", M_(2, 3) + "; Section S2"), ("Data sources/measurement", "8", "Materials and Methods; Section S1"),
      ("Bias", "9", M_(5) + "; Sections S3, S6 and S7"), ("Study size", "10", M_(1) + f" ({N['n_districts']} districts)"), ("Quantitative variables", "11", M_(3)),
      ("Statistical methods", "12", M_(4, 5)), ("Participants (flow)", "13", "Not applicable (aggregate district data)"), ("Descriptive data", "14", R_(1) + "; Table 1"), ("Outcome data", "15", R_(1)),
      ("Main results", "16", R_(2, 3) + "; Table 2; Fig. 1"), ("Other analyses", "17", "Results, 4–6; Fig. 2; Sections S4–S7"),
      ("Key results", "18", "Discussion, first paragraph"), ("Limitations", "19", "Discussion, strengths and limitations paragraph"), ("Interpretation", "20", "Discussion"), ("Generalisability", "21", "Discussion, strengths and limitations paragraph"),
      ("Funding", "22", "Title page (Funding)")]
J.page_break(); J.head("Section S8. STROBE checklist", 2)
J.table_fit("Table S7. STROBE checklist for this ecological study", ["Item", "No.", "Where reported"], [[a, b, c] for a, b, c in CK], "", fs_max=9)
foot_row(J, "STROBE, Strengthening the Reporting of Observational Studies in Epidemiology.", 8, 12)
ps = os.path.join(OUT, "Supplementary_Material_JLA_LIPT.docx"); J.doc_title = "Supplementary Material"; J.save(ps)
subprocess.run(["/opt/homebrew/bin/soffice", "--headless", "-env:UserInstallation=file:///tmp/lo_lipt_esm_jla", "--convert-to", "pdf", "--outdir", OUT, ps], check=True, capture_output=True)
print("saved", os.path.basename(ps))
