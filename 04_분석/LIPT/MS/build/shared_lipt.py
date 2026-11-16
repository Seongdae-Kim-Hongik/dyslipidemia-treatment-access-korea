# shared_lipt.py — 31호 LIPT 원고 공용 상수: 참고문헌 문장형 표제(서지 대조 완료본), 표 1 공변량, 표 2 묶음·라벨, 그림 범례(2026-11-16).
TFIX = {"kang2015korea": "Korea Community Health Survey data profiles",
        "heidari2016sex": "Sex and gender equity in research: rationale for the SAGER guidelines and recommended use",
        "kwon2025dyslipidemia": "Dyslipidemia fact sheet in South Korea, 2024",
        "kwon2026cardiovascular": "Cardiovascular disease incidence and lipid-lowering medication use in Korean adults with dyslipidemia: a nationwide population-based retrospective cohort study from 2010 to 2019",
        "ray2022world": "World Heart Federation cholesterol roadmap 2022",
        "simpson2017penalising": "Penalising model component complexity: a principled, practical approach to constructing priors",
        "smart2025effect": "The effect of exercise training on blood lipids: a systematic review and meta-analysis",
        "zheutlin2024association": "Association between pharmacy proximity with cardiovascular medication use and risk factor control in the United States",
        "stocks2009gender": "Gender, socioeconomic status, need or access? Differences in statin prescribing across urban, rural and remote Australia",
        "mach2019esc": "2019 ESC/EAS guidelines for the management of dyslipidaemias: lipid modification to reduce cardiovascular risk",
        "ncdrisc2020repositioning": "Repositioning of the global epicentre of non-optimal cholesterol",
        "ctt2010efficacy": "Efficacy and safety of more intensive lowering of LDL cholesterol: a meta-analysis of data from 170,000 participants in 26 randomised trials",
        "lee2025national": "National trends in dyslipidemia prevalence, awareness, treatment, and control in South Korea from 2005 to 2022",
        "lee2025inter": "Inter-regional patient outmigration to Seoul in South Korea: the role of regional healthcare quality perceptions",
        "han2021regional": "Regional and income disparities in treatment and drug adherence of patients with dyslipidemia: a retrospective cohort study in South Korea, 2003-2015",
        "marcus2021unmet": "Unmet need for hypercholesterolemia care in 35 low- and middle-income countries: a cross-sectional study of nationally representative surveys",
        "hartz2006why": "Why do sales of lipid-lowering drugs vary between counties in Norway? Evidence from the OPPHED Health Study 2000-2001",
        "ashworth2007social": "Social deprivation and statin prescribing: a cross-sectional analysis using data from the new UK general practitioner 'Quality and Outcomes Framework'",
        "erickson2014geospatial": "Geospatial analysis of statin adherence using pharmacy claims data in the state of Michigan",
        "kodama2007effect": "Effect of aerobic exercise training on serum levels of high-density lipoprotein cholesterol: a meta-analysis",
        "wallachkildemoes2013adherence": "Adherence to preventive statin therapy according to socioeconomic position",
        "cheolseong2017data": "Data resource profile: the National Health Information Database of the National Health Insurance Service in South Korea",
        "riebler2016intuitive": "An intuitive Bayesian spatial model for disease mapping that accounts for scaling",
        "lipsitch2010negative": "Negative controls: a tool for detecting confounding and bias in observational studies"}

TAB1_COV = [("pop80_share", "Population aged 80 years or older, %"), ("tertiary_educated_share", "Tertiary education, % of adults"),
            ("im_specialists_per_100k", "Internal-medicine specialists per 100,000"), ("screening_uptake", "Health-screening uptake, %"),
            ("obesity_rate", "Obesity, %"), ("walking_practice_rate", "Walking practice, %"), ("moderate_pa_rate", "Moderate or vigorous activity, %"),
            ("public_sports_facilities_per_100k", "Public sports facilities per 100,000")]

GROUPS = [("Care reach and selection", ["im_specialists_per_100k", "screening_uptake", "tertiary_educated_share"]),
          ("Lipid risk factors", ["obesity_rate", "high_risk_drinking_rate", "current_smoking_rate", "walking_practice_rate", "moderate_pa_rate", "public_sports_facilities_per_100k"]),
          ("Deprivation and household", ["basic_livelihood_rate", "single_person_household_share"]),
          ("Forced controls", ["urban_population_share", "physicians_per_1000", "sex_ratio", "fiscal_independence", "pop80_share"])]
LABEL = {"im_specialists_per_100k": "Internal-medicine specialists", "screening_uptake": "Health-screening uptake", "tertiary_educated_share": "Tertiary education",
         "obesity_rate": "Obesity", "high_risk_drinking_rate": "High-risk drinking", "current_smoking_rate": "Current smoking", "walking_practice_rate": "Walking practice",
         "moderate_pa_rate": "Moderate or vigorous activity", "public_sports_facilities_per_100k": "Public sports facilities", "basic_livelihood_rate": "Basic livelihood security",
         "single_person_household_share": "Single-person households", "urban_population_share": "Urban population share", "physicians_per_1000": "Physicians per 1,000",
         "sex_ratio": "Sex ratio", "fiscal_independence": "Fiscal autonomy", "pop80_share": "Aged 80 years or older"}

FIGCAP = {
 1: ("Geography of treated dyslipidaemia and its relation to suspected dyslipidaemia among health-screening attendees, Korea, 2011–2024.",
     "(A) Residual spatial rate ratio (RR) by district, the posterior mean of the exponentiated Besag–York–Mollié 2 district effect from the principal model. Solid outlines, hot spots (posterior probability of residual spatial RR above 1 greater than 0.95); dashed outlines, cold spots (less than 0.05); thick lines, province boundaries; grey, no data (Sejong). (B) Districts classified by whether the sex- and age-standardised ratios of treated and of suspected untreated dyslipidaemia for 2011–2024 exceeded 1. District boundaries as of 2024."),
 2: ("Rate ratios for the three subset-stable district characteristics across models.",
     "Rate ratios per 1 standard deviation with 95% credible intervals from the principal model, models with Knorr-Held type II (best fitting) and type IV space–time interactions, the principal model fitted to 2011–2017 and to 2018–2024 only, and the principal model with expected numbers computed from residents instead of attendees. The dotted vertical line marks a rate ratio of 1."),
}
