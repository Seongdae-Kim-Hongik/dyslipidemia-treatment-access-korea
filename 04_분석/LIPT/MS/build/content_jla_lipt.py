# content_jla_lipt.py — 31호 LIPT J Lipid Atheroscler(이중 익명) 원고 문장: content_lipt의 Methods·Results·수치를 그대로 쓰고 제목·running head·키워드·윤리 문단만 바꾼다(2026-11-16).
#  이중 익명: 본문에 기관명·IRB 번호·저장소·AI 고지 금지(제목면에만). 키워드 ≤5(MeSH). 제목 쌍점·시리즈 틀 금지.
from content_lipt import *          # noqa: F401,F403  (N, ci, METHODS, RESULTS, sup, fh, dW ...)
import content_lipt as _B
_LK = _B._LK
TITLE = "Is self-reported treated dyslipidemia among Korean screening attendees linked to district education rather than lifestyle risk factors?"
RUNNING = "Education, lifestyle and treated dyslipidemia"
assert ":" not in TITLE and "229" not in TITLE and "standardi" not in TITLE.lower() and len(RUNNING) <= 50
KEYWORDS = "Dyslipidemias; Health services accessibility; Educational status; Spatial analysis; Republic of Korea"
assert len(KEYWORDS.split(";")) <= 5
METHODS = [m for m in _B.METHODS if m[0] != "Ethics and reporting"] + [
    ("Reporting", "Only published district-level aggregate statistics were used, and no individual-level data were accessed. Reporting follows the Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement [@vonelm2007strengthening] (" + sup('strobe') + ").")]
assert len(METHODS) == len(_B.METHODS)
RESULTS = _B.RESULTS
# 이전 문장 오류 정정(2026-11-16): 2년 지연 괄호 안에 창별 수치가 들어가 있었음 → 창별 수치는 'both windows' 뒤로, 2년 지연은 E2_lag2 값으로.
_EDU = _B.EDU; _w1 = N['win_irr'][(_EDU, 'W1_2011-17')]; _w2 = N['win_irr'][(_EDU, 'W2_2018-24')]; _l1 = N['s41'][('E1_lag1', _EDU)]; _l2 = N['s41'][('E2_lag2', _EDU)]
assert _w1[3] and _w2[3] and not _l1[3] and not _l2[3]
_old = f"in both windows and with resident-based expected numbers, but not with 1-year ({tci(_l1)}) or 2-year lagged covariates (2011–2017 {tci(_w1)}; 2018–2024 {tci(_w2)})"
_new = f"in both windows (2011–2017 {tci(_w1)}; 2018–2024 {tci(_w2)}) and with resident-based expected numbers, but not with 1-year ({tci(_l1)}) or 2-year lagged covariates ({tci(_l2)})"
RESULTS = [(h, t.replace(_old, _new)) for h, t in _B.RESULTS]
assert sum(_new in t for _, t in RESULTS) == 1

# review 반영(2026-11-16): 용어·과장 정리
_SUBS = [("Lipid risk factors: obesity", "Lifestyle-related risk factors: obesity"),
         ("sex-specific models were not possible because district covariates are not reported by sex, and sex is reported following", "sex-specific associations were not examined because district covariates are not reported by sex, and sex is reported following"),
         (f"Intervals were not adjusted for multiplicity; as a rough frequentist analogy, about {_B.EXP_CHANCE:.2f} of the {_B.NHYP} associations would exclude 1 by chance if all were null.", "Intervals were not adjusted for multiplicity, and associations were interpreted in light of the number of comparisons and the sensitivity analyses."),
         ("Against the expected direction, it was lower with more internal-medicine specialists per population", "It was lower with more internal-medicine specialists per population, opposite to the expected direction")]
def _sub(L):
    out = []
    for h, t in L:
        for a, b in _SUBS: t = t.replace(a, b)
        if h == "Association against the expected direction": h = "Post hoc analyses of specialist density"
        out.append((h, t))
    return out
METHODS = _sub(METHODS); RESULTS = _sub(RESULTS)
_all = " ".join(t for _, t in METHODS + RESULTS)
assert "Lifestyle-related risk factors" in _all and "by chance" not in _all and "were not possible" not in _all and "Against the expected" not in _all
