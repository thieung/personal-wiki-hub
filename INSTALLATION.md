# Quick Start Guide

Step-by-step setup for personal-wiki-hub with Obsidian + Claude Code.

## Prerequisites

| Tool | Version | Check |
|------|---------|-------|
| macOS | 12+ | `sw_vers` |
| Homebrew | latest | `brew --version` |
| Git | 2.30+ | `git --version` |
| Node.js | 18+ | `node --version` |
| Claude Code | latest | `claude --version` |

---

## Step 1: Install Core Dependencies

```bash
# Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Git
brew install git

# Node.js (for some Claude Code features)
brew install node

# Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

---

## Step 2: Install Obsidian

```bash
# Via Homebrew
brew install --cask obsidian

# Or download from: https://obsidian.md/download
```

---

## Step 3: Install Media Tools (for /wiki:capture)

```bash
# YouTube transcript extraction
brew install yt-dlp

# PDF processing (for ai-multimodal skill)
brew install poppler

# GitHub CLI (for repo capture)
brew install gh
gh auth login
```

---

## Step 4: Clone/Open Vault

```bash
# If new vault
git clone <your-vault-repo> ~/personal-wiki-hub
cd ~/personal-wiki-hub

# Or open existing folder as Obsidian vault
# Obsidian → Open folder as vault → select ~/personal-wiki-hub
```

---

## Step 5: Install Obsidian Plugins

Open Obsidian → Settings (⌘,) → Community plugins → Turn on

### Required Plugins

| Plugin | Purpose | Settings |
|--------|---------|----------|
| **Periodic Notes** | Weekly review automation | Weekly Note → Template: `templates/weekly-review.md` |
| **Templater** | Template variables (`{{date}}`) | Enable folder templates |

### Recommended Plugins

| Plugin | Purpose |
|--------|---------|
| **Smart Connections** | Semantic search when vault grows (>100 pages) |
| **Dataview** | Query frontmatter as database |
| **Obsidian Git** | Auto-commit every 30 minutes |
| **Calendar** | Visual daily/weekly note navigation |

### Plugin Installation

1. Settings → Community plugins → Browse
2. Search plugin name
3. Install → Enable
4. Configure per table above

---

## Step 6: Configure Periodic Notes

Settings → Periodic Notes:

### Daily Notes

| Setting | Value |
|---------|-------|
| Enabled | ✓ |
| Daily Note Template | `templates/daily-note.md` |
| Daily Note Folder | `notes/daily/` |
| Date Format | `YYYY-MM-DD` |

### Weekly Notes

| Setting | Value |
|---------|-------|
| Enabled | ✓ |
| Weekly Note Template | `templates/weekly-review.md` |
| Weekly Note Folder | `notes/reviews/` |
| Week Start | Monday |

Now:
- Every day: Obsidian can auto-create daily journal
- Every Monday: Obsidian auto-creates weekly review checklist

---

## Step 7: Verify Vault Structure

Open terminal in vault directory:

```bash
cd ~/personal-wiki-hub
claude

# In Claude Code session:
/wiki:setup --verify
```

Expected output:
```
Wiki Setup Status:
  Structure:  ✓ complete (11 directories)
  Agents:     ✓ 5/5 installed
  Skills:     ✓ 11/11 available
  Search:     Grep + index.md (tier 1)
  .gitignore: ✓ configured
  CLAUDE.md:  ✓ schema present
```

---

## Step 8: Run Obsidian Setup Script

Bootstrap Obsidian with vault-specific CSS snippets, graph colors, and search exclusions:

```bash
# Run setup (idempotent, safe to re-run)
bash bin/setup-vault.sh

# Force overwrite existing configs
bash bin/setup-vault.sh --force
```

**What it does:**
- Creates `.obsidian/app.json` — excludes `plans/`, `docs/`, `.claude/`, `sessions/` from search/graph
- Creates `.obsidian/appearance.json` — enables `vault-colors` CSS snippet
- Creates `.obsidian/graph.json` — color-codes layers (wiki=blue, notes=green, etc.)
- Installs `.obsidian/snippets/vault-colors.css` — folder highlighting

**After running:**
1. Open vault in Obsidian
2. Settings → Appearance → CSS Snippets → enable "vault-colors"
3. Open Graph View to verify color-coded layers

---

## Step 9: Configure Git (Optional but Recommended)

```bash
# Ensure .gitignore is set
cat >> .gitignore << 'EOF'
sessions/
plans/
docs/
.DS_Store
.obsidian/workspace*.json
EOF

# Initial commit
git add -A
git commit -m "chore: vault setup complete"

# Or use Obsidian Git plugin for auto-commits
```

---

## Step 10: First Capture + Ingest

Test the full pipeline:

```bash
# In Claude Code session:
/wiki:capture https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f --ingest

# Check result
/wiki:status
/wiki:browse
```

---

## Step 11: Daily Usage

### Daily workflow
1. Open daily note (⌘N or click today in Calendar plugin)
2. Capture thoughts in `## Captures` section
3. Track tasks in `## Tasks` section
4. Reflect at end of day

### Capture knowledge
```bash
/wiki:capture <url-or-file> --ingest
```

### Quick capture (fleeting notes)
- Use `notes/fleeting/` for quick ideas
- Process into daily note or wiki later

### Ask questions
```bash
/wiki:query "What is X?"
```

### Weekly maintenance
Open weekly review note (auto-created Monday) → follow checklist:
- [ ] `"compile this week"`
- [ ] `"analyze graph health"`
- [ ] `"review backlog"`
- [ ] Check Graph View (⌘G) for orphans
- [ ] Process `notes/fleeting/` items

---

## Troubleshooting

### "yt-dlp not found"
```bash
brew install yt-dlp
```

### "gh CLI not authenticated"
```bash
gh auth login
```

### "Periodic Notes not creating weekly note"
- Check template path: `templates/weekly-review.md`
- Check folder exists: `notes/reviews/`
- Restart Obsidian

### "Claude Code can't find skills"
```bash
# Verify skills location
ls .claude/skills/

# Or check project-level
ls .claude/agents/
```

### "/wiki:* commands not recognized"
Skills are loaded from CLAUDE.md context. Ensure you're in vault directory:
```bash
cd ~/personal-wiki-hub
claude
```

---

## Directory Structure Reference

```
personal-wiki-hub/
├── raw/               # Drop sources here (immutable)
│   └── archive/       # Auto-archived after 30 days
├── wiki/              # LLM-maintained knowledge
│   ├── index.md       # Content catalog
│   ├── log.md         # Operation history
│   └── backlog.md     # Pending concepts
├── notes/             # Your personal notes (LLM reads only)
│   ├── daily/         # Daily journal entries
│   ├── fleeting/      # Quick captures, inbox
│   └── reviews/       # Weekly review notes
├── outputs/           # Generated artifacts
├── projects/          # Per-project knowledge
├── content/           # Blog drafts
├── sessions/          # Exported Claude Code logs
├── templates/         # Frontmatter templates
│   ├── daily-note.md
│   ├── weekly-review.md
│   ├── fleeting-note.md
│   └── wiki-page.md
├── .claude/agents/    # Wiki subagents
├── CLAUDE.md          # Schema governance
├── README.md          # Full reference
├── INSTALLATION.md    # This file
└── PROJECT_STRUCTURE.md  # Detailed structure guide
```

**Full details:** See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

## Next Steps

1. **Capture 3-5 sources** on a topic you're researching
2. **Run `/wiki:synthesize`** to discover cross-page insights
3. **Set up Obsidian Git** for automatic backups
4. **Explore Graph View** (⌘G) to visualize knowledge connections

Happy knowledge building!
