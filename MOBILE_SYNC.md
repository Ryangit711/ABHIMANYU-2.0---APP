# MOBILE SYNC — ABHIMANYU 2.0 on Termux (Android)

## Prerequisites

```bash
pkg install git python openssh
```

If opencode isn't installed yet:
```bash
pip install opencode-cli
# or follow install guide at https://opencode.ai
```

## Clone (First Time)

```bash
cd ~
git clone git@github.com:Ryangit711/ABHIMANYU-2.0.git
cd ABHIMANYU-2.0
```

If SSH key isn't set up on phone:
```bash
ssh-keygen -t ed25519 -C "phone"
cat ~/.ssh/id_ed25519.pub
# Copy output → add to GitHub: Settings → SSH and GPG keys → New SSH key
```

## Pull Latest (Every Session)

```bash
cd ~/ABHIMANYU-2.0
git pull origin main
opencode
```

## File Map (Phone Access)

| What | Where | How to Read |
|------|-------|-------------|
| Pipeline state | `data/pipeline/PIPELINE.md` | `read` or `TRACK` command |
| Today's due actions | `data/networking/CADENCE_FOOTER.md` | `CADENCE --footer` command |
| Contact tracker | `data/networking/cadence.json` | `CADENCE --dashboard` command |
| People maps (search strings) | `data/networking/PEOPLE_MAPS_BY_COMPANY.md` | Read file |
| Thought journal | `data/thought_log/YYYY-MM-DD.md` | `THOUGHT --today` |
| Kernel rules | `AGENTS.md` | Contains all permanent rules |
| This guide | `MOBILE_SYNC.md` | — |
| Master resume (DOCX) | OneDrive only (phone has own OneDrive) | Open OneDrive app |

## Session Continuity (No Chat History on Phone)

The conversation you had on PC does NOT transfer to phone. But the **file state** does. Here's how to continue:

1. `git pull origin main` — gets all PC commits
2. `STATUS` — see pipeline state
3. `TRACK` — see submissions, stages, T+ days
4. `THOUGHT --today` or `THOUGHT --last` — see what was discussed
5. `CADENCE --footer` — see due networking actions

Then pick up from the file state:
- If a SHOOT package was created but not submitted → submit it
- If a networking connect is due → send it
- If FETCH needs to run → run FETCH

## Useful Commands on Phone

```
FETCH              → Scan jobs (no browser needed for auto-fetch)
SHOOT [company]    → Build package (full 16-section, text only)
STATUS             → Full pipeline state
TRACK              → Kanban view
CADENCE --footer   → Due networking actions
THOUGHT --last     → Last 10 prompts from PC session
MANUAL-SUBMIT [co] → Generate phone submission blueprint
```

## OneDrive Access (DOCX Files)

Phone has its own OneDrive app. The same `ABHIMANYU-2.0/YYYY-MM-DD/CompanyName/` structure lives there. DOCX files are OneDrive-only (not in git).

## Resume Source (Markdown)

The DOCX master resume was generated from `JOBS-OS-2026/00_RESUME_MASTER.md`. Read/edit the markdown source on phone if needed; regenerate DOCX when back on PC.

## Quick Start

```bash
cd ~/ABHIMANYU-2.0 && git pull && opencode
# Then: STATUS → TRACK → see what's due → execute
```
