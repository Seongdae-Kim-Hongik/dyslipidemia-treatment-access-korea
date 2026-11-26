# build_manuscript_lipt.py - manuscript and title page (docx).
# Part of the analysis code for dyslipidemia-treatment-access-korea (v1.1.0, MIT license). See README.md (Pipeline) for how to run.
import os, re, json, subprocess
from docx.shared import Pt
from docx_engine import DocxEngine
from american import amer
import content_manuscript_lipt as C
HERE = os.path.dirname(os.path.abspath(__file__)); MS = os.path.dirname(HERE); OUT = os.path.join(MS, "out"); os.makedirs(OUT, exist_ok=True)
N = C.N; REFS = json.load(open(os.path.join(HERE, "refs_lipt.json"), encoding="utf-8"))
DRAFT = os.path.join(MS, "draft", "02_manuscript_jla.md")
TITLE = C.TITLE; RUNNING = C.RUNNING; ORCID = "0000-0002-1525-0091"; PHONE = os.environ.get("AUTHOR_PHONE", "not given"); EMAIL = os.environ.get("AUTHOR_EMAIL", "not given")
AFFIL = "Department of Biohealth Convergence Open Sharing System, Hongik University, Seoul, Korea"
ADDRESS = "Department of Biohealth Convergence Open Sharing System, Hongik University, 94 Wausan-ro, Mapo-gu, Seoul 04066, Korea"
IRB = "The Institutional Review Board of Hongik University approved the study on 4 November 2025 (IRB No. 7002340-202511-HR-012) and its continuing review on 3 November 2026 (IRB No. 7002340-202611-HR-040), and waived informed consent because only published aggregate statistics were used."
AI_STATEMENT = "During the preparation of this work, the author used Claude Opus 5.5 (Anthropic) and ChatGPT (GPT-6 Astra; OpenAI) only for translation and English-language editing of the manuscript. The author reviewed and edited all output and takes full responsibility for the content of the manuscript."
CONTRIB = "Conceptualization, data curation, formal analysis, investigation, methodology, software, validation, visualization, writing - original draft, and writing - review and editing: Kim S."
COI = "The author declares that there are no competing interests."
FUNDING = "None. This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors."
REPO = "https://github.com/Seongdae-Kim-Hongik/dyslipidemia-treatment-access-korea"
_zf = os.path.join(MS, "out", "zenodo_doi.txt"); ZENODO = open(_zf).read().strip() if os.path.exists(_zf) else "[ZENODO DOI]"
DATA = ("The source data are publicly available from the Korean Statistical Information Service (https://kosis.kr) and the other national statistics cited in the Methods. "
        f"The analysis code that generates every number, table and figure is openly available on Zenodo (https://doi.org/{ZENODO}) and GitHub ({REPO}) under the MIT license. "
        "The processed district-year data are available from the author on reasonable request.")
SZ = 10
def read_draft():
    md = open(DRAFT, encoding="utf-8").read(); md = re.sub(r"<!--.*?-->", "", md, flags=re.S); S = {}; cur = None
    _e = N["main"][C.EDU]; _ph = {"N_DISTRICTS": f"{N['n_districts']}", "N_HYP": f"{N['n_hyp']}", "N_FORCED": f"{sum(1 for v in N['main'].values() if v['role'] == 'forced')}",
           "N_ATTEND_M": f"{N['T1']['2011-2024']['exam']/1e6:.1f}", "N_CASES_M": f"{N['T1']['2011-2024']['cases']/1e6:.1f}",
           "RR_EDU": f"RR {_e['IRR']:.3f}; 95% CrI {_e['lo']:.3f}–{C.fh(_e['hi'])}", "RHO_TS": f"{N['gap']['all_2011-24']['rho_lipt_susp']:.2f}",
           "VS_COV": f"{100*N['varpart']['fixed_covariates']['share_of_linear_predictor_var']:.0f}"}
    md = re.sub(r"⟦([A-Z_]+)⟧", lambda m: _ph[m.group(1)], md); assert "⟦" not in md
    for line in md.split("\n"):
        m = re.match(r"^## (.+)$", line)
        if m: cur = m.group(1).strip(); S[cur] = []; continue
        if cur is not None: S[cur].append(line)
    return {k: [p.strip() for p in "\n".join(v).split("\n\n") if p.strip()] for k, v in S.items()}
def pandoc_cites(t):
    f = lambda m: (m.group(2) or "") + "{{" + ",".join(k.strip().lstrip("@") for k in m.group(1).split(";")) + "}}"
    return re.sub(r"\s*\[(@[^\]]+)\]([.,;:])?", f, t)
def all_keys():
    src = " ".join(t for _, t in C.METHODS + C.RESULTS) + open(DRAFT, encoding="utf-8").read()
    src = re.sub(r"<!--.*?-->", "", src, flags=re.S)
    return sorted(k for k in {k.strip().lstrip("@") for g in re.findall(r"\[(@[^\]]+)\]", src) for k in g.split(";")} if re.fullmatch(r"(web:)?[a-z][a-z0-9]*", k))
KEYS = all_keys()
ABL = ("Objective", "Methods", "Results", "Conclusion")

AUTH = {"okuyama2019effect": ["Okuyama K", "Akai K", "Kijima T", "Abe T", "Isomura M", "Nabika T"], "rhee2019guidelines": ["Rhee EJ", "Kim HC", "Kim JH", "Lee EY", "Kim BJ", "Kim EM", "Song Y", "Lim JH"], "mach2019esc": ["Mach F", "Baigent C", "Catapano AL", "Koskinas KC", "Casula M", "Badimon L", "Chapman MJ"],
        "ctt2010efficacy": ["Cholesterol Treatment Trialists' (CTT) Collaboration"], "hartz2006why": ["Hartz I", "Njølstad I", "Furu K", "Skurtveit S", "Eggen AE"]}
from shared_lipt import TFIX
NLMJ = {"J R Stat Soc Series B Stat Methodol": "J R Stat Soc Series B Stat Methodol", "J Public Health (Oxf)": "J Public Health (Oxf)"}
def rng(p):
    p = str(p); m = re.match(r"^(\d+)-(\d+)$", p)
    return f"{m.group(1)}-{m.group(2)}" if m else p
def ref(k):
    r = REFS[k]
    if r["type"] == "web":
        t = r["title"].rstrip(".")
        if k == "web:kosis2026screening":
            return f"{r['authors']}. National health screening statistics: screening attendees by district (DT_35007_N098) and by sex and age group (DT_35007_N099), judgment results by disease (DT_35007_N105) and by sex and 5-year age group (DT_35007_N106), 2011-2024 [Internet]. Daejeon: Korean Statistical Information Service; {r['year']} [cited 2026 Nov 11]. Available from: https://kosis.kr/statHtml/statHtml.do?orgId=350&tblId=DT_35007_N098, https://kosis.kr/statHtml/statHtml.do?orgId=350&tblId=DT_35007_N099, https://kosis.kr/statHtml/statHtml.do?orgId=350&tblId=DT_35007_N105 and https://kosis.kr/statHtml/statHtml.do?orgId=350&tblId=DT_35007_N106"
        return f"{r['authors']}. R: a language and environment for statistical computing. Version 4.6.0 [Internet]. Vienna: R Foundation for Statistical Computing; {r['year']} [cited 2026 Oct 20]. Available from: {r['url']}"
    au = AUTH.get(k, r["authors"])
    a = ", ".join(au) if len(au) <= 6 else ", ".join(au[:6]) + ", et al"
    t = TFIX.get(k, r["title"].rstrip(".")); t = t + ("" if t.endswith(("?", "!")) else ".")
    iss = f"({r['issue']})" if r.get("issue") else ""
    return f"{a}. {t} {NLMJ.get(r['journal'], r['journal'])} {r['year']};{r['vol']}{iss}:{rng(r['pages'])}."

class TX(DocxEngine):
    raw = False
    def __init__(self, cite="sup", lines=True):
        super().__init__(cite)
        st = self.doc.styles["Normal"]; st.font.size = Pt(SZ); self.cell_ls = 2.0; self.title_pt = None
        if not lines:
            from docx.oxml.ns import qn
            for s in self.doc.sections:
                e = s._sectPr.find(qn("w:lnNumType"))
                if e is not None: s._sectPr.remove(e)
    def table(self, title, *a, **k):
        n0 = len(self.doc.paragraphs); r = super().table(title, *a, **k)
        if self.title_pt:
            for run in self.doc.paragraphs[n0].runs: run.font.size = Pt(self.title_pt)
        return r
    def _emit(self, p, text, sz=12, bold=False, italic=False):
        if sz == 12: sz = SZ
        if not self.raw:
            text = amer(text); text = re.sub(r"(^|[\s(])-(?=\d)", "\\1\u2212", text)
        return super()._emit(p, text, sz, bold, italic)

def foot_row(J, text, sz=8, ls=12):
    from docx.enum.text import WD_LINE_SPACING
    p = J.doc.add_paragraph(); p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY; p.paragraph_format.line_spacing = Pt(ls); p.paragraph_format.space_before = Pt(4)
    c = J.counting; J.counting = False; J._emit(p, text, sz); J.counting = c
def put_table(J, t, fs=9):
    c = J.counting; J.counting = False; J.table_fit(amer(t[0]), [amer(x) for x in t[1]], [[amer(x) for x in r] for r in t[2]], "", fs_max=fs, title_bold=True); foot_row(J, t[3], 8); J.counting = c

from shared_lipt import TAB1_COV, GROUPS as _G, LABEL
GROUPS = [("Lifestyle-related risk factors" if g == "Lipid risk factors" else g, v) for g, v in _G]
def table1():
    from shared_lipt import SRCAB, YRAB, SRC_FOOT, UNIT
    T = N["T1"]; cols = ["W1_2011-17", "W2_2018-24", "2011-2024"]
    rows = [["__H__", "Health screening"],
            ["  District-years", "n", ""] + [f"{T[c]['n']:,}" for c in cols],
            ["  Attendances", "million", ""] + [f"{T[c]['exam']/1e6:.1f}" for c in cols],
            ["  Treated dyslipidaemia", "million", ""] + [f"{T[c]['cases']/1e6:.2f}" for c in cols],
            ["  Crude share treated", "% of attendances", ""] + [f"{T[c]['pos']:.1f}" for c in cols],
            ["  Crude rate", "per 100,000 attendances", ""] + [f"{N['s22'][k]['crude_per100k_228']:,.0f}" for k in ("2011-2017", "2018-2024", "2011-2024")],
            ["  Standardised rate, national", "per 100,000 attendances", ""] + [f"{N['s22'][k]['ASR_per100k_national_std2015']:,.0f}" for k in ("2011-2017", "2018-2024", "2011-2024")],
            ["  Treatment ratio, median*", "ratio", ""] + [f"{T[c]['sir_med']:.2f}" for c in cols],
            ["  Treatment ratio, P10–P90*", "ratio", ""] + [f"{T[c]['sir_p10']:.2f}–{T[c]['sir_p90']:.2f}" for c in cols]]
    for g, vs in GROUPS:
        rows.append(["__H__", f"{g}, mean (SD)"])
        for v in vs:
            mx = max(abs(T[c]['cov'][v][0]) for c in cols); dp = 0 if mx >= 100 else (2 if mx < 1 else 1)
            rows.append([f"  {LABEL[v]}", UNIT[v], f"{SRCAB[v]}, {YRAB.get(v, '2011–24')}"] + [f"{T[c]['cov'][v][0]:,.{dp}f} ({T[c]['cov'][v][1]:,.{dp}f})" for c in cols])
    assert sum(1 for r in rows if r[0].startswith("  ") and r[2]) == 16
    foot = ("Treated dyslipidaemia, programme judgement of existing disease: attendees classified as already diagnosed and on drug treatment for dyslipidaemia; P10–P90, 10th–90th percentile; SD, standard deviation; respondents, Community Health Survey respondents; invited people, people invited to general health screening. "
            "Crude rate, treated attendances per 100,000 attendances in the analysed districts; standardised rate, national rate directly standardised for sex and age to the 2015 national attendee structure (age- and sex-specific national rates are given in Supplementary Table S11). "
            "All 16 district-level covariates are shown on their original scale (district-years); internal-medicine specialists entered the models as log(1 + specialists per 100,000); medians, interquartile ranges, ranges and filled cells are given in Supplementary Table S3. "
            + SRC_FOOT + " "
            "*Observed over expected numbers summed over the window, with expected numbers from the national share treated by sex and 5-year age group applied to attendees. "
            "†Census years; values between censuses were linearly interpolated and values after 2020 were held at the 2020 census. "
            "‡Age-standardised district estimates. §Not surveyed in 2019 (obesity) or 2018 (moderate-to-vigorous activity); filled by within-district interpolation.")
    return ("Table 1. Treated dyslipidaemia among health-screening attendees and the 16 district-level covariates, with units, data sources and years, by calendar window, Korea, 2011–2024", ["Characteristic", "Unit", "Source, years", "2011–2017", "2018–2024", "2011–2024"], rows, foot)
def table2():
    from shared_lipt import UNIT
    rows = []; assert sum(len(v) for g, v in GROUPS[:-1]) == N["n_hyp"] and set(LABEL) == set(N["main"])
    f3 = lambda e, lo, hi: f"{e:.3f} ({lo:.3f}\u2060–\u2060{C.fh(hi)})"
    t3 = lambda t: f"{t[0]:.3f} ({t[1]:.3f}\u2060–\u2060{C.fh(t[2]) if t[3] else f'{t[2]:.3f}'})"
    for g, vs in GROUPS:
        rows.append(["__H__", g])
        for v in vs:
            m = N["main"][v]; mv = N["mv"].get(v)
            rows.append([f"  {LABEL[v]}" + ("†" if v == C.IMS else ""), UNIT[v], f3(m['IRR'], m['lo'], m['hi']), f"{100*mv['cred_frac']:.0f}" if mv else "NA",
                         t3(N["epop"][v]), t3(N["sens_main"]["s8"][v]), t3(N["xf"]["E_crude"][v])])
    A = N["retention"]
    foot = (f"RR, rate ratio per 1 standard deviation of the covariate; CrI, credible interval; NA, not applicable (forced into every specification). Principal model, negative binomial with a Besag–York–Mollié 2 district effect and random-walk and independent year effects, without a space–time interaction (n={N['n_rows']:,} district-years, {N['n_districts']} districts, 2011–2024), with expected numbers from national sex- and age-specific shares applied to attendees. "
            "The last 3 columns refit the principal model with other expected numbers: residents, the same shares applied to the resident population; age only, national age-specific shares without sex; crude, attendees multiplied by the national crude share, so that sex and age enter only through the forced sex ratio and share aged 80 years or older (post hoc). "
            "An association was regarded as credible when the 95% CrI excluded 1; RRs and CrIs are rounded to 3 decimals, and intervals with a bound shown as 1.000 were classified from unrounded values, which are kept in the results tables of the code repository. "
            f"The 3 credible covariates remained credible in {A[C.EDU]['kept']} (tertiary education), {A[C.IMS]['kept']} (specialists) and {A[C.MPA]['kept']} (activity) of {A[C.EDU]['n_specs']} alternative specifications; estimates from space–time interaction models are shown in Fig. 2 and Supplementary Table S5. "
            "The share aged 80 years or older is a forced control beyond indirect standardisation and is not interpreted. *Share of the 200 covariate-subset fits containing the covariate in which the CrI excluded 1 (subset-stable, at least 75% with the same sign in at least 95%). "
            "†Entered the models as log(1 + specialists per 100,000) before standardisation.")
    return ("Table 2. District characteristics and sex- and age-standardised treated dyslipidaemia in the principal model and with alternative expected numbers", ["Characteristic", "Unit", "RR (95% CrI)", "Subsets credible, %*", "Residents", "Age only", "Crude"], rows, foot)
from shared_lipt import FIGCAP

BREAK_BEFORE = {"Lifestyle-related risk factors", "Strengths and limitations"}
def build():
    D = read_draft(); J = TX(cite="sup")
    J.para(f"<b>{TITLE}</b>")
    J.head("Abstract", 1)
    for p, lab in zip(D["Abstract"], ABL):
        assert p.startswith(lab + ":"), (lab, p[:30]); J.para(f"<b>{lab}:</b> {p[len(lab)+1:].strip()}")
    J.para(f"<b>Keywords:</b> {C.KEYWORDS}", before=6)
    J.page_break(); J.counting = True
    J.head("INTRODUCTION", 1)
    for p in D["Introduction"]: J.para(pandoc_cites(p), indent=True)
    J.head("MATERIALS AND METHODS", 1)
    for i, (h, p) in enumerate(C.METHODS, 1): J.head(f"{i}. {h}", 2); J.para(pandoc_cites(p), indent=True)
    J.head("RESULTS", 1)
    for i, (h, p) in enumerate(C.RESULTS, 1): J.head(f"{i}. {h}", 2); J.para(pandoc_cites(p), indent=True)
    J.head("DISCUSSION", 1); _k = 0
    for p in D["Discussion"]:
        if p.startswith("### "):
            _k += 1
            pass
            J.head(f"{_k}. {p[4:].strip()}", 2); continue
        J.para(pandoc_cites(p), indent=True)
    J.counting = False
    J.head("ACKNOWLEDGMENTS", 4); J.para(C.ACK_ANON)
    J.head("CONFLICTS OF INTEREST", 4); J.para(COI)
    J.head("FUNDING", 4); J.para(FUNDING)
    J.head("DATA AVAILABILITY STATEMENT", 4); J.para("The source data are publicly available from the Korean Statistical Information Service (https://kosis.kr) and the other national statistics cited in the Materials and Methods. The analysis code that generates every number, table and figure is openly available in a public repository under the MIT license; the link is given on the title page to preserve anonymity during review. The processed district-year data are available on reasonable request.")
    J.head("AUTHOR CONTRIBUTIONS", 4); J.para(C.CONTRIB_ANON)
    J.para("<b>Supplementary Material:</b> Supplementary Sections S1–S9, Supplementary Tables S1–S11 and Supplementary Figs. S1 and S2 are provided in a separate file.", before=12)
    assert sorted(J.cites) == KEYS, (set(J.cites) ^ set(KEYS))
    J.page_break(); J.head("REFERENCES", 1); J.raw = True; rl = []
    for i, k_ in enumerate(J.cites, 1): s_ = f"{i}. " + ref(k_); rl.append(s_); J.para(s_)
    J.raw = False
    J.title_pt = 11; J.page_break(); put_table(J, table1(), fs=8); J.page_break(); J.fit_pad = 0.45; put_table(J, table2(), fs=9); J.fit_pad = 0.65; J.title_pt = None
    J.page_break(); J.head("FIGURE LEGENDS", 1)
    for k_ in sorted(FIGCAP):
        _p = J.para(f"<b>Fig. {k_}. {FIGCAP[k_][0]}</b> {FIGCAP[k_][1]}")
        for _r in _p.runs:
            if _r.bold: _r.font.size = Pt(11)
    return J, rl, D
def titlepage(bw, aw, nref, npg):
    J = TX(cite="sup", lines=False)
    J.para("<b>Title page</b>")
    J.para(f"<b>Title:</b> {TITLE}", before=6)
    J.para(f"<b>Running head:</b> {RUNNING}", before=4)
    J.para("<b>Author:</b> Seongdae Kim", before=4)
    J.para(f"<b>Affiliation:</b> {AFFIL}", before=4)
    J.para(f"<b>Correspondence:</b> Seongdae Kim, {ADDRESS}. Telephone: {PHONE}. Fax: not available. E-mail: {EMAIL}. ORCID: Seongdae Kim https://orcid.org/{ORCID}", before=4)
    J.para(f"<b>Funding:</b> {FUNDING}", before=4)
    J.para(f"<b>Conflict of Interest:</b> {COI}", before=4)
    J.para(f"<b>Author Contributions:</b> {CONTRIB}", before=4)
    J.para(f"<b>Ethics Statement:</b> {IRB}", before=4)
    J.para(f"<b>Data Availability Statement:</b> {DATA}", before=4)
    J.para(f"<b>Acknowledgments:</b> {AI_STATEMENT}", before=4)
    J.para(f"<b>Manuscript details:</b> main text {bw:,} words; abstract {aw} words; {nref} references; 2 tables; 2 figures; {npg} pages in the anonymized manuscript file.", before=4)
    return J
def to_pdf(path):
    subprocess.run(["/opt/homebrew/bin/soffice", "--headless", "-env:UserInstallation=file:///tmp/lo_lipt_jla", "--convert-to", "pdf", "--outdir", OUT, path], capture_output=True, check=True)
def npages(pdf): return int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
def docx_bw(path):
    from docx import Document
    t = "\n".join(x.text for x in Document(path).paragraphs)
    a = t.find("\nINTRODUCTION\n"); return len(t[a:t.find("\nACKNOWLEDGMENTS\n", a)].split())
if __name__ == "__main__":
    p = os.path.join(OUT, "Manuscript_anonymized_LIPT.docx"); D = read_draft()
    AB = [re.sub(r"^(Objective|Methods|Results|Conclusion):\s*", "", x) for x in D["Abstract"]]; aw = sum(len(x.split()) for x in AB) + 4
    J, rl, D = build(); J.doc_title = "Manuscript"; J.save(p); bw = docx_bw(p); to_pdf(p); np_ = npages(p[:-5] + ".pdf")
    TP = titlepage(bw, aw, len(KEYS), np_); tp = os.path.join(OUT, "Title_Page_LIPT.docx"); TP.doc_title = "Title page"; TP.save(tp)
    open(os.path.join(OUT, "wordcount_jla.txt"), "w").write(f"body_words={bw}\nabstract_words={aw}\nrefs={len(KEYS)}\ntables=2\nfigures=2\ntitle_words={len(TITLE.split())}\npages={np_}\n")
    print(f"body {bw} | abstract {aw} | refs {len(KEYS)} | pages {np_} | title words {len(TITLE.split())}")
