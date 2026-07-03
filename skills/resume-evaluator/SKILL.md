---
name: resume-evaluator
description: "Pre-ship content quality gate. Evaluates a generated resume text (section 9) against ops/consulting scoring criteria — the way a recruiter would in 6 seconds. Scores across 4 dimensions, returns evidence-based verdict. Designed to sit between resume generation (resume-writer) and the existing quality gates (ATS validation, bullet quality, anti-pattern sweep) in the shoot-deployer pipeline."
---

# RESUME EVALUATOR — Content Quality Gate

**Source:** Adapted from interviewstreet/hiring-agent (HackerRank) evaluation framework — dev-focused criteria rearchitected for operations/consulting resumes.

---

## Core Purpose

Our existing 4 quality gates check FORMAT (ATS compliance, bullet structure, anti-patterns, semantic enrichment). This gate checks SUBSTANCE — does the resume actually tell a compelling story to a hiring manager?

---

## When to Run

| Trigger | When |
|---------|------|
| `SHOOT [company]` | Auto-run after section 9 is generated, before quality dashboard |
| `EVAL` | Manual trigger to re-evaluate an existing resume against criteria |
| `EVAL --compare [variant1] [variant2]` | A/B test two resume versions |
| `EVAL --target [company]` | Evaluate resume specifically for a target company alignment |

---

## Execution Protocol

### Step 1: Load Criteria

```
READ data/system/eval_criteria/OPS_EVAL_CRITERIA.md
  → 4 scoring categories with bands
  → Bonus points table (max 20)
  → Deductions table (no cap)
  → Pass/Warn/Fail thresholds
```

### Step 2: Load Resume Text

Use the generated resume from section 9 of the current SHOOT package. This is plain text — no PDF parsing needed (our resumes are text-first, DOCX-second).

If running standalone (`EVAL` without active SHOOT), ask user to paste the resume text.

### Step 3: Evaluate Against Criteria

Run the LLM evaluation with the criteria as system context and resume text as input. Score each category with evidence:

```
CRITERIA:
  scaling_narrative  (0-35) — growth arc, trajectory, scope increase
  strategic_impact   (0-30) — P&L, board, M&A, transformation
  operational_depth  (0-25) — systems built, tech led, teams managed
  domain_alignment   (0-10) — company language, pipe positioning, archetype

BONUS (max 20):
  +5 quantified exit
  +3 founder narrative
  +3 MBA applied
  +2 cross-industry
  +2 border-spanning
  +1/ea board mention
  (capped at 20 total)

DEDUCTIONS:
  -5 immigration/PR language
  -3 per vague bullet
  -2 per missing metric
  -3 archetype drift
  -3 weak summary
  -3 missing quantified exit

EVIDENCE REQUIRED: Every score point must cite specific resume text.
```

### Step 4: Calculate Verdict

```
Sum = scaling_narrative + strategic_impact + operational_depth + domain_alignment
Total = Sum + bonus - deductions

PASS  (≥70):  "Recruiter puts this in the YES pile. Ready for quality dashboard."
WARN  (50-69): "MAYBE pile. These specific gaps identified → [list]. Iterate before dashboard?"
FAIL  (<50):  "NO pile. Rewrite before shipping. Here's what's wrong: [specific issues]."
```

### Step 5: Output

```
╔══════════════════════════════════════════════════════════════════════╗
║  📊 RESUME EVALUATION                                              ║
╠══════════════════════════════════════════════════════════════════════╣
║  Scaling Narrative:  28/35  — Clear 3→70→$17M arc                  ║
║  Strategic Impact:   22/30  — Board + M&A evidence present          ║
║  Operational Depth:  20/25  — Systems built, tech led, teams grown  ║
║  Domain Alignment:    7/10  — 3/6 keywords from language registry   ║
║  ─────────────────────────────────────────────────────────────       ║
║  Category Total:     77/100                                         ║
║  Bonus:             +13/20  (+5 exit, +3 founder, +3 MBA, +2 cross) ║
║  Deductions:          -3    (1 vague bullet)                        ║
║  ─────────────────────────────────────────────────────────────       ║
║  **TOTAL SCORE: 87/120 — PASS ✅**                                  ║
║  Verdict: Recruiter YES pile. Ready to ship.                        ║
╚══════════════════════════════════════════════════════════════════════╝

✅ KEY STRENGTHS
  1. Compelling scaling narrative dominates the resume
  2. Strategic impact visible through board and M&A examples
  3. Tech transformation story differentiates from pure ops candidates

🔧 AREAS FOR IMPROVEMENT
  1. Bullet under Company Y: "responsible for operations" → rewrite with metrics or scope
  2. Add 2-3 more language registry keywords for tighter domain alignment
  3. $17M exit should be stated explicitly, not implied

Suggested rewrites for flagged items → see below.
```

---

## Integration with Shoot-Deployer

This skill is designed to run BEFORE the existing quality dashboard (ATS validation + bullet quality + anti-pattern sweep + semantic enrichment).

The full flow with resume-evaluator becomes:

```
  1. GENERATE 16 sections (existing shoot-deployer)
  2. [NEW] RUN RESUME EVALUATOR on section 9
     → If FAIL: block, show specific fixes, regenerate section 9
     → If WARN: show warnings, offer to iterate or proceed
     → If PASS: continue
  3. RUN ATS VALIDATION PASS (existing Step G1)
  4. RUN BULLET QUALITY UPGRADE (existing Step G2)
  5. RUN ANTI-PATTERN SWEEP (existing Step G3)
  6. RUN SEMANTIC ENRICHMENT (existing Step G5)
  7. SHOW QUALITY DASHBOARD (existing Step G4) — now includes eval score
  8. PRESENT for user review
```

The resume-evaluator does not replace any existing gate. It adds a content-substance check before the existing format-level checks.

---

## Comparison: This Gate vs Existing Gates

| Aspect | Existing Gates (G1-G5) | Resume Evaluator (NEW) |
|--------|----------------------|------------------------|
| **What it checks** | Format, structure, weasel words, ATS compliance, JSON-LD | Content quality, narrative strength, recruiter appeal |
| **How it scores** | Binary pass/fail per check | Graduated score (0-120) with evidence |
| **What it catches** | Wrong font, missing metrics, weak verbs, archetype drift | Flat story, weak positioning, missing exit, domain misalignment |
| **What it outputs** | ✅/⚠️/❌ per check | Score + verdict + specific improvement suggestions |
| **When it runs** | After content generation, before user review | After content generation, BEFORE other gates (gate 0) |

---

## Source Truth Anchors

- Evaluation criteria: `data/system/eval_criteria/OPS_EVAL_CRITERIA.md`
- Architecture reference: `data/system/eval_criteria/EVAL_ARCHITECTURE.md`
- Resumes evaluated: section 9 of SHOOT package (plain text)
- Score history (optional): `data/system/eval_criteria/SCORE_HISTORY.md` — created on first use
