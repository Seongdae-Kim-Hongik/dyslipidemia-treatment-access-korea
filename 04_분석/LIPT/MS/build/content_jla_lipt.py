# content_jla_lipt.py — 31호 LIPT J Lipid Atheroscler(이중 익명) 원고 문장: content_lipt의 Methods·Results·수치를 그대로 쓰고 제목·running head·키워드·윤리 문단만 바꾼다(2026-11-16).
#  이중 익명: 본문에 기관명·IRB 번호·저장소·AI 고지 금지(제목면에만). 키워드 ≤5(MeSH). 제목 쌍점·시리즈 틀 금지.
from content_lipt import *          # noqa: F401,F403  (N, ci, METHODS, RESULTS, sup, fh, dW ...)
import content_lipt as _B
_LK = _B._LK
TITLE = "Does lipid-lowering treatment in Korea follow lipid risk or access to care? A nationwide district-level analysis of health screening, 2011–2024"
RUNNING = "Lipid risk or access in dyslipidemia treatment"
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
