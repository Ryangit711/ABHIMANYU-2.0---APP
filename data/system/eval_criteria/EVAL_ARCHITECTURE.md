# RESUME EVALUATOR — System Architecture

**Assimilated from:** interviewstreet/hiring-agent (HackerRank)  
**License:** MIT (original) — adapted architecture, not copied code  
**Status:** Reference architecture — implemented as LLM-prompted evaluation within existing system

---

## What We Took

| Component | Original (Hiring Agent) | Our Adaptation | Location |
|-----------|------------------------|----------------|----------|
| **Evaluation criteria** | Dev-focused: open_source, self_projects, production, technical_skills | Ops/consulting: scaling_narrative, strategic_impact, operational_depth, domain_alignment | `data/system/eval_criteria/OPS_EVAL_CRITERIA.md` |
| **Scoring engine** | Python evaluator class + LLM per-section parsing | LLM-prompted evaluation via existing skill system (Claude) — no new runtime | `skills/resume-evaluator/SKILL.md` |
| **Evidence-based scoring** | Every score point must reference source text | Same rule — provenance enforced | `OPS_EVAL_CRITERIA.md` — Provenance section |
| **Fairness constraints** | Name/gender/college/grades blind | Adapted: name-blind, institution-blind, geography-blind | `OPS_EVAL_CRITERIA.md` — built into prompts |
| **Bonus/deduction system** | Capped bonus 20, deductions unlimited | Same structure, adapted categories | `OPS_EVAL_CRITERIA.md` |
| **System message + user prompt pattern** | Separate Jinja templates for system + user | Single markdown criteria doc — loaded as context | `OPS_EVAL_CRITERIA.md` |
| **PDF → text extraction** | pymupdf_rag.py + pdf.py | NOT assimilated — our resume is already text at generation time | N/A — no need, we generate text before DOCX |
| **GitHub enrichment** | github.py | NOT assimilated — Aman is not a developer | N/A — not applicable |
| **CSV export + caching** | score.py DEV_MODE output | NOT assimilated — can add if needed but not primary flow | N/A — optional future |
| **Jinja template manager** | prompt.py + template_manager.py | NOT assimilated — AGENTS.md context already IS our prompt management | N/A — different architecture |

---

## What We Did NOT Take (And Why)

| Feature | Why Skipped |
|---------|-------------|
| Running a separate Python process | Our LLM is already in-context (Claude). Adding an external Python pipeline adds failure points and latency. Same evaluation achieved via structured SKILL.md prompt. |
| GitHub API integration | Aman's profile is operations/consulting, not software engineering. No repos to score. |
| PDF text extraction (pymupdf) | Our resume is generated as text first, then DOCX/PDF. We evaluate at TEXT stage — cleaner, faster, no PDF parsing needed. |
| Structured output parsing (Pydantic) | Our system already has NORTHSTAR format with structured sections. Adding Pydantic would require Python runtime. Can be added later if automation demands it. |
| Multi-LLM provider abstraction (Ollama/Gemini) | We have one provider (Claude). Abstracting adds complexity without benefit. If we add local LLM later, pull from Hiring Agent's models.py patterns. |

---

## Integration Points

### Point 1: Pre-Ship Quality Gate (Primary)

```
SHOOT [company] → shoot-deployer → 16 sections generated
                                     ↓
                      [NEW] resume-evaluator reads section 9 (resume text)
                                     ↓
                      Scores across 4 categories + bonus - deductions
                                     ↓
                      If PASS (≥70): proceed to quality dashboard → user review
                      If WARN (50-69): show scores + improvement suggestions
                      If FAIL (<50): block shipment, suggest rewrite, show what to change
```

This mirrors Hiring Agent's evaluation flow but runs in-claude, not as a separate Python process.

### Point 2: A/B Resume Comparison

Generate 2 resume variants → evaluate both → ship the higher scorer.

```
Section 9 variant A → evaluate → score 82
Section 9 variant B → evaluate → score 74
Ship variant A
```

### Point 3: Post-Rejection Analysis (with feedback-engine)

```
Rejection received → LEARN [company] rejection
                     → resume-evaluator re-reads the resume we shipped
                     → scores it
                     → compares score with industry standard for that company
                     → outputs specific gaps to fix
```

---

## Data Flow

```
[resume text (section 9)]
       ↓
OPS_EVAL_CRITERIA.md loaded as scoring rubric
       ↓
LLM evaluates against criteria
  ├── Per-category score + evidence
  ├── Bonus points + breakdown
  ├── Deductions + reasons
  └── Key strengths + areas for improvement
       ↓
Score calculated:
  Total = sum(categories) + bonus - deductions
  Verdict: PASS (≥70) | WARN (50-69) | FAIL (<50)
       ↓
Results displayed to user (option to iterate)
       ↓
If PASS → continue to quality dashboard (existing shoot-deployer flow)
If WARN/FAIL → show specific fixes → regenerate → re-evaluate
```

---

## File Map

| File | Purpose |
|------|---------|
| `skills/resume-evaluator/SKILL.md` | Skill instruction — how to run the evaluation |
| `data/system/eval_criteria/OPS_EVAL_CRITERIA.md` | Scoring rubric — the criteria LLM uses to score |
| `data/system/eval_criteria/EVAL_ARCHITECTURE.md` | This file — architecture reference |
| `SKILL_REGISTRY.md` | Updated to register the new skill |
| `data/system/COMMANDS_UPDATE.md` | New command aliases |

---

## Future Options (Not Built Yet — Reference Only)

- **Python scoring engine:** If we want the evaluation to run faster or more consistently, port `evaluator.py` logic as a Python script that uses structured output from the LLM
- **Historical scores CSV:** Track score trends across resume versions — mirroring Hiring Agent's `resume_evaluations.csv`
- **Competitor resume scoring:** Scrape competitor profiles → text → score against same criteria → see where we rank
- **ATS simulation layer:** Extend to simulate specific ATS platform parsing (Workday vs Greenhouse) — using source material from `04_ATS_NUANCE_DB.md` + `32_ATS_TECH_SPEC.md`
