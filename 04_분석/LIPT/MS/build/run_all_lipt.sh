#!/bin/bash
# run_all_lipt.sh - build figures, manuscript, title page and Supplementary Material.
# Part of the analysis code for dyslipidemia-treatment-access-korea (v1.1.0, MIT license). See README.md (Pipeline) for how to run.
set -e; cd "$(dirname "$0")"; O=../out
python3 figs_lipt.py
python3 build_manuscript_lipt.py
python3 build_supplement_lipt.py
python3 sanitize_docx.py $O/Manuscript_anonymized_LIPT.docx $O/Supplementary_Material_LIPT.docx $O/Title_Page_LIPT.docx > /dev/null
for f in Manuscript_anonymized_LIPT Supplementary_Material_LIPT Title_Page_LIPT; do /opt/homebrew/bin/soffice --headless -env:UserInstallation=file:///tmp/lo_lipt_all --convert-to pdf --outdir $O $O/$f.docx > /dev/null 2>&1; done
