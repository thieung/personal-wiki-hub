# /wiki:refresh

Refresh content of an existing wiki page — verify claims, update stale info, optionally research new data.

## Usage

```
/wiki:refresh <page.md>
/wiki:refresh wiki/rowboat.md
/wiki:refresh wiki/rowboat.md --research
/wiki:refresh wiki/rowboat.md --all-sources
/wiki:refresh --stale 60
```

## Arguments

- `<page.md>` — Path to wiki page to refresh (required unless `--stale`)
- `--research` — Do fresh web research to supplement existing sources
- `--all-sources` — Re-read all cited sources in `raw/` before refreshing
- `--stale <days>` — Batch mode: refresh all pages with `updated:` older than N days (default 60)
- `--factcheck` — Run cross-model fact-check via `codex:rescue` on the refreshed content before applying diff

## Behavior

### Single page mode

1. Read target page, parse frontmatter and body
2. Audit claims against other wiki pages (consistency check)
3. Validate source URLs if present (check accessibility)
4. If `--all-sources`: re-read all files listed in `sources:` frontmatter
5. If `--research`: web search for updated information on the topic
6. If `--factcheck`: delegate proposed diff + sources to `codex:rescue` for independent verification (see prompt template in `.claude/agents/wiki-ingestor.md`)
7. **Propose diff** — show changes + factcheck findings, do NOT auto-apply
8. On user approval: update content, bump `updated:` date
8. Update cross-references if needed
9. Prepend to `wiki/log.md` (new entries at TOP): `## [YYYY-MM-DD] refresh | Page Title`

### Batch mode (`--stale`)

1. Glob all wiki/*.md files
2. Filter by `updated:` date older than N days
3. List stale pages with age, ask user to confirm batch
4. Run single-page refresh for each confirmed page
5. Summary report at end

## Example

```
/wiki:refresh wiki/rowboat.md --research
→ Read: wiki/rowboat.md (updated: 2026-04-08)
→ Sources checked: raw/rowboat-github-repo.md ✓
→ Web research: found v0.3 release, new MCP routing changes
→ Proposed diff: +12 lines, -3 lines, 2 sections updated
→ Awaiting approval...
```

```
/wiki:refresh --stale 60
→ Found 3 stale pages:
  1. wiki/karpathy-llm-wiki-pattern.md (67 days)
  2. wiki/llm-wiki-best-practices.md (62 days)
  3. wiki/rowboat.md (61 days)
→ Confirm batch refresh? [y/n]
```

## Notes

- Single page: always proposes diff first, never auto-applies
- Batch mode: asks confirmation before starting
- Preserves page history via git (no destructive updates)
- Uses web research only when `--research` flag is set
- Does not use any specific agent — runs inline with full tool access
