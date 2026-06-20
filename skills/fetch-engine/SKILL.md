---
name: fetch-engine
description: "Triggered when user says FETCH, WIDENET, or FETCH --pipe / --urls / --score. Executes continuous 24h-fresh job discovery across all 4 pipes. Every job MUST be posted within last 24 hours of command time. Stale jobs are skipped instantly and replaced from same source. Move like light."
---

# FETCH ENGINE — 8-Phase Job Discovery Pipeline

## Source Truth Anchors (JOBS-OS Primary)
- Full pipeline protocol: `AGENTS.md` → FETCH 8-PHASE PROTOCOL section
- Scoring corpus: `01_MASTER_CORPUS.md`
- ATS rules: `04_ATS_NUANCE_DB.md` + `32_ATS_TECH_SPEC.md`
- Infiltration: `37_INFILTRATION_LAYER.md`
- Consulting DNA: `CONSULTING_OS.md`
- Scripts: `33_FETCH_ENGINE.py`, `APIFY_FETCH.py`
- Exclusions: `data/jobs.json`

## Phase 0 — System Readiness
Before anything else, verify:
1. AGENTS.md loaded — kernel active
2. local_config.json exists — identity ready
3. data/jobs.json read — applied jobs excluded
4. Master Corpus accessible — truth anchor set
5. CONSULTING_OS.md accessible — consulting DNA ready
6. secrets.json exists — Apify API key available
7. APIFY_FETCH.py exists — JS fallback module loaded
8. OMNI configs synced — all tools see same rules
9. OneDrive path verified — dual-write active
10. Git remote verified — push target live

Show SYSTEM READY banner. If any check fails → warn user and stop.

## Phase 1 — Create Date Folder
- `YYYY-MM-DD/` at system root
- Subdirs: `WAVE_1/`, `WAVE_2/`, `WAVE_3/`, `CALLBACK_READY/`
- DELETE and recreate if exists (fresh start every time)
- NEVER delete `data/jobs.json` — that is permanent system memory

## Phase 2 — Websearch 4 Pipes + Apify Bulk Search (24h fresh window)
- **C PIPE (Consulting)**: EY-Parthenon, Deloitte, EY, KPMG, PwC, Accenture, MBB
- **T PIPE (Tech/Ops Core)**: Clio, Shopify, Amazon, 1Password, Tailscale, DoorDash, SaaS ops
- **I PIPE (Internal Strategy)**: lululemon, TELUS, corporate strategy, BizOps, RevOps
- **S PIPE (Startups)**: Procurify, Ada, funded Vancouver startups, chief of staff roles
- Cross-check Greenhouse boards: Brex, Hootsuite, EviSmart, Thinkific, Practice Better
- Test NEW Greenhouse slugs each run: GitLab, Zapier, Notion, Canva, Stripe, HubSpot, etc.
- Apify fallback when webfetch returns blank/truncated

## Phase 3 — Auto-Verify All URLs
- HTTP-check every listing (200=active, 404=dead, 403=caution)
- Dead → instantly replace from unculled pool (no permission needed)

## Phase 4 — Backend Due Diligence
- Score fit% against Master Corpus
- Filter: ≥60% fit, $120K+ floor, TEER 0/1, Vancouver/Remote Canada only
- Skip: government jobs (citizenship required), licensed roles (P.Eng, CPA, MD, RN), credit check roles
- Check data/jobs.json — exclude already-applied
- Quality gate: established companies only (no sketchy domains/startups with broken HR)

## Phase 5 — Write CURATED_30.md + FETCH_LOG.md
- 30 jobs, pipe-divided (C | T | I | S), sorted by fit% desc
- Each row: #, Pipe, Wave, Company, Role, Salary, Fit%, Archetype, Status

## Phase 6 — Generate CALLBACK_READY/ DNA Sheets
- One-pager per company: DNA, 60-sec pitch, 5 Q&A, 3 STAR, keywords, outreach
- Contact method column: Phone / Email / Portal (with user sleep-schedule notes)

## Phase 7 — Display
1. Full proofread table (pipe, wave, company, role, salary, fit%, ATS format, why, contact method)
2. Simplest Summary — 3-4 sentence plain-language recap
3. Command footer — full command reference

## Phase 8 — SHOOT All Jobs
- Immediately after display, execute full 13-section for EVERY unsHOT job
- One by one, full depth, shown for proofreading

## Output
- Table + summary + footer in chat
- Files in `YYYY-MM-DD/{WAVE_1,WAVE_2,WAVE_3,CALLBACK_READY}/`
- Dual-write to OneDrive
- Git push (placeholders only)
