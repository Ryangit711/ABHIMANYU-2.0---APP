# @ryangit711/abhimanyu

One-command installer for **ABHIMANYU 2.0** — the AI-powered job search operating system.

## Quick Start

```bash
npx @ryangit711/abhimanyu init
```

This clones ABHIMANYU 2.0 into `./ABHIMANYU-2.0` and installs all dependencies.

## What It Does

1. Clones the ABHIMANYU 2.0 repository
2. Installs npm dependencies
3. Bootstraps skill entrypoints for your AI CLI
4. Detects which AI coding tools you have installed

## After Installation

```bash
cd ABHIMANYU-2.0
opencode    # or claude, codex, gemini, etc.
```

Then issue commands like:
- `FETCH` — scan job boards for new listings
- `SHOOT [company]` — generate a full application package
- `EVAL` — evaluate resume quality
- `DIAGNOSE` — check system health

## Supported AI CLIs

- Claude Code
- OpenCode
- Codex
- Gemini CLI
- Qwen Code
- GitHub Copilot CLI
- Grok Build CLI

## Requirements

- Node.js >= 18
- Python 3
- git

## Optional

- `npx playwright install chromium` — for browser automation (auto-apply)
- `python-docx` — for DOCX generation (`pip install python-docx`)
