#!/bin/bash
# 31호 LIPT J Lipid Atheroscler 전체 빌드(2026-11-16): 그림 → 원고·제목면 → 보충 → 커버 → sanitize → PDF
set -e; cd "$(dirname "$0")"; O=../out
python3 figs_lipt.py
python3 build_jla_lipt.py
python3 esm_jla_lipt.py
python3 cover_jla_lipt.py
python3 sanitize_docx.py $O/Manuscript_anonymized_JLA_LIPT.docx $O/Supplementary_Material_JLA_LIPT.docx $O/Cover_Letter_JLA_LIPT.docx $O/Title_Page_JLA_LIPT.docx > /dev/null
for f in Manuscript_anonymized_JLA_LIPT Supplementary_Material_JLA_LIPT Cover_Letter_JLA_LIPT Title_Page_JLA_LIPT; do /opt/homebrew/bin/soffice --headless -env:UserInstallation=file:///tmp/lo_lipt_jla_all --convert-to pdf --outdir $O $O/$f.docx > /dev/null 2>&1; done
