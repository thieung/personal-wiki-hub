# /wiki:setup

Initialize or verify vault structure and configuration.

## Usage

```
/wiki:setup
/wiki:setup --verify
```

## Arguments

- `--verify` — Only check structure, don't create anything

## Behavior

1. Check for `CLAUDE.md` with "Personal Knowledge Base" header
2. Verify/create directory structure:
   ```
   raw/{assets,archive}
   wiki/{assets}
   wiki/index.md
   wiki/log.md
   notes/{assets}
   outputs/{answers,reports,research}
   projects/
   content/
   sessions/
   templates/
   .claude/agents/
   ```
3. Verify agent files exist in `.claude/agents/`:
   - wiki-ingestor.md
   - wiki-librarian.md
   - wiki-synthesizer.md
   - wiki-auditor.md
4. Check `.gitignore` includes: sessions/, plans/, docs/, .DS_Store
5. Detect search tier:
   - Check if `qmd` CLI is installed (`which qmd`)
   - Check if QMD MCP server is configured
   - Report current tier
6. Report setup status

## Output

```
Wiki Setup Status:
  Structure:  ✓ complete (11 directories)
  Agents:     ✓ 4/4 installed
  Skills:     ✓ 8/8 available
  Search:     Grep + index.md (tier 1)
  .gitignore: ✓ configured
  CLAUDE.md:  ✓ schema present
```

## Notes

- Safe to run multiple times — only creates missing items
- Never overwrites existing files
- Use `--verify` for read-only check
