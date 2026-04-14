# /wiki:audit

Structural health check of the wiki and notes directories.

## Usage

```
/wiki:audit
/wiki:audit --fix
/wiki:audit --wiki-only
/wiki:audit --notes-only
/wiki:audit --page wiki/rowboat.md
```

## Arguments

- `--fix` — Auto-fix safe issues in wiki/ (missing sections, index sync)
- `--wiki-only` — Only audit wiki/ directory
- `--notes-only` — Only audit notes/ directory (report-only, no fixes)
- `--page <path>` — Audit single page

## Behavior

1. Locate vault root
2. Delegate to `wiki-auditor` agent with scope and fix flag
3. Agent scans all .md files, checks:
   - Frontmatter completeness
   - Broken `[[wikilinks]]`
   - Orphan pages (no inbound links)
   - Stale pages (updated >60 days ago)
   - Missing TLDR / counter-arguments sections
   - Anti-cramming / anti-thinning violations
   - Index consistency with actual files
4. Saves report to `outputs/reports/audit-YYYY-MM-DD.md`
5. If `--fix`: applies safe fixes to wiki/ only
6. Appends to `wiki/log.md`

## Auto-trigger

Runs automatically when ingest counter in CLAUDE.md reaches >=5. Resets counter after audit.

## Example

```
/wiki:audit --fix
→ Scanned: 12 pages (8 wiki/, 4 notes/)
→ Issues: 3 critical, 5 warning, 2 info
→ Auto-fixed: 2 (added missing counter-arguments template, synced index)
→ Report: outputs/reports/audit-2026-04-12.md
```

## Notes

- notes/ is always report-only — never modified
- Uses `wiki-auditor` agent from `.claude/agents/wiki-auditor.md`
