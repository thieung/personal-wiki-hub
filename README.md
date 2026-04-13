# thieunv-vault

LLM-maintained personal knowledge base following the [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Designed for Claude Code with Obsidian as the human interface.

## Quick Start

```bash
# Verify vault structure
/wiki:setup --verify

# Capture and ingest a source in one step
/wiki:capture https://example.com/article --ingest

# Ask the wiki a question
/wiki:query "What is the Karpathy LLM wiki pattern?"

# Check health
/wiki:status
```

## Architecture

```
thieunv-vault/
├── raw/               # External sources (immutable, user drops)
├── wiki/              # LLM-maintained knowledge (auto-generated)
├── notes/             # User-owned thinking (LLM reads only)
├── outputs/           # LLM-generated answers, reports, research
├── projects/          # Code-driven project knowledge
├── content/           # Blog drafts
├── sessions/          # Auto-exported Claude Code session logs
├── templates/         # Frontmatter templates
└── CLAUDE.md          # Schema governance
```

## Skills Reference

### /wiki:capture — Capture external sources

Fetches content from any source type and saves to `raw/`.

```bash
# Web article
/wiki:capture https://example.com/article

# GitHub repo
/wiki:capture https://github.com/user/repo

# YouTube video (extracts transcript)
/wiki:capture https://youtube.com/watch?v=xxx

# PDF document
/wiki:capture /path/to/document.pdf

# Clipboard content
/wiki:capture --clipboard

# Capture + immediately ingest into wiki
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

---

### /wiki:ingest — Process sources into wiki

Reads raw sources and extracts knowledge into typed wiki pages.

```bash
# Ingest a single source
/wiki:ingest raw/article-name.md

# Ingest from URL (saves to raw/ first, then ingests)
/wiki:ingest https://example.com/article

# Batch ingest all raw files
/wiki:ingest raw/*.md
```

| Option | Description |
|--------|-------------|
| `<source>` | File path in `raw/`, URL, or glob pattern |

**What happens:** Classifies source type → extracts entities/concepts → creates/updates wiki pages with frontmatter, TLDR, counter-arguments → updates index.md + log.md → computes source SHA-256 hashes for provenance tracking.

---

### /wiki:query — Search and answer from wiki

Searches wiki using progressive disclosure (L0→L3) for token efficiency.

```bash
# Basic question
/wiki:query "What orchestration patterns does Rowboat use?"

# Force save answer
/wiki:query "Compare DDD vs clean architecture" --save

# Deep mode — reads linked raw sources for fact-checking
/wiki:query "Is Rowboat's MCP integration production-ready?" --deep

# Limit search scope
/wiki:query "billing domain events" --scope projects/ejar3

# Save answer as permanent wiki page
/wiki:query "MCP vs direct API tradeoffs" --file-back
```

| Option | Description |
|--------|-------------|
| `<question>` | Natural language question |
| `--save` | Force save to `outputs/answers/` |
| `--deep` | L3 disclosure: read linked raw sources |
| `--scope <dir>` | Limit search to directory (e.g., `projects/ejar3`) |
| `--file-back` | Save as wiki page (type: query-result) |

**Progressive disclosure levels:**
- **L0:** Index TLDRs only (fastest, cheapest)
- **L1:** Candidate page headings
- **L2:** Full page body (standard)
- **L3:** Page + all linked raw sources (deepest)

---

### /wiki:synthesize — Cross-page analysis

Finds connections, patterns, and insights across multiple wiki pages.

```bash
# Topic-based synthesis
/wiki:synthesize "orchestration patterns"

# Synthesize specific pages
/wiki:synthesize --pages wiki/rowboat.md wiki/karpathy-llm-wiki-pattern.md

# Full wiki scan (no focus)
/wiki:synthesize
```

| Option | Description |
|--------|-------------|
| `[focus]` | Topic or question (optional, defaults to full scan) |
| `--pages <paths>` | Specific pages to synthesize from |

**Requires minimum 3 source pages.** Produces comparison/insight pages in `wiki/` or research reports in `outputs/research/`.

---

### /wiki:audit — Health check

Structural and content quality audit of wiki and notes.

```bash
# Report only (default)
/wiki:audit

# Auto-fix safe issues in wiki/
/wiki:audit --fix

# Audit wiki only
/wiki:audit --wiki-only

# Audit notes only (always report-only)
/wiki:audit --notes-only

# Audit single page
/wiki:audit --page wiki/rowboat.md
```

| Option | Description |
|--------|-------------|
| `--fix` | Auto-fix safe issues in wiki/ |
| `--wiki-only` | Only audit wiki/ directory |
| `--notes-only` | Only audit notes/ (report-only) |
| `--page <path>` | Single page audit |

**Checks:** Missing frontmatter, broken wikilinks, orphan pages, stale pages (>60 days), anti-cramming/thinning violations, source hash drift, missing TLDR/counter-arguments, index integrity.

**Auto-trigger:** Runs when ingest counter reaches >=5.

---

### /wiki:refresh — Update stale pages

Refreshes content of existing wiki pages — verifies claims, updates info.

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

# Batch with custom threshold
/wiki:refresh --stale 30
```

| Option | Description |
|--------|-------------|
| `<page.md>` | Wiki page path (required unless `--stale`) |
| `--research` | Fresh web research to supplement sources |
| `--all-sources` | Re-read all cited raw/ files |
| `--stale <days>` | Batch mode: all pages older than N days (default 60) |

**Single page:** Always proposes diff first. **Batch:** Asks confirmation before starting.

---

### /wiki:index — Rebuild content catalog

Rebuilds `wiki/index.md` from actual wiki files.

```bash
# Standard rebuild
/wiki:index

# Include TLDRs in index (heavier but better for search)
/wiki:index --full
```

| Option | Description |
|--------|-------------|
| `--full` | Include page TLDRs in index entries |

---

### /wiki:link — Cross-linking pass

Finds and adds missing `[[wikilinks]]` between related pages.

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

**Detects:** Unlinked mentions of page titles, missing related pages (shared tags/sources).

---

### /wiki:setup — Initialize/verify vault

Scaffolds or verifies vault structure.

```bash
# Full setup (creates missing items)
/wiki:setup

# Verify only (read-only check)
/wiki:setup --verify
```

| Option | Description |
|--------|-------------|
| `--verify` | Only check structure, don't create |

**Checks:** Directory structure (11 dirs), agent files (4), skills (10), search tier, .gitignore, CLAUDE.md schema.

---

### /wiki:status — Metrics dashboard

Quick overview of wiki health and metrics.

```bash
# Full dashboard
/wiki:status

# Show only unprocessed sources
/wiki:status --unprocessed

# Per-page details
/wiki:status --verbose
```

| Option | Description |
|--------|-------------|
| `--unprocessed` | Show raw/ files not yet ingested |
| `--verbose` | Include per-page status, confidence, age |

---

## Agents

| Agent | Location | Role |
|-------|----------|------|
| `wiki-ingestor` | `.claude/agents/wiki-ingestor.md` | raw/ → wiki/ extraction with provenance tracking |
| `wiki-librarian` | `.claude/agents/wiki-librarian.md` | Search + answer with progressive disclosure |
| `wiki-synthesizer` | `.claude/agents/wiki-synthesizer.md` | Cross-page analysis, concrete noun test |
| `wiki-auditor` | `.claude/agents/wiki-auditor.md` | Health check, source hash drift detection |

## Frontmatter Schema

```yaml
---
title: Page Title
type: summary | entity | concept | comparison | query-result | insight | decision
status: draft | active | stale | superseded
sources: [source-filename.md]
source_hashes: { source-filename.md: "sha256-8" }
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: low | medium | high
tags: [english-kebab-case]
relations:
  - { type: supports | contradicts | is-a | part-of | evolved-into | depends-on, target: "[[page]]" }
---
```

## Common Workflows

### Add knowledge from a new source
```bash
/wiki:capture https://example.com/article --ingest
```

### Research a topic from existing knowledge
```bash
/wiki:query "How does X compare to Y?" --deep --save
```

### Weekly maintenance
```bash
/wiki:status                    # Check health
/wiki:audit --fix               # Fix safe issues
/wiki:refresh --stale 60        # Update old pages
/wiki:link                      # Add missing cross-links
/wiki:index --full              # Rebuild catalog
```

### Deep analysis
```bash
/wiki:synthesize "topic area"   # Cross-page insights
/wiki:query "question" --file-back  # Save answer to wiki
```

## Ownership Rules

| Directory | Writer | Reader |
|-----------|--------|--------|
| `raw/` | User only | LLM |
| `wiki/` | LLM only | Both |
| `notes/` | User only | Both |
| `outputs/` | LLM | Both |
| `projects/` | LLM compiles | Both |

## Search Tiers

| Scale | Backend | Setup |
|-------|---------|-------|
| <100 pages | Grep + `wiki/index.md` | Default |
| 100-500 | QMD CLI | `brew install tobi/tap/qmd` |
| 500+ | QMD MCP server | QMD + MCP config |
