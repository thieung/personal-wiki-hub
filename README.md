# personal-wiki-hub

[English](README.md) | [Tiếng Việt](README.vi.md)

LLM-maintained personal knowledge base following the [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), extended with production patterns from [rohitg00's agentmemory architecture](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2). Designed for Claude Code with Obsidian as the human interface.

## Quick Start

```bash
# Verify vault structure
/wiki:setup --verify

# Capture and ingest a source in one step
/wiki:capture https://example.com/article --ingest

# Browse what's in the wiki
/wiki:browse

# Ask the wiki a question
/wiki:query "What is the Karpathy LLM wiki pattern?"

# Check health
/wiki:status
```

**First time?** See [INSTALLATION.md](INSTALLATION.md) for step-by-step setup guide.

## Architecture

```
personal-wiki-hub/
├── raw/               # External sources (immutable, user drops)
│   ├── assets/        # Images attached to sources
│   └── archive/       # Unprocessed items >30 days
├── wiki/              # LLM-maintained knowledge (auto-generated)
│   ├── assets/        # LLM-generated diagrams
│   ├── index.md       # Content catalog
│   ├── log.md         # Operation log (append-only)
│   └── backlog.md     # Concepts pending promotion
├── notes/             # User-owned thinking (LLM reads only)
│   ├── daily/         # Daily journal entries
│   ├── fleeting/      # Quick captures, inbox
│   ├── reviews/       # Weekly review notes
│   └── assets/        # Personal diagrams
├── outputs/           # LLM-generated answers, reports, research
│   ├── answers/       # Q&A results worth keeping
│   ├── reports/       # Analysis reports
│   └── research/      # Research synthesis
├── projects/          # Code-driven project knowledge
│   └── <project>/     # Per-project: knowledge/, decisions/, ops/
├── content/           # Blog drafts
├── sessions/          # Auto-exported Claude Code session logs
├── templates/         # Frontmatter templates (daily, weekly, wiki, fleeting)
├── .claude/
│   ├── agents/        # wiki-* subagents (5)
│   └── skills/        # wiki-* skills (11)
└── CLAUDE.md          # Schema governance
```

**Full structure details:** See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

## Skills Reference (11 skills)

**Location:** `.claude/skills/wiki-*` (project-local)

### /wiki:capture — Capture external sources

Fetches content from any source type and saves to `raw/`. Auto-detects source type and applies appropriate extraction.

```bash
# Web article
/wiki:capture https://example.com/article

# GitHub repo (uses gh CLI for README + structure)
/wiki:capture https://github.com/user/repo

# YouTube video (extracts transcript via yt-dlp)
/wiki:capture https://youtube.com/watch?v=xxx

# PDF document (uses ai-multimodal for extraction)
/wiki:capture /path/to/document.pdf

# Clipboard content (uses pbpaste on macOS)
/wiki:capture --clipboard

# Capture + immediately ingest into wiki (pipeline shortcut)
/wiki:capture https://example.com/article --ingest

# Custom title override
/wiki:capture https://example.com/article --title "Custom Title"
```

| Option | Description |
|--------|-------------|
| `<source>` | URL, file path, or `--clipboard` |
| `--ingest` | Pipeline shortcut: capture + ingest in one step |
| `--title "..."` | Override auto-detected title |
| `--clipboard` | Capture from system clipboard |

**Source type auto-detection:**

| Source | Detection | Method |
|--------|-----------|--------|
| Web article | `https://` (non-GitHub, non-YouTube) | `WebFetch` → markdown |
| GitHub repo | `github.com/` URL | `gh` CLI for README + structure |
| YouTube | `youtube.com/` or `youtu.be/` | `yt-dlp` for transcript |
| PDF | `.pdf` extension | `ai-multimodal` skill |
| Local file | File path exists | Copy to `raw/` |
| Clipboard | `--clipboard` flag | `pbpaste` (macOS) |

**Security:** HTTPS only, rejects RFC1918/loopback/cloud metadata endpoints.

**Use cases:**
- Capture a blog post you found interesting for later wiki synthesis
- Save a GitHub repo's architecture for project comparison
- Grab a YouTube talk transcript to extract key decisions
- Quick-capture a clipboard snippet during research

---

### /wiki:ingest — Process sources into wiki

Reads raw sources, classifies content, and extracts knowledge into typed wiki pages with full frontmatter, provenance tracking, and cross-references.

```bash
# Ingest a single source
/wiki:ingest raw/article-name.md

# Ingest from URL (saves to raw/ first, then ingests)
/wiki:ingest https://example.com/article

# Batch ingest all unprocessed raw files
/wiki:ingest raw/*.md
```

| Option | Description |
|--------|-------------|
| `<source>` | File path in `raw/`, URL, or glob pattern |

**What happens:** Classifies source type → extracts entities/concepts → creates/updates wiki pages with frontmatter, TLDR, counter-arguments → updates index.md + log.md → computes source SHA-256 hashes for provenance tracking → increments ingest counter.

**Source classification:**

| Type | Extraction approach |
|------|-------------------|
| Report/whitepaper | Section-by-section, exec summary first |
| Paper | Method + findings |
| Transcript | Speaker attribution, decisions, action items |
| Article/blog | Key claims + evidence |
| Thread/tweet | Core insight + context |
| Code repo | Architecture + patterns + dependencies |

**Use cases:**
- Process a captured research paper into entity + concept pages
- Batch-ingest a folder of articles after a research session
- Ingest directly from URL when you don't need the raw file separately
- After ingest count reaches 5, auto-suggests running `/wiki:audit`

**Agent:** `wiki-ingestor` (`.claude/agents/wiki-ingestor.md`)

---

### /wiki:query — Search and answer from wiki

Searches wiki using progressive disclosure (L0→L3) for token efficiency. Follows typed relations for connected knowledge.

```bash
# Basic question
/wiki:query "What orchestration patterns does Rowboat use?"

# Force save answer to outputs/
/wiki:query "Compare DDD vs clean architecture" --save

# Deep mode — reads linked raw sources for fact-checking
/wiki:query "Is Rowboat's MCP integration production-ready?" --deep

# Limit search scope to a specific project
/wiki:query "billing domain events" --scope projects/ejar3

# Save answer as permanent wiki page (type: query-result)
/wiki:query "MCP vs direct API tradeoffs" --file-back
```

| Option | Description |
|--------|-------------|
| `<question>` | Natural language question |
| `--save` | Force save to `outputs/answers/` |
| `--deep` | L3 disclosure: read linked raw sources for verification |
| `--scope <dir>` | Limit search to directory (e.g., `projects/ejar3`) |
| `--file-back` | Save as wiki page (type: query-result) |

**Progressive disclosure levels:**
- **L0:** Index TLDRs only — fastest, cheapest. Most queries start here.
- **L1:** Candidate page headings — narrows to relevant sections
- **L2:** Full page body — standard depth for most answers
- **L3:** Page + all linked raw sources — deepest, for fact-checking claims

**Side effects:** Bumps `last_queried:` on every wiki page used to answer (via wiki-librarian).

**Use cases:**
- Quick lookup: "What is X?" → L0-L1 resolves instantly
- Comparison: "How does X compare to Y?" → L2 with `--save` for reuse
- Fact-check: "Is claim X accurate?" → `--deep` reads original raw sources
- Knowledge promotion: Good answer → `--file-back` makes it a permanent wiki page

**Agent:** `wiki-librarian` (`.claude/agents/wiki-librarian.md`)

---

### /wiki:browse — Navigate wiki content

Discover and navigate pages by type, tag, keyword, or recency. Reads frontmatter only for token efficiency.

```bash
# Full browse — all pages grouped by type with TLDRs
/wiki:browse

# Filter by tag
/wiki:browse --tag multi-agent

# Filter by page type
/wiki:browse --type entity

# Keyword search across titles and TLDRs
/wiki:browse --search "orchestration"

# Recently updated or queried pages (last 7 days)
/wiki:browse --recent 7

# Filter by confidence level
/wiki:browse --confidence low

# Show only stale pages needing attention
/wiki:browse --stale
```

| Option | Description |
|--------|-------------|
| *(no args)* | Full browse: all pages grouped by type |
| `--tag <tag>` | Filter pages by a specific tag |
| `--type <type>` | Filter by page type (entity, concept, insight, etc.) |
| `--search <keyword>` | Keyword search across page titles and TLDRs |
| `--recent <days>` | Pages updated or queried within N days (default: 30) |
| `--confidence <level>` | Filter by confidence level (low, medium, high) |
| `--stale` | Show only stale pages needing refresh |

**Distinct from `/wiki:query`:** browse = navigation ("what pages exist about X?"), query = answering ("what does X mean?").

**Use cases:**
- Explore what knowledge exists before starting a new project
- Find all low-confidence pages that need additional sources
- List stale pages before a weekly maintenance session
- Search for pages related to a keyword before ingesting a new source (avoid duplicates)
- Review recently queried pages to identify frequently-used knowledge

**Runs inline** — no agent delegation, uses Grep + Glob + index.md directly.

---

### /wiki:synthesize — Cross-page analysis

Finds connections, patterns, contradictions, and insights across multiple wiki pages. Produces new wiki pages or research reports.

```bash
# Topic-based synthesis
/wiki:synthesize "orchestration patterns"

# Synthesize from specific pages
/wiki:synthesize --pages wiki/rowboat.md wiki/karpathy-llm-wiki-pattern.md wiki/llm-wiki-best-practices.md

# Full wiki scan — discover connections across all pages
/wiki:synthesize
```

| Option | Description |
|--------|-------------|
| `[focus]` | Topic or question to synthesize around (optional) |
| `--pages <paths>` | Specific pages to synthesize from |

**Requires minimum 3 source pages.** Produces:
- Comparison page → `wiki/` (type: comparison)
- Insight page → `wiki/` (type: insight)
- Research report → `outputs/research/`

**Quality rules:**
- Concrete noun test: output must have a clear, referenceable title
- Contradictions between pages surfaced as primary value
- Cross-references updated in all source pages

**Use cases:**
- After ingesting 5+ sources on a topic: synthesize to find patterns
- Compare competing tools/approaches across multiple entity pages
- Discover hidden connections between seemingly unrelated concepts
- Generate a comparison page before making a technology decision

**Agent:** `wiki-synthesizer` (`.claude/agents/wiki-synthesizer.md`)

---

### /wiki:audit — Health check

Structural and content quality audit of wiki and notes. Can auto-fix safe issues in wiki/.

```bash
# Report only (default — no modifications)
/wiki:audit

# Auto-fix safe issues in wiki/
/wiki:audit --fix

# Audit wiki only (skip notes/)
/wiki:audit --wiki-only

# Audit notes only (always report-only, never modifies)
/wiki:audit --notes-only

# Audit a single page
/wiki:audit --page wiki/rowboat.md
```

| Option | Description |
|--------|-------------|
| `--fix` | Auto-fix safe issues in wiki/ |
| `--wiki-only` | Only audit wiki/ directory |
| `--notes-only` | Only audit notes/ (report-only) |
| `--page <path>` | Single page audit |

**Checks performed:**

| Category | Checks |
|----------|--------|
| Structural | Missing frontmatter fields, broken `[[wikilinks]]`, orphan pages, duplicate titles |
| Staleness | Pages >60 days old AND not queried within 30 days → stale |
| Content quality | Missing TLDR, missing counter-arguments, anti-cramming/thinning violations |
| Provenance | Source hash drift (raw file changed after wiki compiled), sources not in raw/ |
| Supersession | `superseded_by:` ↔ `supersedes:` bidirectional integrity |
| Source coverage | Raw files not cited in any wiki page's `sources:` (unprocessed detection) |
| Index | Pages not in index, index entries pointing to non-existent pages, tag inconsistency |
| Archival | Pages with `last_queried:` >90 days and `confidence: low` → candidates |

**Auto-fixable (with `--fix`):** Missing sections (TLDR template, counter-arguments), index sync, stale status marking, missing status/confidence fields.

**Report-only (never auto-fix):** Content quality judgments, broken wikilinks, notes/ issues, duplicate resolution.

**Auto-trigger:** Runs automatically when ingest counter in CLAUDE.md reaches >=5.

**Use cases:**
- Weekly maintenance: `/wiki:audit --fix` to clean up accumulated issues
- Pre-synthesis check: audit before synthesizing to ensure data quality
- After bulk ingest: verify all new pages meet schema requirements
- Single page deep-check before sharing or referencing

**Agent:** `wiki-auditor` (`.claude/agents/wiki-auditor.md`) — Write/Edit tools only active with `--fix`.

---

### /wiki:refresh — Update stale pages

Refreshes content of existing wiki pages — verifies claims against sources, optionally researches new data. Always proposes diff before applying.

```bash
# Refresh single page (proposes diff, doesn't auto-apply)
/wiki:refresh wiki/rowboat.md

# Refresh with fresh web research
/wiki:refresh wiki/rowboat.md --research

# Re-read all cited raw sources before refreshing
/wiki:refresh wiki/rowboat.md --all-sources

# Combine: re-read sources + web research
/wiki:refresh wiki/rowboat.md --research --all-sources

# Batch: refresh all pages stale >60 days
/wiki:refresh --stale 60

# Batch with custom threshold (30 days)
/wiki:refresh --stale 30
```

| Option | Description |
|--------|-------------|
| `<page.md>` | Wiki page path (required unless `--stale`) |
| `--research` | Fresh web research to supplement existing sources |
| `--all-sources` | Re-read all cited raw/ files before refreshing |
| `--stale <days>` | Batch mode: all pages older than N days (default 60) |

**Safety:** Single page always proposes diff first — never auto-applies. Batch mode asks confirmation before starting. History preserved via git.

**Use cases:**
- A tool you documented has released a major update: `--research` to pull in new info
- Source hash drift detected by audit: `--all-sources` to re-read and reconcile
- Monthly maintenance: `--stale 60` to batch-refresh aging pages
- Fact-checking before a blog post: `--all-sources --research` for thoroughness

**Runs inline** — no agent delegation.

---

### /wiki:index — Rebuild content catalog

Rebuilds `wiki/index.md` from actual wiki files. Groups by type, sorts alphabetically, generates tag cloud.

```bash
# Standard rebuild (titles + types only)
/wiki:index

# Include TLDRs in index (heavier but better for L0 search)
/wiki:index --full
```

| Option | Description |
|--------|-------------|
| `--full` | Include page TLDRs in index entries |

**Output format:**
```markdown
# Wiki Index
*Last rebuilt: 2026-04-14*

## Entities
- [[rowboat]] — AI coworker platform (YC S24)
- [[karpathy-llm-wiki-pattern]] — LLM-maintained persistent knowledge base

## Concepts
- [[llm-wiki-best-practices]] — Community-validated wiki practices

## Tags
agent-orchestration (2), knowledge-management (3), llm-tools (1)
```

**Use cases:**
- After bulk ingest: rebuild to include all new pages
- After deleting/renaming pages: sync index with actual files
- Switch to `--full` when wiki grows past 50 pages (TLDRs help L0 search)
- Regular maintenance: run after `/wiki:link` to ensure consistency

**Runs inline** — no agent delegation, no web access.

---

### /wiki:link — Cross-linking pass

Finds and adds missing `[[wikilinks]]` between related pages. Detects unlinked title mentions and pages sharing tags/sources.

```bash
# Preview proposed links (no changes)
/wiki:link --dry-run

# Apply cross-links
/wiki:link

# Single page only
/wiki:link --page wiki/rowboat.md
```

| Option | Description |
|--------|-------------|
| `--dry-run` | Show proposed links without applying |
| `--page <path>` | Only process a single page |

**Detection rules:**
- Body mentions of other page titles not wrapped in `[[wikilinks]]`
- Pages sharing 2+ tags but not in each other's "Related pages" section
- Pages citing same raw sources but not cross-linked

**Example output (dry-run):**
```
Proposed changes:
  wiki/rowboat.md:
    + Line 15: "Karpathy pattern" → "[[karpathy-llm-wiki-pattern|Karpathy pattern]]"
    + Related pages: add [[multi-agent-orchestration-patterns]] (shared tags)
  wiki/llm-wiki-best-practices.md:
    + Related pages: add [[karpathy-llm-wiki-pattern]] (shared source)
→ 3 links proposed across 2 pages
```

**Use cases:**
- After ingest: ensure new pages are properly cross-linked
- After bulk rename: fix broken references
- Regular maintenance: discover missing connections
- Pairs well with `/wiki:audit` for orphan page detection

**Runs inline** — safe operation, only adds links, never removes content.

---

### /wiki:setup — Initialize/verify vault

Scaffolds or verifies vault structure and configuration.

```bash
# Full setup (creates missing directories, checks everything)
/wiki:setup

# Verify only (read-only check, no creation)
/wiki:setup --verify
```

| Option | Description |
|--------|-------------|
| `--verify` | Only check structure, don't create anything |

**Verification checklist:**

| Check | Details |
|-------|---------|
| Directories | 11 required dirs (raw/, wiki/, notes/, outputs/, projects/, etc.) |
| Agent files | 5 agents in `.claude/agents/` |
| Skills | 11 skills available |
| Search tier | Grep/QMD CLI/QMD MCP detection |
| .gitignore | sessions/, plans/, docs/, .DS_Store included |
| CLAUDE.md | Schema present with "Personal Knowledge Base" header |

**Output:**
```
Wiki Setup Status:
  Structure:  ✓ complete (11 directories)
  Agents:     ✓ 5/5 installed
  Skills:     ✓ 11/11 available
  Search:     Grep + index.md (tier 1)
  .gitignore: ✓ configured
  CLAUDE.md:  ✓ schema present
```

**Use cases:**
- First-time setup: `/wiki:setup` creates all missing structure
- After git clone: verify vault integrity
- Debugging: check if agents/skills are properly installed
- Safe to run repeatedly — never overwrites existing files

**Runs inline** — no agent delegation.

---

### /wiki:status — Metrics dashboard

Quick overview of wiki health, metrics, and recent activity.

```bash
# Full dashboard
/wiki:status

# Show only unprocessed sources
/wiki:status --unprocessed

# Per-page details (status, confidence, age)
/wiki:status --verbose
```

| Option | Description |
|--------|-------------|
| `--unprocessed` | Show raw/ files not yet ingested into wiki |
| `--verbose` | Include per-page status, confidence, age, last queried |

**Dashboard output:**
```
Wiki Status — 2026-04-14
──────────────────────────
Pages:       12 wiki/ | 5 notes/ | 3 outputs/
Raw sources: 8 total | 2 unprocessed
Ingest count: 3/5 (audit in 2 ingests)

By type:     entity(4) concept(3) summary(2) comparison(1) decision(1) insight(1)
By status:   active(9) draft(2) stale(1)
By confidence: high(3) medium(5) low(4)

Hash drift:  1 page (wiki/rowboat.md — raw source changed)
Search tier: Grep + index.md (<100 pages)

Recent activity:
  [2026-04-14] audit  | Schema backfill — v2 improvements
  [2026-04-08] ingest | Rowboat — Open-Source AI Coworker
  [2026-04-08] ingest | 7 Things That Make an LLM Wiki Actually Stick
```

**Use cases:**
- Daily check: quick glance at wiki health before starting work
- Find unprocessed sources: `--unprocessed` to see what needs ingesting
- Pre-audit check: review metrics before deciding to run full audit
- Progress tracking: monitor wiki growth over time

**Runs inline** — read-only, never modifies any files. Fast: reads frontmatter only unless `--verbose`.

---

## Agents (5)

| Agent | Location | Role | Tools |
|-------|----------|------|-------|
| `wiki-ingestor` | `.claude/agents/wiki-ingestor.md` | raw/ → wiki/ extraction with provenance tracking | Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch |
| `wiki-librarian` | `.claude/agents/wiki-librarian.md` | Search + answer with progressive disclosure, bumps `last_queried:` | Read, Glob, Grep, Bash, WebFetch, WebSearch, Edit (frontmatter only) |
| `wiki-synthesizer` | `.claude/agents/wiki-synthesizer.md` | Cross-page analysis, concrete noun test, min 3 sources | Read, Write, Edit, Glob, Grep, Bash |
| `wiki-auditor` | `.claude/agents/wiki-auditor.md` | Health check, source hash drift, supersession integrity, unprocessed detection | Read, Glob, Grep, Bash; Write/Edit only with `--fix` |
| `wiki-crystallizer` | `.claude/agents/wiki-crystallizer.md` | sessions/ → wiki insights extraction, credential scrubbing | Read, Write, Edit, Glob, Grep, Bash (no web tools) |

---

## Frontmatter Schema

```yaml
---
title: Page Title
type: summary | entity | concept | comparison | query-result | insight | decision
status: draft | active | stale | superseded
sources: [source-filename.md, ...]
source_hashes: { source-filename.md: "sha256-first-8-chars" }
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: low | medium | high        # low=1 source, medium=2+, high=3+ corroborating
last_queried: YYYY-MM-DD               # bumped when page used to answer a query
supersedes: "[[old-page-name]]"        # this page replaces the target
superseded_by: "[[new-page-name]]"     # this page was replaced by target
tags: [always-english-kebab-case]
relations:
  - { type: supports | contradicts | is-a | part-of | evolved-into | evolved-from | depends-on, target: "[[page]]" }
---
```

### Type descriptions

| Type | Description | When to use |
|------|-------------|-------------|
| `summary` | Overview of a source or topic | Summarizing a whitepaper or long article |
| `entity` | A specific tool, project, person, or organization | Documenting Rowboat, a framework, a company |
| `concept` | A pattern, principle, or technique | Multi-agent orchestration, DDD patterns |
| `comparison` | Structured comparison of alternatives | "Tool A vs Tool B" analysis |
| `query-result` | Reusable answer promoted from outputs/ | A frequently-asked question's answer |
| `insight` | Distilled lesson from sessions, debugging, or cross-project observation | "Why approach X failed for Y" |
| `decision` | Records conflicting positions and the chosen resolution | When sources disagree on a topic |

### Status lifecycle

```
draft → active → stale (auto, >60 days no update AND no query) → superseded (manual)
```

Pages with `last_queried:` within 30 days are immune to stale marking.

### Relation types

| Type | Meaning | Example |
|------|---------|---------|
| `supports` | Provides evidence/foundation for target | best-practices → supports → karpathy-pattern |
| `contradicts` | Disagrees with target | page-a → contradicts → page-b |
| `is-a` | Instance or type of target | rowboat → is-a → karpathy-pattern |
| `part-of` | Structural component of target | auth-module → part-of → ejar3 |
| `evolved-into` | Gave rise to target | karpathy-pattern → evolved-into → rowboat |
| `evolved-from` | Was derived from target | rowboat → evolved-from → karpathy-pattern |
| `depends-on` | Requires target to function | rowboat → depends-on → multi-agent-patterns |

---

## Common Workflows

### Add knowledge from a new source
```bash
/wiki:capture https://example.com/article --ingest
# or two steps:
/wiki:capture https://example.com/article
/wiki:ingest raw/article-name.md
```

### Research a topic from existing knowledge
```bash
/wiki:browse --search "orchestration"       # See what exists
/wiki:query "How does X compare to Y?" --deep --save  # Deep answer
```

### Explore and discover
```bash
/wiki:browse                                # See everything
/wiki:browse --tag multi-agent              # Filter by topic
/wiki:browse --confidence low               # Find weak pages
/wiki:browse --stale                        # Find aging pages
```

### Build knowledge from session logs
```bash
# After exporting sessions via /session-sync:
# wiki-crystallizer extracts decisions, failures, patterns → wiki/ insights
```

### Weekly maintenance
```bash
/wiki:status                    # Check health metrics
/wiki:audit --fix               # Fix safe issues
/wiki:refresh --stale 60        # Update old pages
/wiki:link                      # Add missing cross-links
/wiki:index --full              # Rebuild catalog

# New: Graph + Backlog review
"compile this week"             # Process raw/ files from last 7 days
"analyze graph health"          # Orphans, hubs, clusters report
"review backlog"                # Process wiki/backlog.md
```

**Tip:** Use Obsidian's Periodic Notes plugin with `templates/weekly-review.md` for automated weekly checklist.

### Deep analysis
```bash
/wiki:synthesize "topic area"               # Cross-page insights (min 3 pages)
/wiki:query "question" --file-back          # Save answer as wiki page
```

### Supersede a page
```bash
# When page A is replaced by page B:
# 1. Add superseded_by: "[[page-b]]" to page A frontmatter
# 2. Add supersedes: "[[page-a]]" to page B frontmatter
# 3. Set status: superseded on page A
# Auditor enforces bidirectional consistency
```

---

## Ownership Rules

| Directory | Writer | Reader | Notes |
|-----------|--------|--------|-------|
| `raw/` | User only | LLM | Immutable after drop |
| `wiki/` | LLM only | Both | Derived from raw/ + notes/ |
| `notes/` | User only | Both | LLM audits (report-only), never modifies |
| `outputs/` | LLM | Both | May be promoted to wiki/ |
| `projects/` | LLM compiles | Both | Compiled from codebases + sessions |
| `sessions/` | Auto-export hook | LLM | Read-only for LLM |

## Search Tiers

| Scale | Backend | Setup | When to upgrade |
|-------|---------|-------|-----------------|
| <100 pages | Grep + `wiki/index.md` | Default (current) | — |
| 100-500 | QMD CLI | `brew install tobi/tap/qmd` | Index scan feels slow |
| 500+ | QMD MCP server | QMD + MCP config | CLI response time >2s |

## v2 Features

### Query-aware staleness
Pages with `last_queried:` within 30 days are immune to stale marking, even if `updated:` is >60 days old. The librarian bumps `last_queried:` on every query.

### Supersession tracking
When a page replaces another: set `superseded_by:` on old page, `supersedes:` on new page. Bidirectional — auditor enforces both sides.

### Crystallization pipeline
Extract reusable knowledge from Claude Code session logs:
```
sessions/ → wiki-crystallizer → wiki/ (type: insight) + projects/*/knowledge/
```
Reprocessing guard via `wiki/log.md` entries (no session file modification). Credential patterns (`sk-*`, `ghp_*`, `AKIA*`) automatically stripped.

### Graph Health (Obsidian UI)
Trigger: `"analyze graph health"` — produces report on:
- Orphan pages (no inbound links)
- Hub pages (>10 inbound links, candidates for splitting)
- Isolated clusters needing bridge concepts

Output: `outputs/reports/graph-health-YYYY-MM-DD.md`

### Concept Backlog
Hybrid placeholder approach — no empty stubs, but concepts are tracked:
- Concepts with ≥3 mentions → create wiki page immediately
- Concepts with <3 mentions → append to `wiki/backlog.md`
- Weekly: `"review backlog"` to promote accumulated concepts

---

## Trigger Phrases

Explicit triggers for operations (use these exact phrases):

| Phrase | Operation | Scope |
|--------|-----------|-------|
| `"ingest [filename]"` | Ingest | Single file in `raw/` |
| `"compile this week"` | Compile | `raw/` files modified in last 7 days |
| `"compile [project]"` | Compile | Specific project knowledge |
| `"crystallize [session]"` | Crystallize | Extract insights from session log |
| `"query [question]"` | Query | Search + synthesize answer |
| `"audit vault"` | Audit | Full structural audit |
| `"analyze graph health"` | Graph Health | Obsidian graph analysis |
| `"refresh [page]"` | Refresh | Update single wiki page |
| `"review backlog"` | Backlog | Process `wiki/backlog.md` |
