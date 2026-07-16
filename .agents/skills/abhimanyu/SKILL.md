---
name: abhimanyu
description: AI job search operating system — FETCH jobs, SHOOT application packages, EVAL resumes, AUTO-APPLY, and manage your entire pipeline
arguments: command
user_invocable: true
user-invocable: true
argument-hint: "[FETCH | SHOOT [company] | EVAL | AUTO-APPLY [company] | DIAGNOSE | STATUS | CONTACT | NEGOTIATE | TRACK | PING | PATTERNS | LEARN | INGEST [url] | CADENCE | SKILL CREATE | SKILL IMPROVE | LIFTOFF]"
license: MIT
---

# ABHIMANYU 2.0 — Router

ABHIMANYU 2.0 is a multi-CLI job-search operating system. The routing below is shared across all supported AI coding CLIs.

## Invocation Notes

- CLIs with slash-command registration can expose this router as `/abhimanyu`.
- Interactive sessions use natural language — the agent reads AGENTS.md and routes accordingly.
- The routing semantics stay the same regardless of the entrypoint.

Examples:

```text
FETCH                        → Scan job boards for new listings
SHOOT Methanex               → Generate full application package for Methanex
SHOOT Indeed --all           → Generate packages for all Indeed roles
EVAL                         → Evaluate latest resume output
AUTO-APPLY Methanex          → Browser-auto-apply to Methanex
DIAGNOSE                     → System health check
STATUS                       → Show pipeline status
CONTACT Methanex             → Find contacts at Methanex
NEGOTIATE Methanex 120000    → Negotiation playbook
TRACK                        → Show application tracker
PING                         → DAEMON heartbeat check
PATTERNS                     → Analyze rejection patterns
LEARN Indeed success 85      → Record outcome lesson
INGEST https://instagram.com/... → Extract social intelligence
CADENCE                      → Show networking cadence
SKILL CREATE something       → Create a new skill
SKILL IMPROVE resume-writer  → Improve an existing skill
LIFTOFF                      → Start autonomous DAEMON mode
```

## Mode Routing

Determine the mode from `$command`:

| Input | Mode | Skill to Load |
|-------|------|---------------|
| (empty / no args) | `discovery` — Show command menu | — |
| `FETCH`, `WIDENET`, `SCAN` | Job discovery pipeline | `skills/fetch-engine/SKILL.md` |
| `SHOOT [company]` | Full application package | `skills/shoot-deployer/SKILL.md` |
| `ATOMIZE [company]` | Company DNA extraction | `skills/dna-extraction/SKILL.md` |
| `SCORE [company]` | Score company fit | `skills/dna-extraction/SKILL.md` |
| `ALCHEMIZE` | Resume + cover letter polish | `skills/resume-writer/SKILL.md` + `skills/cover-letter-writer/SKILL.md` |
| `EVAL` | Resume quality evaluation | `skills/resume-evaluator/SKILL.md` |
| `AUTO-APPLY [company]` | Browser automation submit | `skills/browser-automation/SKILL.md` |
| `AUTO-APPLY --manual [company]` | Phone fallback blueprint | `skills/manual-submit/SKILL.md` |
| `DIAGNOSE`, `REFRESH`, `STATUS` | System health | `skills/system-health/SKILL.md` |
| `CONTACT`, `CONTACT LIST` | Contact management | `skills/contact-engine/SKILL.md` |
| `NEGOTIATE [company] [offer]` | Salary negotiation | `skills/negotiation-playbook/SKILL.md` + `skills/salary-negotiation/SKILL.md` |
| `TRACK`, `AUDIT` | Pipeline tracker | `skills/pipeline-tracker/SKILL.md` |
| `PING`, `DAEMON START`, `LIFTOFF` | Autonomous daemon | `skills/daemon/SKILL.md` |
| `PATTERNS` | Pattern analysis | `skills/pattern-analyzer/SKILL.md` |
| `LEARN [company] [outcome] [score]` | Record lesson | `skills/feedback-engine/SKILL.md` |
| `INGEST [url]` | Social intelligence | `skills/ingest-social/SKILL.md` + `skills/social-distill/SKILL.md` |
| `CADENCE` | Networking cadence | `skills/networking-cadence/SKILL.md` |
| `LINKEDIN CONNECT/INBOX/SEARCH` | LinkedIn automation | `skills/linkedin-automation/SKILL.md` |
| `SKILL CREATE [name]` | Create new skill | `skills/skill-creator/SKILL.md` |
| `SKILL IMPROVE [name]` | Improve existing skill | `skills/skill-creator/SKILL.md` |
| `GENPDF` | PDF generation | `skills/pdf-generator/SKILL.md` |

**Auto-detection:** If `$command` is not a known sub-command AND contains JD text (keywords: "responsibilities", "requirements", "qualifications", "about the role", "we're looking for") or a URL to a JD, execute the **SHOOT** workflow with auto-DNA extraction.

If `$command` is not a sub-command AND doesn't look like a JD, show discovery.

---

## Discovery Mode (no arguments)

Show this menu:

```
ABHIMANYU 2.0 — Command Center

Available commands:
  FETCH                      → Scan 41+ job boards for fresh listings
  SHOOT [company]            → Generate full 16-section application package
  SHOOT [company] --all      → Generate packages for all roles at company
  EVAL                       → Evaluate resume quality (10 dimensions)
  AUTO-APPLY [company]       → Browser-auto-submit application
  CONTACT [company]          → Find contacts + draft outreach
  NEGOTIATE [company] $offer → Negotiation playbook
  TRACK                      → Application pipeline status
  DIAGNOSE                   → System health check
  PING                       → DAEMON heartbeat
  PATTERNS                   → Analyze rejection patterns
  LEARN [co] [outcome] $sc   → Record lesson learned
  INGEST [url]               → Extract social intelligence
  CADENCE                    → Networking cadence status
  SKILL CREATE [name]        → Create a new skill
  SKILL IMPROVE [name]       → Improve an existing skill
  LIFTOFF                    → Start autonomous DAEMON mode

The machines do the typing. You do the thinking.
  1. Decide which company to target
  2. Review the output
  3. Say YES or NO
```

---

## Context Loading by Mode

After determining the mode, load the necessary files before executing:

### Skills loaded on-demand

Each skill is loaded from `skills/{name}/SKILL.md` when triggered. The SKILL.md contains:
- YAML frontmatter (name, description, triggers)
- Full protocol instructions
- Cross-skill wiring (which other skills to invoke)
- Quality gates and validation rules

### Shared context

Before executing any mode, the agent should have already loaded:
- `AGENTS.md` — The kernel (boot sequence, rules, philosophy)
- `SKILL_REGISTRY.md` — Index of all available skills
- `BIRDS_EYE.md` — System architecture map

### User-layer files (loaded when relevant)

- `data/jobs.json` — Pipeline state
- `data/cadence.json` — Networking cadence
- `Master_Resume.md` — Master resume content
- `Master_Resume_ATS_CLEAN.md` — ATS-cleaned resume
- `local_config.json` — User-specific configuration
- `secrets.json` — API keys and tokens
