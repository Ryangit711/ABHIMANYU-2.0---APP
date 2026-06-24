# SYSTEM SOURCES — QBIT 1 Sweep Registry

## Primary Job Boards (Sweep Every FETCH — 13 Total)
- **Indeed** — indeed.ca — general job board, broadest coverage
- **LinkedIn** — linkedin.com/jobs — professional network, company pages
- **Glassdoor** — glassdoor.ca — salary data + job listings
- **Workopolis** — workopolis.com — Canadian-focused
- **Jooble** — jooble.ca — aggregator, catches cross-posted roles
- **Google Jobs** — google.com/search?q=jobs — aggregator, surfaces roles from all boards
- **Hiring Cafe** — hiring.cafe — curated tech/startup roles
- **Eluta.ca** — eluta.ca — aggregates directly from company career pages (finds hidden roles)
- **SimplyHired** — simplyhired.ca — aggregator, different coverage from Indeed
- **Monster Canada** — monster.ca — legacy board, unique corporate listings
- **ZipRecruiter** — ziprecruiter.ca — aggregator, strong for US-in-Canada roles
- **Otta** — otta.com — curated tech/startup roles at scale-ups
- **BCjobs.ca** — bcjobs.ca — BC-specific corporate and local roles

## Company Career Pages (Sweep Per Pipe)

### T PIPE (Tech/BigTech)
- Clio — clio.com/about/careers
- Shopify — shopify.com/careers
- Amazon — amazon.jobs
- 1Password — 1password.com/jobs
- Tailscale — tailscale.com/careers
- DoorDash — doordash.com/careers
- Indeed — indeed.com/careers
- Jobber — jobber.com/careers

### I PIPE (Internal Strategy/Corporate)
- lululemon — lululemon.com/careers
- TELUS — telus.com/careers
- Vancity — vancity.com/careers
- Methanex — methanex.com/careers
- Providence Healthcare — providencehealthcare.org/careers
- BC Cancer — bccancer.bc.ca/careers
- Aritzia — aritzia.com/careers
- Arc'teryx — arcteryx.com/careers

### C PIPE (Consulting)
- Deloitte — deloitte.com/careers
- EY — ey.com/careers
- KPMG — kpmg.com/careers
- PwC — pwc.com/careers
- Accenture — accenture.com/careers
- MBB (McKinsey, BCG, Bain) — respective career portals

### S PIPE (Startups)
- Procurify — procurify.com/careers
- Ada — ada.com/careers
- Hiive — hiive.com/careers
- EvenUp — evenup.com/careers
- Practice Better — practicebetter.com/careers
- Thinkific — thinkific.com/careers
- EviSmart — evismart.com/careers
- Brex — brex.com/careers

## Greenhouse Boards (Check All Each FETCH)
- Greenhouse common: Brex, Hootsuite, EviSmart, Thinkific, Practice Better
- Test new slugs each run: GitLab, Zapier, Notion, Canva, Stripe, HubSpot

## ATS Tech Spec Reference (JOBS-OS Vault)
- Per-platform ATS parsing rules: `32_ATS_TECH_SPEC.md` in JOBS-OS vault
  - Greenhouse: DOCX, Arial/Calibri, 10-12pt, 0.75-1in margins, single column, no headers
  - Workday: DOCX, Arial/Calibri/Times New Roman, 10-12pt, contact info in body (not header)
  - Lever: DOCX, Liberation Sans/Calibri, 10-11pt, 0.75in margins, simple section headers
  - ICIMS: DOCX preferred, standard fonts, single column, no tables
  - SAP SuccessFactors: DOCX, Calibri 10-11pt, generic section headers
- Cross-reference gen_docx.py CONFIG before generating any DOCX

## Apify Fallback
- When webfetch returns blank/truncated, use APIFY_FETCH.py

## Community Intel
- Reddit — r/vancouverjobs, r/cscareerquestions, r/consulting, r/startups
- X.com — finance/startup job posts

---

## Dedup + ATS Feasibility + Route Guidance Protocol

### Phase 2b — Dedup (Same Job on Multiple Sources)
Every job found across multiple sources is collapsed into ONE entry. The FETCH table shows each job once. Dedup key: company name + role title + location must match (approximate fuzzy match — same company + same role level = same job even if title has minor variation).

### Phase 2c — ATS Feasibility Check
For each dedup'd job, identify company's ATS platform. Cross-reference against ATS Tech Spec section above:

| ATS | DOCX Pass? | Gotcha | Risk |
|-----|-----------|--------|------|
| **Greenhouse** | ✅ Yes | Liberation Sans/Calibri 10-11pt, 0.75in margins | Low |
| **Workday** | ✅ Yes (with care) | Contact info MUST be in body (not header). Arial/Calibri only | Medium — header content skipped |
| **Oracle Cloud** | ✅ Yes | Calibri 11pt, 0.75in margins, simple section headers | Low |
| **Lever** | ✅ Yes | Liberation Sans/Calibri 10-11pt, no tables | Low |
| **ICIMS** | ✅ Yes | Standard fonts, single column | Low |
| **SAP SuccessFactors** | ✅ Yes | Calibri 10-11pt, generic headers | Low |
| **Taleo** | ⚠️ Caution | Legacy — prefers DOCX, can mangle formatting | Medium — test before submit |
| **BambooHR** | ✅ Yes | Standard DOCX works | Low |
| **Unknown** | ⚠️ Verify | Use DOCX with generic format (Calibri 11pt, 0.75in, no headers) | Flag for manual check |

Flag: ✅ Pass / ⚠️ Verify (format spec check needed) / ❌ Blocked (with reason + fix)

### Phase 2d — Route Guidance
For each job, determine best application route. Priority:

1. **Company career page** (best — direct feed, no third-party filter)
2. **ATS direct portal** (Workday/Greenhouse/Oracle direct URLs — skip middleman)
3. **LinkedIn Easy Apply** (only if career page doesn't exist or is broken)
4. **Primary board** (Indeed/Google Jobs/SimplyHired — general, acceptable fallback)
5. **Third-party board** (Workopolis/ZipRecruiter — lowest priority)

**Rule:** If job found on career page AND on Indeed → recommend career page. If only on Indeed → recommend Indeed. If only on Otta/Hiring Cafe → that's a direct-source board, recommend that source.

Add column to FETCH table: **Apply Via** — one of "Company site", "ATS portal", "LinkedIn", "Indeed", "Otta", "Hiring Cafe", "[Board name]"

---

## Add/Remove Protocol
- **Add:** Append to relevant section above + update AGENTS.md QBIT 1 inline list
- **Remove:** Delete from relevant section + update AGENTS.md QBIT 1 inline list
- **Reason for change** must be logged in data/thought_log/
