---
name: ingest-social
description: "Triggered when user says INGEST [url]. Extracts full text intelligence from Instagram posts (captions, image OCR, video transcriptions), classifies, cross-references with Aman's pipeline and profile, and assimilates into system — making the organism incrementally smarter with every feed."
---

# INGEST SOCIAL — The Amoeba Skill

## Core Metaphor
The system is a single-cell organism. Every INGEST is food. The amoeba consumes, digests, and integrates what is useful — then grows slightly larger, slightly smarter. Nothing is wasted. What does not fit is excreted. What fits becomes part of the body.

## Phases

### Phase 0 — Pre-Ingest Verification
1. `instaloader` available — Instagram caption extraction ready
2. `yt-dlp` + `ffmpeg` available — video download + audio extract ready
3. `faster-whisper` available — speech-to-text ready
4. `pytesseract` + `tesseract` binary — OCR ready (⚠️ optional — OCR silently skips if tesseract binary missing)
5. `data/intel/` directory exists — ingestion target
6. Master Corpus accessible — truth anchor for cross-reference
7. OneDrive path verified — dual-write active

### Phase 1 — Extract (Gather Raw Intelligence from URL)
Run ALL applicable extractors against the URL:

| Extractor | What it gets | Tool |
|-----------|-------------|------|
| **Caption** | Post text, hashtags, mentions, timestamp | `instaloader` / direct fetch |
| **Image text** | Text embedded in post images | `pytesseract` (if tesseract binary available) |
| **Video speech** | Spoken content in Reels/videos | `yt-dlp` → `ffmpeg` → `faster-whisper` |
| **Comments** | Top comments + engagement signals | `instaloader` |

**Fallback:** If no special tool works, use `webfetch` to get the public page HTML and extract what is visible.

### Phase 2 — Classify (What Kind of Intel Is This?)
Auto-detect the type of intelligence from content keywords:

| Category | Keywords That Trigger | Action |
|----------|----------------------|--------|
| **salary** | "salary", "comp", "pay", "offer", "$XXXK", "TC" | → Update compensation DB |
| **interview** | "interview", "onsite", "screen", "case study", "loop" | → Store in learned/interviews.md |
| **process** | "application", "ATS", "resume tip", "recruiter" | → Store in learned/process.md |
| **culture** | "culture", "values", "WLB", "vibe", "environment" | → Update fit_maps/[company].md |
| **company** | "DoorDash", "Indeed", "Shopify" [or any tracked company] | → Cross-reference pipeline, update fit_maps |
| **market** | "hiring freeze", "layoffs", "growth", "trend" | → Update pipeline strategy |
| **general** | Everything else | → Store data/intel/general/ for reference |

### Phase 3 — Cross-Reference (Make It Personal)
For EVERY extracted datapoint, run:

1. **Does this relate to a company in my pipeline?** → Link to that company's fit_map + current stage
2. **Does this change my approach?** → If contradicts current strategy, flag for user review
3. **Does this match my profile?** → Compare against Master Corpus — confirm or challenge current positioning
4. **Is this actionable?** → If yes → suggest specific action (update resume phrasing, change outreach angle, etc.)

### Phase 4 — Assimilate (The Amoeba Grows)
Write intelligence to system files:

| Datapoint | Written To |
|-----------|-----------|
| Salary benchmarks | `data/pipeline/COMPENSATION_DB.md` |
| Interview process tips | `data/learned/interviews.md` |
| Company DNA updates | `data/fit_maps/[COMPANY].md` |
| New keywords / language | `data/learned/keywords.md` |
| Market intelligence | `data/pipeline/market_intel.md` |
| Raw ingestion log | `data/intel/[YYYY-MM-DD]/[slug].md` |

### Phase 5 — Report (Show the Growth)
Display to user:
```
📋 INGEST SUMMARY — [URL]
━━━━━━━━━━━━━━━━━━━━━━━━
🧠 Caption:   ✅ extracted (XX chars)
🖼️ OCR:       ✅/⚠️ n images processed
🎤 Video:     ✅/⚠️ XX seconds transcribed
💬 Comments:  ✅/⚠️ n comments processed

📌 Classification: [salary | interview | culture | company | market | general]
🔗 Linked to pipeline: [Company — Role — Stage]
⚡ Actionable: [Yes/No — specific suggestion]

📁 System files updated:
  ├── data/learned/interviews.md (+1 entry)
  └── data/fit_maps/DoorDash_Canada.md (+1 cue)

🦠 Amoeba is now 0.03% smarter.
```

### Phase 6 — Git Commit
```
git add -A && git commit -m "INGEST — [URL slug] — [classification] — YYYY-MM-DD HH:MM"
```

## Commands

| Command | What It Does |
|---------|-------------|
| `INGEST [url]` | Run full pipeline: extract → classify → cross-ref → assimilate → report |
| `INGEST [url] --assimilate` | Same + auto-apply learnings (no user review gate) |
| `INGEST [url] --quick` | Caption + comments only, skip video/image processing |
| `INGEST --queue` | Show pending items that need user review before assimilation |
| `INGEST --status` | Show ingestion stats: total ingested, by category, by company |

## Dependencies

| Dependency | Required? | Install |
|-----------|-----------|---------|
| `instaloader` | Yes | `pip install instaloader` |
| `yt-dlp` | No (video skip) | `pip install yt-dlp` |
| `ffmpeg` | No (video skip) | `sudo apt install ffmpeg` |
| `faster-whisper` | No (video skip) | `pip install faster-whisper` |
| `pytesseract` | No (image skip) | `pip install pytesseract` |
| `tesseract binary` | No (image skip) | `sudo apt install tesseract-ocr` |

## Edge Cases
- **Private post?** → Report "INGEST requires public post" — skip
- **No caption, no images, no video?** → Report "No ingestible content found" — abort
- **URL is not Instagram?** → Attempt generic web fetch and extract visible text
- **Whisper very slow?** → Show progress indicator every 30s. Long videos (>5min) request user confirmation.
- **Instaloader rate limited?** → Wait 60s and retry once. If still limited, fall back to webfetch.
- **Content already ingested?** → Check data/intel/ for slug → report "Already ingested on [date]" → skip or re-ingest on user request.
