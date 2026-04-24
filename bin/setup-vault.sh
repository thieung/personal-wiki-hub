#!/bin/bash
# setup-vault.sh — One-shot Obsidian bootstrap for thieunv-vault
# Idempotent: safe to re-run. Merges JSON configs, doesn't overwrite.

set -e

VAULT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OBSIDIAN_DIR="$VAULT_ROOT/.obsidian"
FORCE=false

# Parse args
while [[ $# -gt 0 ]]; do
    case $1 in
        --force) FORCE=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check OS
check_os() {
    case "$(uname -s)" in
        Darwin) OS="darwin" ;;
        Linux) OS="linux" ;;
        *) log_error "Unsupported OS: $(uname -s)"; exit 1 ;;
    esac
    log_info "Detected OS: $OS"
}

# Check Obsidian installed (warn only)
check_obsidian() {
    local found=false
    if [[ "$OS" == "darwin" ]]; then
        [[ -d "/Applications/Obsidian.app" ]] && found=true
    else
        (flatpak list 2>/dev/null | grep -qi obsidian) && found=true
        command -v obsidian &>/dev/null && found=true
    fi

    if $found; then
        log_info "Obsidian installation detected"
    else
        log_warn "Obsidian not found. Install from obsidian.md before using vault."
    fi
}

# Check jq available
check_jq() {
    if ! command -v jq &>/dev/null; then
        log_error "jq is required. Install: brew install jq (macOS) or apt install jq (Linux)"
        exit 1
    fi
}

# Merge JSON config (preserves user customizations)
merge_json() {
    local file="$1"
    local new_content="$2"

    if [[ -f "$file" && "$(cat "$file")" != "{}" ]]; then
        if $FORCE; then
            log_warn "Overwriting $file (--force)"
            echo "$new_content" > "$file"
        else
            # Merge: new content wins for conflicting keys
            local merged
            merged=$(jq -s '.[0] * .[1]' "$file" <(echo "$new_content") 2>/dev/null || echo "$new_content")
            echo "$merged" > "$file"
            log_info "Merged $file"
        fi
    else
        echo "$new_content" > "$file"
        log_info "Created $file"
    fi
}

# Setup app.json (exclude folders from search/graph)
setup_app_json() {
    local config='{
        "userIgnoreFilters": [
            "plans/",
            "docs/",
            ".claude/",
            "sessions/"
        ]
    }'
    merge_json "$OBSIDIAN_DIR/app.json" "$config"
}

# Setup appearance.json (enable CSS snippet)
setup_appearance_json() {
    local config='{
        "enabledCssSnippets": ["vault-colors"]
    }'
    merge_json "$OBSIDIAN_DIR/appearance.json" "$config"
}

# Setup graph.json (color groups)
setup_graph_json() {
    local config='{
        "colorGroups": [
            {"query": "path:raw/", "color": {"a": 0.3, "rgb": 8421504}},
            {"query": "path:wiki/", "color": {"a": 1, "rgb": 4169E1}},
            {"query": "path:notes/", "color": {"a": 1, "rgb": 2E8B57}},
            {"query": "path:outputs/", "color": {"a": 1, "rgb": 16753920}},
            {"query": "path:projects/", "color": {"a": 1, "rgb": 9400D3}}
        ]
    }'
    merge_json "$OBSIDIAN_DIR/graph.json" "$config"
}

# Install CSS snippet
install_css_snippet() {
    local snippet_dir="$OBSIDIAN_DIR/snippets"
    local snippet_file="$snippet_dir/vault-colors.css"

    mkdir -p "$snippet_dir"

    if [[ -f "$snippet_file" ]] && ! $FORCE; then
        log_info "CSS snippet already exists: $snippet_file"
    else
        cat > "$snippet_file" << 'EOF'
/* vault-colors.css — Color-code vault layers in file explorer */
/* Tested on Obsidian v1.9.10 */

/* raw/ — gray/dimmed (immutable sources) */
.nav-folder-title[data-path^="raw"] {
    color: var(--text-muted);
    opacity: 0.7;
}

/* wiki/ — blue (LLM-maintained) */
.nav-folder-title[data-path^="wiki"] {
    color: #4169E1;
}

/* notes/ — green (user-owned) */
.nav-folder-title[data-path^="notes"] {
    color: #2E8B57;
}

/* outputs/ — orange (generated artifacts) */
.nav-folder-title[data-path^="outputs"] {
    color: #FFA500;
}

/* projects/ — purple (code-driven) */
.nav-folder-title[data-path^="projects"] {
    color: #9400D3;
}

/* content/ — teal (blog drafts) */
.nav-folder-title[data-path^="content"] {
    color: #20B2AA;
}

/* sessions/ — slate (auto-export) */
.nav-folder-title[data-path^="sessions"] {
    color: #708090;
}
EOF
        log_info "Installed CSS snippet: $snippet_file"
    fi
}

# Verify dashboard.base exists
verify_dashboard() {
    local dashboard="$VAULT_ROOT/wiki/meta/dashboard.base"
    if [[ ! -f "$dashboard" ]]; then
        log_error "Dashboard not found: $dashboard"
        log_error "Run Phase 5 (bases-dashboard-seed) first."
        exit 1
    fi
    log_info "Dashboard verified: $dashboard"
}

# Print next steps
print_next_steps() {
    echo ""
    log_info "Setup complete! Next steps:"
    echo "  1. Open vault in Obsidian"
    echo "  2. Enable CSS snippets: Settings → Appearance → CSS Snippets → vault-colors"
    echo "  3. Verify graph colors: Open Graph View"
    echo "  4. (Optional) Install plugins: Local REST API, obsidian-git"
    echo ""
}

# Main
main() {
    log_info "Setting up thieunv-vault for Obsidian..."
    check_os
    check_jq
    check_obsidian

    mkdir -p "$OBSIDIAN_DIR"

    setup_app_json
    setup_appearance_json
    setup_graph_json
    install_css_snippet
    verify_dashboard

    print_next_steps
}

main "$@"
