# content_lipt.py — 31호 LIPT  원고의 Methods·Results 문장(수치는 numbers_lipt에서만, 2026-11-12, content_cogn.py 구조 복제).
#  인용 = [@key] 또는 [@web:...]; 번호식. 단독 저자 → 1인칭 금지. 영국식 철자(dyslipidaemia), 결과 절 해석 금지.
#  제목 쌍점 금지, 시리즈 제목 틀 반복 금지.
from numbers_lipt import load, ROB, RS, EDU, IMS, MPA
import os, pandas as pd
N = load()
def fh(x): return f"{x:.4f}" if (f"{x:.3f}" == "1.000" and f"{x:.4f}" != "1.0000") else f"{x:.3f}"   # 1을 가까스로 배제하는 상한은 4자리
def ci(v, src=None):
    r = (src or N["main"])[v]; return f"RR {r['IRR']:.3f}; 95% CrI {r['lo']:.3f}–{fh(r['hi'])}"
def tci(t): return f"RR {t[0]:.3f}; 95% CrI {t[1]:.3f}–{fh(t[2]) if len(t) > 3 and t[3] else f'{t[2]:.3f}'}"
M = N["main"]; T1 = N["T1"]; G_ = N["gap"]["all_2011-24"]
S43 = lambda a, v: N["s43"][(a, v)]
dW = lambda a: N["s43_waic"][a] - N["waic_main"]
NCO = lambda o, v: N["nco"][(o, v)]
S46 = lambda a, v: N["s46"][(a, v)]
NC = lambda v: (N["negctl"][v]["IRR"], N["negctl"][v]["lo"], N["negctl"][v]["hi"])
SC = lambda s, v: N["sens_main"][s][v]
RSL = lambda v, r: N["region_slope"][f"{v}__{r}"]
EN = {"전라남도": "South Jeolla", "경상북도": "North Gyeongsang", "경상남도": "South Gyeongsang", "충청남도": "South Chungcheong", "전라북도": "North Jeolla",
      "강원도": "Gangwon", "부산시": "Busan", "충청북도": "North Chungcheong", "대구시": "Daegu", "경기도": "Gyeonggi", "서울시": "Seoul", "인천시": "Incheon",
      "광주시": "Gwangju", "울산시": "Ulsan", "대전시": "Daejeon", "세종시": "Sejong", "제주도": "Jeju"}
def sidos(d, n):
    l = [f"{EN.get(k, k)} ({v})" for k, v in list(d.items())[:n]]; return ", ".join(l[:-1]) + " and " + l[-1]
KH = ("KH_typeI", "KH_typeII", "KH_typeIII", "KH_typeIV")
TITLE = "Treated dyslipidaemia among Korean health-screening attendees is more common in more educated districts, with no clear link to lipid risk factors"
RUNNING = "Geography of treated dyslipidaemia"
assert ":" not in TITLE and "229" not in TITLE and "standardi" not in TITLE.lower()
KEYWORDS = "Dyslipidaemias; Hydroxymethylglutaryl-CoA reductase inhibitors; Health services accessibility; Educational status; Spatial analysis; Republic of Korea"
HIGHLIGHTS = ["Treated dyslipidaemia among screening attendees clustered in Korea's capital region",
              "Its map differed from the map of untreated suspected dyslipidaemia",
              "More educated districts had more treated dyslipidaemia across space–time models",
              "Obesity, smoking, drinking and walking showed no credible district-level association",
              "Specialists per population ran against expectation, possibly a denominator effect"]
assert 3 <= len(HIGHLIGHTS) <= 5 and all(len(h) <= 85 for h in HIGHLIGHTS), [len(h) for h in HIGHLIGHTS]
assert 3 <= len(KEYWORDS.split(";")) <= 7
_LK = pd.read_csv(os.path.join(RS, "S1_likelihood.csv")); _LK = _LK[_LK.set == "REF_forced_only"].set_index("family").WAIC
_FAM = pd.read_csv(os.path.join(RS, "S3_main_fit.csv")).family.iloc[0]
assert _FAM == "nbinomial" and _LK["nbinomial"] < _LK["poisson"] and abs(_LK["nbinomial"] - N["waic_forced"]) < 0.05
NHYP = N["n_hyp"]; EXP_CHANCE = 0.05 * NHYP; assert NHYP == 11
SUP = {"methods": 1, "covariates": 2, "checks": 3, "maps": 4, "windows": 5, "specs": 6, "posthoc": 7, "strobe": 8}
def sup(k): return f"Supplementary Section S{SUP[k]}"
_pc = lambda v: f"{100*N['mv'][v]['cred_frac']:.0f}%"
ALT = N["retention"]; LO = N["leaveout"]
NULLV = ["screening_uptake", "obesity_rate", "high_risk_drinking_rate", "current_smoking_rate", "walking_practice_rate", "public_sports_facilities_per_100k",
         "basic_livelihood_rate", "single_person_household_share"]
BEST = min(KH, key=lambda a: N["s43_waic"][a])
_EPP = float(pd.read_csv(os.path.join(RS, "S10_offset_sensitivity_IRR.csv")).set_index("cov").loc[MPA, "P_gt1"]); assert _EPP < 0.025
Y0, Y1 = N["pos_y"][2011], N["pos_y"][2024]

METHODS = [
("Design, outcome and population",
 f"This ecological study used the general health screening programme of the National Health Insurance Service, which covers nearly the whole population and invites adults every 2 years [@cheolseong2017data]. The screening judgement places attendees who report a physician diagnosis of dyslipidaemia and current drug treatment in a separate category of existing disease; the annual number of attendees in this category was the outcome, here called treated dyslipidaemia. Numbers of attendees and of people with treated dyslipidaemia by district, sex and age group (19 years or younger, 5-year groups from 20–24 to 80–84 years, and 85 years or older) for 2011–2024 were taken from the national statistics portal [@web:kosis2026screening]. Districts were harmonised to {N['n_districts']} units ({N['n_rows']:,} district-years); Sejong, reported separately in only 1 year, was treated as unobserved ({sup('methods')})."),
("Age and sex standardisation",
 f"Expected numbers were obtained by indirect standardisation: the national share with treated dyslipidaemia in each sex and age group was applied to the attendees in each district and rescaled each year to the national total [@inskip1983methods]. Observed over expected numbers gives the standardised treatment ratio. With attendees, rather than residents, as the denominator, the ratio describes treatment among people who attended screening. Sex entered the analysis through standardisation; sex-specific models were not possible because district covariates are not reported by sex, and sex is reported following the Sex and Gender Equity in Research (SAGER) guidelines [@heidari2016sex]. Expected numbers from attendees ranged from {N['estd_ecrude'][0]:.2f} to {N['estd_ecrude'][1]:.2f} times the crude expectation."),
("Covariates",
 f"The spatial pattern was first described with models containing forced controls only. Eleven district characteristics and their expected directions were then fixed before any covariate model was fitted, in three groups. Care reach and selection: internal-medicine specialists per 100,000 population (expected positive), health-screening uptake (negative, because higher uptake brings in healthier attendees) and the share of adults with tertiary education (positive, because education is associated with lipid testing [@marcus2021unmet]). Lipid risk factors: obesity, high-risk drinking and current smoking (positive), and walking, moderate-or-vigorous physical activity and public sports facilities per 100,000 (negative, because exercise improves blood lipids [@kodama2007effect; @smart2025effect]); behavioural rates came from the Community Health Survey [@kang2015korea]. Deprivation and household: basic livelihood security receipt and single-person households (negative, because poorer people are less adherent to statins [@wallachkildemoes2013adherence] and living alone may reduce support for care). Five controls were forced into every model: urban population share, physicians per 1,000, sex ratio, fiscal autonomy and the share aged 80 years or older. Covariates were standardised to 1 standard deviation (SD); missing years were filled by within-district interpolation, or by district or year means where a district had no observations; erroneous 2021–2023 values of basic livelihood receipt in 33 district-years were set to missing before filling ({sup('covariates')}; checks in {sup('checks')})."),
("Statistical analysis",
 f"The likelihood (Poisson or negative binomial) was chosen by the lower widely applicable information criterion (WAIC) of the forced-controls model. Models had an offset of log expected numbers, a Besag–York–Mollié 2 (BYM2) district effect with penalised-complexity priors [@riebler2016intuitive; @simpson2017penalising] and random-walk and independent year effects, fitted by integrated nested Laplace approximation [@rue2009approximate] in R [@web:rcore2026]. Rate ratios (RRs) per 1 SD are reported with 95% credible intervals (CrIs); an association was credible when the interval excluded 1. RRs are mutually adjusted ecological associations, not causal effects [@morgenstern1995ecologic]. Intervals were not adjusted for multiplicity; as a rough frequentist analogy, about {EXP_CHANCE:.2f} of the {NHYP} associations would exclude 1 by chance if all were null. Sensitivity to covariate selection was assessed with 200 random covariate subsets [@steegen2016increasing]; a covariate was subset-stable if credible in at least 75% of the subsets containing it, with the same sign in at least 95%. Residual hot and cold spots had a posterior probability of a residual spatial RR above 1 of more than 0.95 or less than 0.05, for the whole period and two windows (2011–2017, 2018–2024) that do not cross the 2018 change in the lipid-testing schedule."),
("Sensitivity and prespecified secondary analyses",
 f"Knorr-Held type I–IV space–time interactions were added [@knorrheld2000bayesian]; subset-stable covariates were split into district means and within-district deviations [@bell2015explaining]; the model was refitted in each window; and expected numbers were recomputed from the resident population. Further specifications varied the likelihood, time effects, priors, neighbourhoods, age bands, forced controls, spatial confounding adjustment [@dupont2022spatial], lags, left-out provinces or years and filled values ({sup('specs')}). District numbers of people treated for gastric cancer and for infectious disease, modelled in the same way, served as comparison outcomes, and district rates of hit-and-run accidents, fires and household waste recycling, added one at a time, as negative-control exposures [@lipsitch2010negative]; E-values quantified the confounding needed to explain associations [@vanderweele2017sensitivity]. A secondary analysis fixed in advance compared each district's treatment ratio with its standardised ratio of suspected dyslipidaemia, the screening category of attendees whose lipid tests were abnormal without treatment, using Spearman correlation and the spatial autocorrelation of the log ratio between them. After the results were seen, an association against the expected direction was examined post hoc with single-covariate models, removal of related covariates, district-mean and within-district parts, and specialist density per area."),
("Ethics and reporting",
 "The institutional review board of Hongik University approved the study and waived informed consent because only published aggregate statistics were used. The study follows the Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement [@vonelm2007strengthening] (" + sup('strobe') + ")."),
]

RESULTS = [
("Treated dyslipidaemia among attendees",
 f"Over 2011–2024, {N['exam_total']/1e6:.1f} million screening attendances included {N['cases_total']:,} attendances with treated dyslipidaemia (Table 1); people screened in several years contribute more than once. The crude share rose steadily from {Y0:.1f}% in 2011 to {Y1:.1f}% in 2024, without a step at the 2018 change in the testing schedule."),
("Spatial pattern",
 f"Moran's I of observed log ratios was {N['moran_pooled']:.2f} pooled over years and {N['moran_year_min']:.2f}–{N['moran_year_max']:.2f} annually; the BYM2 spatial fraction was {N['phi'][0]:.2f} (95% CrI {N['phi'][1]:.2f}–{N['phi'][2]:.2f}). Residual RRs ranged from {N['rr_min']:.2f} to {N['rr_max']:.2f}, with {N['n_hot']} hot spots, mainly in {sidos(N['hot_by_sido'], 4)}, and {N['n_cold']} cold spots, mainly in {sidos(N['cold_by_sido'], 4)} (Fig. 1A). The capital region held {N['hot_capital']} hot spots and {N['cold_capital']} cold spot. In both windows, {N['hot_all_windows']} districts were hot spots and {N['cold_all_windows']} cold spots, and district rankings were stable (Kendall's W {N['kendall_W']:.2f}) ({sup('maps')}). The structured spatial effect accounted for {100*N['varpart']['spatial_structured']['share_of_linear_predictor_var']:.1f}% of the variance of the linear predictor and all covariates, including forced controls, for {100*N['varpart']['fixed_covariates']['share_of_linear_predictor_var']:.1f}%."),
("District correlates",
 f"The negative binomial likelihood was selected (WAIC {_LK['nbinomial']:,.1f} vs {_LK['poisson']:,.1f}). Adding the {NHYP} covariates did not lower WAIC ({N['waic_main']:,.1f} vs {N['waic_forced']:,.1f} with forced controls only). Three covariates were credible, and the same three were subset-stable (Table 2). Treated dyslipidaemia was higher with more tertiary education ({ci(EDU)}) and lower with more moderate-or-vigorous activity ({ci(MPA)}). Against the expected direction, it was lower with more internal-medicine specialists per population ({ci(IMS)}). Tertiary education, activity and specialist density were credible in {_pc(EDU)}, {_pc(MPA)} and {_pc(IMS)} of the covariate subsets containing them. Obesity ({ci('obesity_rate')}), smoking, drinking, walking ({ci('walking_practice_rate')}), sports facilities, screening uptake, basic livelihood receipt and single-person households were not credibly associated. Of the negative-control exposures, fires were credibly associated ({tci(NC('fires_per_10000'))})."),
("Space–time models and sensitivity analyses",
 f"All four interaction types fitted better than the principal model (ΔWAIC {dW('KH_typeIII'):,.0f} to {dW('KH_typeII'):,.0f}, type II best). Tertiary education remained credible in all four types, in both windows and with resident-based expected numbers, but not with 1-year ({tci(N['s41'][('E1_lag1', EDU)])}) or 2-year lagged covariates (2011–2017 {tci(N['win_irr'][(EDU, 'W1_2011-17')])}; 2018–2024 {tci(N['win_irr'][(EDU, 'W2_2018-24')])}) (Fig. 2; {sup('windows')}). In the planned decomposition, education was positively associated between districts ({tci(N['bw'][EDU + '__between'])}) and inversely within districts over time ({tci(N['bw'][EDU + '__within'])}). Moderate-or-vigorous activity was not credible in types II–IV or in either window, and specialist density was not credible in types II and IV or in either window; walking was associated against the expected direction in 2018–2024 only ({tci(N['win_irr'][('walking_practice_rate', 'W2_2018-24')])}), and {N['n_win_int']} of the {NHYP} covariates had credible interactions with calendar window. Across {ALT[EDU]['n_specs']} alternative specifications, tertiary education was credible in {ALT[EDU]['kept']}, specialist density in {ALT[IMS]['kept']} and activity in {ALT[MPA]['kept']}; with filled values perturbed 20 times, the three were credible in {N['rubin'][EDU]['n_cred']}, {N['rubin'][IMS]['n_cred']} and {N['rubin'][MPA]['n_cred']} of 20 fits. Tertiary education stayed credible when each province ({LO[('province', EDU)][1]} of {LO[('province', EDU)][0]}) or year ({LO[('year', EDU)][1]} of {LO[('year', EDU)][0]}) was left out. E-values were {N['evalue'][EDU]['E_point']:.2f} for education, {N['evalue'][IMS]['E_point']:.2f} for specialists and {N['evalue'][MPA]['E_point']:.2f} for activity ({sup('specs')}). With expected numbers from residents, education remained credible ({tci(N['epop'][EDU])}), activity stayed at the margin (RR {N['epop'][MPA][0]:.3f}; posterior probability of RR above 1, {_EPP:.3f}) and specialists were not credible ({tci(N['epop'][IMS])}). In the comparison outcomes, education had RRs of {NCO('INFECT', EDU)[0]:.3f} (infectious disease) and {NCO('GCA', EDU)[0]:.3f} (gastric cancer) and specialists {NCO('INFECT', IMS)[0]:.3f} and {NCO('GCA', IMS)[0]:.3f}. Residual Moran's I was {N['moran_resid']:.2f}; 95% predictive intervals covered {100*N['oos']['coverage95']:.1f}% of 2024 numbers held out with covariates known, and the probability integral transform indicated imperfect calibration."),
("Association against the expected direction",
 f"The inverse association of specialist density persisted alone ({tci(S46('P2_alone', IMS))}) and without physician density and urban share ({tci(S46('P3c_drop_physicians_urban', IMS))}). In a one-way split it lay in district means ({tci(S46('P4_between_within', IMS + '__B'))}) and not in within-district changes ({tci(S46('P4_between_within', IMS + '__W'))}), whereas neither part was credible in the planned two-way decomposition ({tci(N['bw'][IMS + '__between'])} between), and it was confined to the capital region ({tci(RSL(IMS, 'Capital'))}) and Chungcheong ({tci(RSL(IMS, 'Chungcheong'))}). Specialist density per area was positively associated, alone ({tci(S46('P5_per_area', 'spec_per_km2_log'))}) and together with density per population ({tci(S46('P5b_both', 'spec_per_km2_log'))}), while density per population stayed inverse in that model ({tci(S46('P5b_both', IMS))}) ({sup('posthoc')})."),
("Treated versus suspected dyslipidaemia",
 f"District treatment ratios were weakly and inversely correlated with ratios of suspected dyslipidaemia (Spearman's ρ {G_['rho_lipt_susp']:.2f}). Of {G_['n']} districts, {G_['quadrants']['treated high / suspected low']} had a treatment ratio above 1 with a suspected ratio of 1 or less, mostly in Seoul and Gyeonggi, and {G_['quadrants']['treated low / suspected high']} the reverse, mostly in the Jeolla provinces, Busan and the Gyeongsang and Chungcheong provinces (Fig. 1B). The log ratio between treated and suspected dyslipidaemia was spatially clustered (Moran's I {G_['moran_G']:.2f}) and correlated with tertiary education (ρ {G_['rho_G_tertiary']:.2f}) and inversely with specialist density (ρ {G_['rho_G_im']:.2f})."),
]

# 문장 주장 대조(결과표와 어긋나면 빌드 중단)
assert N["n_cred_hyp"] == 3 and N["n_robust"] == 3 and N["waic_main"] > N["waic_forced"] and BEST == "KH_typeII"
assert all(M[v]["cred"] for v in ROB) and M[EDU]["IRR"] > 1 and M[IMS]["IRR"] < 1 and M[MPA]["IRR"] < 1
assert not any(M[v]["cred"] for v in NULLV) and N["negctl"]["fires_per_10000"]["cred"] and not N["negctl"]["hit_and_run_rate"]["cred"] and not N["negctl"]["waste_recycling_rate"]["cred"]
assert all(dW(a) < 0 for a in KH) and all(S43(a, EDU)[3] for a in KH) and not any(S43(a, MPA)[3] for a in ("KH_typeII", "KH_typeIII", "KH_typeIV"))
assert not S43("KH_typeII", IMS)[3] and not S43("KH_typeIV", IMS)[3]
assert all(N["win_irr"][(EDU, w)][3] for w in ("W1_2011-17", "W2_2018-24")) and not any(N["win_irr"][(v, w)][3] for v in (IMS, MPA) for w in ("W1_2011-17", "W2_2018-24"))
assert N['win_irr'][('walking_practice_rate', 'W2_2018-24')][3] and N['win_irr'][('walking_practice_rate', 'W2_2018-24')][0] > 1 and not N['win_irr'][('walking_practice_rate', 'W1_2011-17')][3]
assert N["epop"][EDU][3] and N["epop"][MPA][3] and not N["epop"][IMS][3]
assert S46("P2_alone", IMS)[3] and S46("P3c_drop_physicians_urban", IMS)[3] and S46("P4_between_within", IMS + "__B")[3] and not S46("P4_between_within", IMS + "__W")[3]
assert S46("P5_per_area", "spec_per_km2_log")[3] and S46("P5_per_area", "spec_per_km2_log")[0] > 1 and S46("P5b_both", "spec_per_km2_log")[3]
assert RSL(IMS, "Capital")[3] and RSL(IMS, "Chungcheong")[3] and not any(RSL(IMS, r)[3] for r in ("Yeongnam", "Honam", "Gangwon_Jeju"))
assert LO[("province", EDU)] == (16, 16) and LO[("year", EDU)] == (14, 14) and N["rubin"][EDU]["n_cred"] == 20
assert G_["rho_lipt_susp"] < 0 and G_["moran_G_p"] <= 0.001 and list(N["hot_by_sido"])[:2] == ["서울시", "경기도"] and abs(Y1 - 12.6) < 0.1

if __name__ == "__main__":
    import re
    for h, t in METHODS + RESULTS: print("##", h, "\n", t, "\n")
    print("words M", sum(len(re.sub(r"\[@[^\]]+\]", "", t).split()) for _, t in METHODS), "R", sum(len(re.sub(r"\[@[^\]]+\]", "", t).split()) for _, t in RESULTS))
