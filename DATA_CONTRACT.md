# DATA_CONTRACT.md — System vs User Layer

ABHIMANYU 2.0 has two layers. The **system layer** is auto-updated and versioned. The **user layer** is personal data that must never be touched by updaters.

## System Layer (auto-updatable)

These files are part of the ABHIMANYU 2.0 distribution and can be updated by `update.mjs`:

```
AGENTS.md
CLAUDE.md
OPENCODE.md
CODEX.md
GEMINI.md
SKILL_REGISTRY.md
BIRDS_EYE.md
COMMANDS.md
MASTER_USER_MANUAL.md
REFERENCES.md
TIMELINE.md
HARD_KERNEL_RULE_*.md
README.md
DATA_CONTRACT.md
doctor.mjs
update.mjs
package.json
.scripts/
scripts/gen_docx.py
scripts/auto_apply.py
scripts/ats_scorer.py
scripts/ingest_engine.py
scripts/semantic_enricher.py
scripts/gen_master_resume.py
scripts/gen_indeed_docx.py
scripts/gen_merged_pdf.py
scripts/gen_app_pdf.py
scripts/resume_docx_builder.py
scripts/DAEMON.sh
scripts/update_cadence.sh
scripts/cadence_ctl.sh
skills/
eval/
lib/
template/
spec/
.agents/
```

## User Layer (NEVER auto-updated)

These files contain personal data, configuration, or generated output. They are yours and yours alone:

```
Master_Resume.md
Master_Resume_ATS_CLEAN.md
local_config.json
secrets.json
data/jobs.json
data/contacts.json
data/networking/
data/cadence.json
data/pipeline/
data/learned/
data/fit_maps/
data/intel/
data/thought_log/
data/shoot/
data/daemon/
data/summary/
data/rankings/
data/system/
data/platforms/
data/linkedin/
data/shoot/
data/submission/
2026-*/
ANCHORED_SUMMARY.md
MOBILE_SYNC.md
OMNI_SYNC.sh
_gen_docx_batch.py
```

## The Rule

The updater (`update.mjs`) uses this contract to determine which files it may touch. It will **never** modify, delete, or overwrite files in the user layer. If an update would require changing a user-layer file, the updater will warn and skip it.
