# content_manuscript_lipt.py - manuscript-specific text layer on top of content_lipt.py.
# Part of the analysis code for dyslipidemia-treatment-access-korea (v1.1.0, MIT license). See README.md (Pipeline) for how to run.
from content_lipt import *
import content_lipt as _B
import re as _re
_LK = _B._LK
TITLE = "Is self-reported treated dyslipidemia among Korean screening attendees linked to district education rather than lifestyle risk factors?"
RUNNING = "Education, lifestyle and treated dyslipidemia"
assert ":" not in TITLE and "229" not in TITLE and "standardi" not in TITLE.lower() and len(RUNNING) <= 50
KEYWORDS = "Dyslipidemias; Health services accessibility; Educational status; Spatial analysis; Republic of Korea"
assert len(KEYWORDS.split(";")) <= 5
ETHICS = ("This study was approved by the Institutional Review Board of Hongik University (IRB No. 7002340-202511-HR-012, approved on 4 November 2025), "
          "and its continuing review was approved by the same board (IRB No. 7002340-202611-HR-040, approved on 3 November 2026). "
          "The board waived the requirement for informed consent because only published district-level aggregate statistics were used and no individual-level data were accessed.")
SUPMAP = {"judgement": "Supplementary Section S1 and Supplementary Tables S1 and S2",
          "methods": "Supplementary Section S1",
          "covariates": "Supplementary Section S2 and Supplementary Table S3",
          "checks": "Supplementary Section S3 and Supplementary Table S4",
          "specs": "Supplementary Section S4 and Supplementary Tables S5 and S6",
          "strobe": "Supplementary Section S5 and Supplementary Table S7",
          "persistence": "Supplementary Section S6, Supplementary Table S8 and Supplementary Fig. S1",
          "fig_observed": "Supplementary Fig. S2",
          "spec_tables": "Supplementary Tables S5 and S6",
          "spec_table": "Supplementary Table S5",
          "kh_table": "Supplementary Table S6",
          "windows": "Supplementary Section S7 and Supplementary Table S9",
          "window_table": "Supplementary Table S9",
          "posthoc": "Supplementary Section S8 and Supplementary Table S10"}
assert set(SUPMAP) == set(_B.SUPKEYS)
METHODS, RESULTS = _B.texts(ETHICS, SUPMAP)
_txt = " ".join(t for _, t in METHODS + RESULTS)
assert list(dict.fromkeys(_re.findall(r"Supplementary Section S(\d)", _txt))) == [str(i) for i in range(1, 9)]
_tabs = list(dict.fromkeys(int(x) for g in _re.findall(r"Supplementary Tables? S(\d+)(?: and S(\d+))?", _txt) for x in g if x))
assert _tabs == list(range(1, 11)), _tabs
assert _txt.find("Supplementary Fig. S1") < _txt.find("Supplementary Fig. S2")
ACK_ANON = ("During the preparation of this work, the author used Claude Opus 5.5 (Anthropic) and ChatGPT (GPT-6 Astra; OpenAI) only for translation and English-language editing of the manuscript. "
            "The author reviewed and edited all output and takes full responsibility for the content of the manuscript.")
CONTRIB_ANON = ("The sole author was responsible for conceptualization, data curation, formal analysis, investigation, methodology, software, validation, visualization, "
                "writing (original draft) and writing (review and editing). The named contribution statement is provided on the separate title page.")
