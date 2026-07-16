# ABHIMANYU 2.0: The Modular Evolution

## What This Is

**ABHIMANYU 2.0** is an AI-powered job search operating system. It works with any AI coding CLI — Claude Code, OpenCode, Codex, Gemini CLI, Qwen, Copilot, Grok.

It is the **skill-architecture upgrade** of the original JOBS-OS system. The original JOBS-OS is a monolithic operating system for job search — one AGENTS.md kernel, 40+ numbered modules, 15+ Python scripts. ABHIMANYU 2.0 preserves every bit of that alchemy but refactors into a **modular skill-as-plugin architecture** with 27 independent skills.

## Quick Install

### Option 1: npx (Recommended)

```bash
npx @ryangit711/abhimanyu init
cd ABHIMANYU-2.0
```

### Option 2: Manual

```bash
git clone https://github.com/Ryangit711/ABHIMANYU-2.0---APP.git
cd ABHIMANYU-2.0---APP
npm install
```

### Option 3: From this directory (local)

```bash
cd ABHIMANYU-2.0---APP
npm install
bash OMNI_SYNC.sh
```

## Setup

```bash
npm run doctor     # Check all prerequisites
```

Then open your AI coding tool:

```bash
opencode           # or claude, codex, gemini, qwen, etc.
```

The agent will walk you through setup on first launch — your profile, target roles, and resume — just by chatting.

## Commands

| Command | What It Does |
|---------|--------------|
| `FETCH` | Scan 41+ job boards for fresh listings |
| `SHOOT [company]` | Generate full 16-section application package |
| `EVAL` | Evaluate resume quality (10 dimensions) |
| `AUTO-APPLY [company]` | Browser-auto-submit application |
| `CONTACT [company]` | Find contacts + draft outreach |
| `NEGOTIATE [company] $offer` | Negotiation playbook |
| `TRACK` | Application pipeline status |
| `DIAGNOSE` | System health check |
| `CADENCE` | Networking cadence status |
| `LIFTOFF` | Start autonomous DAEMON mode |

## Architecture

```
ABHIMANYU-2.0/
├── AGENTS.md              ← Bootstrap kernel
├── CLAUDE.md / OPENCODE.md / CODEX.md  ← CLI entry points (@AGENTS.md)
├── .agents/skills/abhimanyu/SKILL.md   ← Skill router
│
├── skills/                ← 27 self-contained skills
│   ├── fetch-engine/      ← 8-phase job discovery
│   ├── shoot-deployer/    ← 16-section application package
│   ├── dna-extraction/    ← Company DNA analysis
│   ├── resume-writer/     ← ATS-optimized resumes
│   ├── cover-letter-writer/ ← DNA-alchemized cover letters
│   ├── interview-prep/    ← Interview cheat sheets
│   ├── networking-cadence/ ← Multi-touch outreach
│   └── ... (27 total)
│
├── scripts/               ← Python + Bash utilities
├── lib/                   ← JavaScript modules (ATS providers, filters)
├── data/                  ← Pipeline state, contacts, intel
├── eval/                  ← Quantitative test infrastructure
├── scaffolder/            ← npm installer (@ryangit711/abhimanyu)
├── doctor.mjs             ← Setup validation
├── update.mjs             ← Self-updater
└── DATA_CONTRACT.md       ← System vs user layer definition
```

## Multi-CLI Support

ABHIMANYU 2.0 is AI-agnostic. The following CLIs are supported out of the box:

- **Claude Code** — `claude`
- **OpenCode** — `opencode`
- **Codex** — `codex`
- **Gemini CLI** — `gemini`
- **Qwen Code** — `qwen`
- **GitHub Copilot CLI** — `copilot`
- **Grok Build CLI** — `grok`

Each CLI reads its own entry file (`CLAUDE.md`, `OPENCODE.md`, etc.) which all redirect to the canonical `AGENTS.md`.

## The Deal

- The machines do the typing. You do the thinking.
- **Three decisions only:** Decide which company to target, review the output, say YES or NO.
- Every skill references its JOBS-OS source files explicitly (see `REFERENCES.md`).
- Skills can be developed, tested, and improved independently.
- The endgame: payroll → paycheck → PR → freedom.

## What Comes From Where

| Component | Source |
|-----------|--------|
| All content/alchemy/format rules | `github.com/Ryangit711/JOBS-OS-2026` |
| Skill architecture pattern | `github.com/anthropics/skills` |
| Installable packaging pattern | `github.com/santifer/career-ops` |
| Eval + benchmarking infra | `github.com/anthropics/skills` |
| Document engine | `github.com/anthropics/skills` |

## License

MIT
