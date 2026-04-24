# /wiki:link

Cross-linking pass — find and add missing `[[wikilinks]]` between related pages.

## Usage

```
/wiki:link
/wiki:link --dry-run
/wiki:link --page wiki/rowboat.md
```

## Arguments

- `--dry-run` — Show proposed links without applying
- `--page <path>` — Only process a single page

## Behavior

1. Glob all `wiki/*.md` files
2. Build page title → filename map from frontmatter
3. For each page:
   - Scan body for mentions of other page titles (case-insensitive)
   - Check if mention is already wrapped in `[[wikilink]]`
   - If not: propose adding wikilink
4. Check "Related pages" section at bottom of each page:
   - Find pages that share 2+ tags
   - Find pages that cite same sources
   - Propose adding missing related page links
5. If `--dry-run`: report proposed changes only
6. Otherwise: apply links, bump `updated:` dates
7. Prepend to `wiki/log.md` (new entries at TOP): `## [YYYY-MM-DD] link | cross-linking pass`

## Example

```
/wiki:link --dry-run
→ Proposed changes:
  wiki/rowboat.md:
    + Line 15: "Karpathy pattern" → "[[karpathy-llm-wiki-pattern|Karpathy pattern]]"
    + Related pages: add [[multi-agent-orchestration-patterns]] (shared tags: agent-orchestration)
  wiki/llm-wiki-best-practices.md:
    + Related pages: add [[karpathy-llm-wiki-pattern]] (shared source: 7-things-llm-wiki-stick.md)
→ 3 links proposed across 2 pages
```

## Notes

- Safe operation — only adds links, never removes content
- Respects Obsidian `[[wikilink]]` and `[[target|display text]]` syntax
- Does not modify `raw/` or `notes/`
- Pairs well with `/wiki:audit` for orphan page detection
