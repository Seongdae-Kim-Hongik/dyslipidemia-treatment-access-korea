# build_jla_lipt.py — J Lipid Atheroscler(KSoLA, Editorial Manager) Original Article 원고 조립(2026-11-16, 31호 LIPT).
#  규정 요점: 논문 폴더 00_저널가이드/JLA_가이드_요점_261116.md
#  A4·여백 2.5 cm·10 pt·이중 간격·쪽 번호. 순서 = 제목 → 초록(Objective/Methods/Results/Conclusion ≤250)·Key words(≤5, MeSH) → Introduction → Materials and Methods → Results
#  → Discussion(결론은 끝 문단, 별도 절 없음) → References(≤50, 첫 인용 순, 위첨자를 문장부호 뒤에, NLM) → Tables(쪽마다, 세로선 없음, 각주 *,†,‡ 순) → Figure legends.
#  이중 익명: 본문에 저자·기관·IRB·저장소·AI 고지 금지 → 제목면 파일(Title_Page)에 running head·교신(주소·전화·팩스·이메일)·연구비·이해상충·저자 기여·윤리·자료 진술·Acknowledgments(AI 고지).
#  사용: run_all_jla.sh
import os, re, json, subprocess
from docx.shared import Pt
from jkms_engine import JKMS
from american import amer
import content_jla_lipt as C
HERE = os.path.dirname(os.path.abspath(__file__)); MS = os.path.dirname(HERE); OUT = os.path.join(MS, "out"); os.makedirs(OUT, exist_ok=True)
N = C.N; REFS = json.load(open(os.path.join(HERE, "refs_lipt.json"), encoding="utf-8"))
DRAFT = os.path.join(MS, "draft", "02_manuscript_jla.md")
TITLE = C.TITLE; RUNNING = C.RUNNING; ORCID = "0000-0002-1525-0091"; PHONE = "+82-2-320-1114"; EMAIL = "kimsd@hongik.ac.kr"
AFFIL = "Department of Biohealth Convergence Open Sharing System, Hongik University, Seoul, Korea"
ADDRESS = "Department of Biohealth Convergence Open Sharing System, Hongik University, 94 Wausan-ro, Mapo-gu, Seoul 04066, Korea"
IRB = "The Institutional Review Board of Hongik University approved the study on 4 November 2025 (IRB No. 7002340-202511-HR-012) and its continuing review on 3 November 2026 (IRB No. 7002340-202611-HR-040), and waived informed consent because only published aggregate statistics were used."
AI_STATEMENT = "During the preparation of this work, the author used Claude (Anthropic) and ChatGPT (OpenAI) only for translation and English-language editing of the manuscript. The author carefully reviewed and edited the output as necessary and takes full responsibility for the final content of the manuscript."
CONTRIB = "Conceptualization, data curation, formal analysis, investigation, methodology, software, validation, visualization, writing - original draft, and writing - review and editing: Kim S."
COI = "The author has no conflicts of interest to declare."
FUNDING = "None. This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors."
REPO = "https://github.com/Seongdae-Kim-Hongik/dyslipidemia-treatment-access-korea"
_zf = os.path.join(MS, "out", "zenodo_doi.txt"); ZENODO = open(_zf).read().strip() if os.path.exists(_zf) else "[ZENODO DOI]"
DATA = ("The source data are publicly available from the Korean Statistical Information Service (https://kosis.kr) and the other national statistics cited in the Methods. "
        f"The analysis code that generates every number, table and figure is openly available on Zenodo (https://doi.org/{ZENODO}) and GitHub ({REPO}) under the MIT license. "
        "The processed district-year data are available from the author on reasonable request.")
SZ = 10
def read_draft():
    md = open(DRAFT, encoding="utf-8").read(); md = re.sub(r"<!--.*?-->", "", md, flags=re.S); S = {}; cur = None
    for line in md.split("\n"):
        m = re.match(r"^## (.+)$", line)
        if m: cur = m.group(1).strip(); S[cur] = []; continue
        if cur is not None: S[cur].append(line)
    return {k: [p.strip() for p in "\n".join(v).split("\n\n") if p.strip()] for k, v in S.items()}
def pandoc_cites(t):   # "text [@a; @b]." → "text.{{a,b}}" (JLA: 위첨자를 마침표·쉼표 뒤에)
    f = lambda m: (m.group(2) or "") + "{{" + ",".join(k.strip().lstrip("@") for k in m.group(1).split(";")) + "}}"
    return re.sub(r"\s*\[(@[^\]]+)\]([.,;:])?", f, t)
def all_keys():
    src = open(os.path.join(HERE, "content_lipt.py"), encoding="utf-8").read().replace("[@vonelm2007strengthening] (\" + sup('strobe')", "") + open(DRAFT, encoding="utf-8").read()
    src = src + "[@vonelm2007strengthening]"
    src = re.sub(r"<!--.*?-->", "", src, flags=re.S); src = re.sub(r"(?m)^\s*#.*$", "", src)
    return sorted(k for k in {k.strip().lstrip("@") for g in re.findall(r"\[(@[^\]]+)\]", src) for k in g.split(";")} if re.fullmatch(r"(web:)?[a-z][a-z0-9]*", k))
KEYS = all_keys()
ABL = ("Objective", "Methods", "Results", "Conclusion")

# ── NLM(Vancouver) 참고문헌: "Surname AB, ... (6명 초과 시 6명+et al.). Title. J Abbr Year;Vol(Issue):pages."
AUTH = {"mach2019esc": ["Mach F", "Baigent C", "Catapano AL", "Koskinas KC", "Casula M", "Badimon L", "Chapman MJ"],
        "ctt2010efficacy": ["Cholesterol Treatment Trialists' (CTT) Collaboration"], "hartz2006why": ["Hartz I", "Njølstad I", "Furu K", "Skurtveit S", "Eggen AE"]}
from shared_lipt import TFIX   # 문장형 표제(서지 대조 완료본)
NLMJ = {"J R Stat Soc Series B Stat Methodol": "J R Stat Soc Series B Stat Methodol", "J Public Health (Oxf)": "J Public Health (Oxf)"}
def rng(p):
    p = str(p); m = re.match(r"^(\d+)-(\d+)$", p)
    return f"{m.group(1)}-{m.group(2)}" if m else p
def ref(k):
    r = REFS[k]
    if r["type"] == "web":
        t = r["title"].rstrip(".")
        if k == "web:kosis2026screening":
            return f"{r['authors']}. National health screening statistics: screening attendees (DT_35007_N098), judgment results by disease (DT_35007_N105) and by sex and 5-year age group (DT_35007_N106), 2011-2024 [Internet]. Daejeon: Korean Statistical Information Service; {r['year']} [cited 2026 Nov 11]. Available from: {r['url']}"
        return f"{r['authors']}. R: a language and environment for statistical computing. Version 4.6.0 [Internet]. Vienna: R Foundation for Statistical Computing; {r['year']} [cited 2026 Oct 20]. Available from: {r['url']}"
    au = AUTH.get(k, r["authors"])
    a = ", ".join(au) if len(au) <= 6 else ", ".join(au[:6]) + ", et al"
    t = TFIX.get(k, r["title"].rstrip(".")); t = t + ("" if t.endswith(("?", "!")) else ".")
    iss = f"({r['issue']})" if r.get("issue") else ""
    return f"{a}. {t} {NLMJ.get(r['journal'], r['journal'])} {r['year']};{r['vol']}{iss}:{rng(r['pages'])}."

class TX(JKMS):
    raw = False
    def __init__(self, cite="sup", lines=True):
        super().__init__(cite)
        st = self.doc.styles["Normal"]; st.font.size = Pt(SZ)
        if not lines:
            from docx.oxml.ns import qn
            for s in self.doc.sections:
                e = s._sectPr.find(qn("w:lnNumType"))
                if e is not None: s._sectPr.remove(e)
    def _emit(self, p, text, sz=12, bold=False, italic=False):
        if sz == 12: sz = SZ
        if not self.raw:
            text = amer(text); text = re.sub(r"(^|[\s(])-(?=\d)", "\\1\u2212", text)
        return super()._emit(p, text, sz, bold, italic)

def foot_row(J, text, sz=8, ls=12):
    from docx.enum.text import WD_LINE_SPACING
    t = J.doc.tables[-1]; r = t.add_row(); m = r.cells[0].merge(r.cells[-1]); m.text = ""; p = m.paragraphs[0]
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY; p.paragraph_format.line_spacing = Pt(ls); p.paragraph_format.space_before = Pt(4)
    c = J.counting; J.counting = False; J._emit(p, text, sz); J.counting = c
def put_table(J, t, fs=9):
    c = J.counting; J.counting = False; J.table_fit(amer(t[0]), [amer(x) for x in t[1]], [[amer(x) for x in r] for r in t[2]], "", fs_max=fs, title_bold=True); foot_row(J, t[3], 8); J.counting = c

from shared_lipt import TAB1_COV, GROUPS, LABEL
def table1():
    T = N["T1"]; cols = ["W1_2011-17", "W2_2018-24", "2011-2024"]
    rows = [["__H__", "Health screening"],
            ["  District-years, n"] + [f"{T[c]['n']:,}" for c in cols],
            ["  Attendances, million"] + [f"{T[c]['exam']/1e6:.1f}" for c in cols],
            ["  Treated dyslipidaemia, million"] + [f"{T[c]['cases']/1e6:.2f}" for c in cols],
            ["  Crude share treated, %"] + [f"{T[c]['pos']:.1f}" for c in cols],
            ["  District treatment ratio, median*"] + [f"{T[c]['sir_med']:.2f}" for c in cols],
            ["  District treatment ratio, P10–P90*"] + [f"{T[c]['sir_p10']:.2f}–{T[c]['sir_p90']:.2f}" for c in cols],
            ["__H__", "District characteristics, mean (SD)"]]
    for v, lab in TAB1_COV:
        mx = max(abs(T[c]['cov'][v][0]) for c in cols); dp = 0 if mx >= 100 else (2 if mx < 1 else 1)
        rows.append([f"  {lab}"] + [f"{T[c]['cov'][v][0]:,.{dp}f} ({T[c]['cov'][v][1]:,.{dp}f})" for c in cols])
    foot = ("Treated dyslipidaemia, attendees classified as already diagnosed and on drug treatment for dyslipidaemia; P10–P90, 10th–90th percentile; SD, standard deviation. "
            "*Observed over expected numbers summed over the window, with expected numbers from the national share treated by sex and 5-year age group applied to attendees.")
    return ("Table 1. Treated dyslipidaemia among health-screening attendees and district characteristics by calendar window, Korea, 2011–2024", ["Characteristic", "2011–2017", "2018–2024", "2011–2024"], rows, foot)
def table2():
    rows = []; assert sum(len(v) for g, v in GROUPS[:-1]) == N["n_hyp"] and set(LABEL) == set(N["main"])
    f3 = lambda e, lo, hi: f"{e:.3f} ({lo:.3f}–{C.fh(hi)})"
    for g, vs in GROUPS:
        rows.append(["__H__", g])
        for v in vs:
            m = N["main"][v]; mv = N["mv"].get(v); k2 = N["s43"][("KH_typeII", v)]; k4 = N["s43"][("KH_typeIV", v)]
            rows.append([f"  {LABEL[v]}", f3(m['IRR'], m['lo'], m['hi']), f"{100*mv['cred_frac']:.0f}" if mv else "NA", f3(*k2[:3]), f3(*k4[:3])])
    foot = (f"RR, rate ratio per 1 standard deviation; CrI, credible interval; NA, not applicable (forced into every specification). Specialists and sports facilities are per 100,000 population and physicians per 1,000. Principal model, negative binomial with a Besag–York–Mollié 2 district effect and random-walk and independent year effects (n={N['n_rows']:,} district-years). "
            f"The share aged 80 years or older is a forced control beyond indirect standardisation and is not interpreted. *Share of the 200 covariate-subset fits containing the covariate in which the CrI excluded 1 (subset-stable, at least 75% with the same sign in at least 95%). "
            f"†Principal model plus a Knorr-Held type II (best fitting, difference in widely applicable information criterion {C.dW('KH_typeII'):,.0f}) or type IV ({C.dW('KH_typeIV'):,.0f}) space–time interaction.")
    return ("Table 2. District characteristics and sex- and age-standardised treated dyslipidaemia in the principal and space–time interaction models", ["Characteristic", "Principal model RR (95% CrI)", "Subsets credible, %*", "Type II RR (95% CrI)†", "Type IV RR (95% CrI)†"], rows, foot)
from shared_lipt import FIGCAP

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
    J.head("DISCUSSION", 1)
    for p in D["Discussion"]: J.para(pandoc_cites(p), indent=True)
    J.counting = False
    J.para("<b>Supplementary Material:</b> Supplementary Sections S1–S8, Supplementary Tables S1–S5 and Supplementary Fig. S1 are provided in a separate file.", before=12)
    assert sorted(J.cites) == KEYS, (set(J.cites) ^ set(KEYS))
    J.page_break(); J.head("REFERENCES", 1); J.raw = True; rl = []
    for i, k_ in enumerate(J.cites, 1): s_ = f"{i}. " + ref(k_); rl.append(s_); J.para(s_)
    J.raw = False
    J.page_break(); put_table(J, table1()); J.page_break(); put_table(J, table2(), fs=7.5)
    J.page_break(); J.head("FIGURE LEGENDS", 1)
    for k_ in sorted(FIGCAP): J.para(f"<b>Fig. {k_}. {FIGCAP[k_][0]}</b> {FIGCAP[k_][1]}")
    return J, rl, D
def titlepage(bw, aw, nref, npg):
    J = TX(cite="sup", lines=False)
    J.para("<b>Title page</b>")
    J.para(f"<b>Title:</b> {TITLE}", before=6)
    J.para(f"<b>Running head:</b> {RUNNING}", before=4)
    J.para("<b>Author:</b> Seongdae Kim", before=4)
    J.para(f"<b>Affiliation:</b> {AFFIL}", before=4)
    J.para(f"<b>Correspondence:</b> Seongdae Kim, {ADDRESS}. Telephone: {PHONE}. Fax: not available. E-mail: {EMAIL}. ORCID: https://orcid.org/{ORCID}", before=4)
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
    a = t.find("\nINTRODUCTION\n"); return len(t[a:t.find("\nSupplementary Material:", a)].split())
if __name__ == "__main__":
    p = os.path.join(OUT, "Manuscript_anonymized_JLA_LIPT.docx"); D = read_draft()
    AB = [re.sub(r"^(Objective|Methods|Results|Conclusion):\s*", "", x) for x in D["Abstract"]]; aw = sum(len(x.split()) for x in AB) + 4
    J, rl, D = build(); J.doc_title = "Manuscript"; J.save(p); bw = docx_bw(p); to_pdf(p); np_ = npages(p[:-5] + ".pdf")
    TP = titlepage(bw, aw, len(KEYS), np_); tp = os.path.join(OUT, "Title_Page_JLA_LIPT.docx"); TP.doc_title = "Title page"; TP.save(tp)
    open(os.path.join(OUT, "wordcount_jla.txt"), "w").write(f"body_words={bw}\nabstract_words={aw}\nrefs={len(KEYS)}\ntables=2\nfigures=2\ntitle_words={len(TITLE.split())}\npages={np_}\n")
    print(f"body {bw} | abstract {aw} | refs {len(KEYS)} | pages {np_} | title words {len(TITLE.split())}")
