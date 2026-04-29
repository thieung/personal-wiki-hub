#!/usr/bin/env python3
"""Session Sync v2 — Export Claude Code sessions with lifecycle management.

Usage:
    session-sync sync                      # Sync current session (for hooks)
    session-sync export [OPTIONS]          # Export sessions
    session-sync list [--active|--all]     # List exported sessions
    session-sync resume [--pick|--active]  # Resume a session
    session-sync note TEXT                 # Add timestamped note
    session-sync close [TEXT]              # Mark session done
    session-sync log [--status S] ...     # Annotate session
    session-sync index                     # Re-index in QMD
    session-sync search QUERY              # BM25 keyword search
    session-sync vsearch QUERY             # Semantic vector search
    session-sync status                    # Show status
    session-sync config [OPTIONS]          # Configure settings
    session-sync list-projects             # List Claude projects
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

__version__ = "2.0.0"

# Ensure lib/ is importable
sys.path.insert(0, str(Path(__file__).parent))

from lib import config_loader as cfg
from lib import session_extractor as extractor
from lib import markdown_renderer as renderer
from lib import session_lifecycle as lifecycle
from lib import qmd_search as qmd

SKILL_DIR = Path(__file__).parent.parent
PROJECTS_DIR = Path.home() / ".claude" / "projects"


# =============================================================================
# Core commands: sync, export, status, config, setup, list-projects
# =============================================================================

def cmd_sync(args) -> int:
    """Sync current session (called by Stop hook or manually)."""
    config = cfg.load_config()
    output_dir = cfg.get_output_dir(config)
    log_file = SKILL_DIR / "sync.log"

    session_id = None
    transcript_path = None

    # Log invocation
    with open(log_file, "a") as f:
        f.write(f"{datetime.now().isoformat()} sync called, isatty={sys.stdin.isatty()}\n")

    # Try stdin (hook mode)
    if not sys.stdin.isatty():
        try:
            raw = sys.stdin.read()
            with open(log_file, "a") as f:
                f.write(f"{datetime.now().isoformat()} stdin ({len(raw)} bytes)\n")
            if raw.strip():
                data = json.loads(raw)
                session_id = data.get("session_id")
                transcript_path = data.get("transcript_path")
        except Exception as e:
            with open(log_file, "a") as f:
                f.write(f"{datetime.now().isoformat()} stdin error: {e}\n")

    # Fallback: env vars
    if not session_id:
        session_id = os.environ.get("CK_SESSION_ID") or os.environ.get("CLAUDE_SESSION_ID")
    if not transcript_path and session_id:
        for pdir in PROJECTS_DIR.iterdir():
            if not pdir.is_dir():
                continue
            jsonl = pdir / f"{session_id}.jsonl"
            if jsonl.exists():
                transcript_path = str(jsonl)
                break

    if not session_id or not transcript_path:
        return 0  # Silent no-op when no session found (normal for first prompt)

    jsonl_path = Path(transcript_path)
    if not jsonl_path.exists():
        return 1

    vault_dir = config.get("target_folder") if config.get("vault_mode") else None
    if _export_one(jsonl_path, output_dir, config, vault_dir):
        with open(log_file, "a") as f:
            f.write(f"{datetime.now().isoformat()} synced: {session_id[:8]}\n")
    return 0


def cmd_export(args) -> int:
    """Export sessions with filters."""
    config = cfg.load_config()
    output_dir = cfg.get_output_dir(config)
    output_dir.mkdir(parents=True, exist_ok=True)
    vault_dir = config.get("target_folder") if config.get("vault_mode") else None

    cutoff = None
    if args.days:
        cutoff = time.time() - (args.days * 86400)
    elif args.since:
        try:
            cutoff = datetime.strptime(args.since, "%Y-%m-%d").timestamp()
        except ValueError:
            print(f"Invalid date: {args.since} (use YYYY-MM-DD)")
            return 1

    project_dirs = sorted(PROJECTS_DIR.glob("-*"))
    if args.project:
        project_dirs = [d for d in project_dirs if args.project in d.name]

    total = 0
    for pdir in project_dirs:
        if not pdir.is_dir():
            continue
        for jsonl in pdir.glob("*.jsonl"):
            if cutoff and jsonl.stat().st_mtime < cutoff:
                continue
            if _export_one(jsonl, output_dir, config, vault_dir):
                total += 1

    print(f"Exported {total} sessions to {output_dir}")
    return 0


def _export_one(jsonl_path: Path, output_dir: Path, config: dict, vault_dir: str | None) -> bool:
    """Export a single session with re-sync preservation."""
    data = extractor.extract_session_data(jsonl_path, vault_dir)
    if not data or data["messages"] == 0:
        return False

    project_name = extractor.parse_project_name(data["cwd"]) if data["cwd"] else "unknown"

    # Determine output path: vault_mode=flat, legacy=per-project
    if config.get("vault_mode"):
        target_dir = output_dir
    else:
        target_dir = output_dir / project_name
    target_dir.mkdir(parents=True, exist_ok=True)

    # Filename with time and project for sort order and identification
    time_part = ""
    if data.get("first_timestamp"):
        try:
            ts = datetime.fromisoformat(data["first_timestamp"].replace("Z", "+00:00"))
            time_part = f"-{ts.strftime('%H%M')}"
        except Exception:
            pass
    short_id = data["session_id"][:8]
    filename = f"{data['date']}{time_part}-{project_name}-{short_id}.md"

    # Check for existing file (by session_id suffix)
    existing = None
    for f in target_dir.glob(f"*-{short_id}.md"):
        existing = f
        break

    output_file = existing or (target_dir / filename)

    # Read preserved fields from existing file
    preserved_fm, my_notes = renderer.read_preserved(output_file)

    md = renderer.generate_markdown(data, project_name, preserved_fm, my_notes, vault_dir)
    output_file.write_text(md, encoding="utf-8")
    return True


def cmd_status(args) -> int:
    """Show current status."""
    config = cfg.load_config()
    output_dir = cfg.get_output_dir(config)
    qmd_path = cfg.find_qmd(config)

    print("Session Sync v2 Status")
    print("=" * 40)
    print(f"Target:     {config['target_folder']}")
    print(f"Output:     {output_dir}")
    print(f"Vault mode: {'yes' if config.get('vault_mode') else 'no'}")
    print(f"Auto-sync:  {'yes' if config.get('auto_sync') else 'no'}")
    print()

    if qmd_path:
        print(f"QMD: {qmd_path}")
    else:
        print("QMD: not installed (npm i -g @tobilu/qmd)")
    print()

    if output_dir.exists():
        md_files = list(output_dir.glob("*.md"))
        if md_files:
            print(f"Sessions: {len(md_files)} exported")
        else:
            # Check per-project subdirs (legacy mode)
            subdirs = [d for d in output_dir.iterdir() if d.is_dir()]
            total = sum(len(list(d.glob("*.md"))) for d in subdirs)
            print(f"Sessions: {total} in {len(subdirs)} projects")
    else:
        print("Sessions: none exported yet")
    return 0


def cmd_config(args) -> int:
    """Configure settings."""
    config = cfg.load_config()
    changed = False

    if args.target_folder:
        config["target_folder"] = args.target_folder
        print(f"target_folder = {args.target_folder}")
        changed = True
    if args.collection_name:
        config["collection_name"] = args.collection_name
        print(f"collection_name = {args.collection_name}")
        changed = True
    if args.auto_sync is not None:
        config["auto_sync"] = args.auto_sync
        print(f"auto_sync = {args.auto_sync}")
        changed = True
    if args.vault_mode is not None:
        config["vault_mode"] = args.vault_mode
        print(f"vault_mode = {args.vault_mode}")
        changed = True
    if args.output_subdir:
        config["output_subdir"] = args.output_subdir
        print(f"output_subdir = {args.output_subdir}")
        changed = True

    if changed:
        cfg.save_config(config)
        print(f"Saved: {cfg.CONFIG_FILE}")
    else:
        print(json.dumps(config, indent=2))
    return 0


def cmd_list_projects(args) -> int:
    """List available Claude Code projects."""
    print("Projects:")
    for pdir in sorted(PROJECTS_DIR.glob("-*")):
        if not pdir.is_dir():
            continue
        count = len(list(pdir.glob("*.jsonl")))
        if count > 0:
            name = extractor.parse_project_name(pdir.name)
            print(f"  {name}: {count} sessions")
    return 0


def cmd_setup(args) -> int:
    """Show setup instructions."""
    script_path = Path(__file__)
    print("Session Sync v2 Setup")
    print("=" * 40)
    print(f"\n1. Run: python3 \"{script_path}\" status")
    print(f"2. Set folder: python3 \"{script_path}\" config --target-folder PATH")
    print(f"3. Export: python3 \"{script_path}\" export --all")
    print(f"4. (Optional) Install QMD: npm i -g @tobilu/qmd")
    print(f"5. (Optional) Index: python3 \"{script_path}\" index")
    print(f"6. (Optional) Add Stop hook to ~/.claude/settings.json")
    return 0


# =============================================================================
# CLI wiring
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Session Sync v2")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", help="Commands")

    # setup / status
    sub.add_parser("setup", help="Setup instructions").set_defaults(func=cmd_setup)
    sub.add_parser("status", help="Show status").set_defaults(func=cmd_status)

    # sync
    sub.add_parser("sync", help="Sync current session (hook)").set_defaults(func=cmd_sync)

    # export
    p = sub.add_parser("export", help="Export sessions")
    p.add_argument("--all", action="store_true")
    p.add_argument("--days", type=int)
    p.add_argument("--since", help="YYYY-MM-DD")
    p.add_argument("--project")
    p.set_defaults(func=cmd_export)

    # list
    p = sub.add_parser("list", help="List sessions")
    p.add_argument("--active", action="store_true", help="Active only (default)")
    p.add_argument("--all", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=lifecycle.cmd_list)

    # resume
    p = sub.add_parser("resume", help="Resume a session")
    p.add_argument("--pick", "-p", action="store_true")
    p.add_argument("--active", "-a", action="store_true")
    p.add_argument("--fork", "-f", action="store_true")
    p.add_argument("--all", action="store_true")
    p.add_argument("file", nargs="?")
    p.set_defaults(func=lifecycle.cmd_resume)

    # note
    p = sub.add_parser("note", help="Add timestamped note")
    p.add_argument("text", nargs="+")
    p.add_argument("--session-id")
    p.set_defaults(func=lifecycle.cmd_note)

    # close
    p = sub.add_parser("close", help="Mark session done")
    p.add_argument("text", nargs="*")
    p.add_argument("--session-id")
    p.set_defaults(func=lifecycle.cmd_close)

    # log
    p = sub.add_parser("log", help="Annotate session")
    p.add_argument("text", nargs="*")
    p.add_argument("--status", "-s")
    p.add_argument("--tags", "-t")
    p.add_argument("--rating", "-r", type=int)
    p.add_argument("--session-id")
    p.set_defaults(func=lifecycle.cmd_log)

    # QMD commands
    sub.add_parser("index", help="Re-index in QMD").set_defaults(func=qmd.cmd_index)

    p = sub.add_parser("search", help="Keyword search")
    p.add_argument("query")
    p.add_argument("-n", type=int, default=10)
    p.set_defaults(func=qmd.cmd_search)

    p = sub.add_parser("vsearch", help="Semantic search")
    p.add_argument("query")
    p.add_argument("-n", type=int, default=10)
    p.set_defaults(func=qmd.cmd_vsearch)

    # config
    p = sub.add_parser("config", help="Configure settings")
    p.add_argument("--target-folder")
    p.add_argument("--collection-name")
    p.add_argument("--auto-sync", type=bool)
    p.add_argument("--vault-mode", type=bool)
    p.add_argument("--output-subdir")
    p.set_defaults(func=cmd_config)

    # list-projects
    sub.add_parser("list-projects", help="List projects").set_defaults(func=cmd_list_projects)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
