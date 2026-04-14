# /wiki:status

Wiki metrics dashboard — page counts, health summary, unprocessed sources.

## Usage

```
/wiki:status
/wiki:status --unprocessed
/wiki:status --verbose
```

## Arguments

- `--unprocessed` — Show only raw/ files not yet ingested into wiki
- `--verbose` — Include per-page details (status, confidence, age)

## Behavior

1. Count files in each directory: `raw/`, `wiki/`, `notes/`, `outputs/`, `projects/`
2. Parse wiki frontmatter for: status distribution, confidence distribution, type distribution
3. Read ingest counter from `CLAUDE.md`
4. Detect unprocessed sources: files in `raw/` not cited in any wiki page's `sources:` field
5. Check for source hash drift (any `source_hashes` mismatches)
6. Read last 5 entries from `wiki/log.md` for recent activity
7. Detect search tier (grep/QMD CLI/QMD MCP)

## Output Format

```
Wiki Status — YYYY-MM-DD
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
  [2026-04-12] ingest | Rowboat GitHub repo
  [2026-04-11] query  | MCP vs direct API
  [2026-04-10] audit  | full scan
```

## Notes

- Read-only operation — never modifies any files
- Fast: only reads frontmatter, not full page content (unless --verbose)
- Unprocessed detection: compares raw/ filenames against all wiki `sources:` fields
