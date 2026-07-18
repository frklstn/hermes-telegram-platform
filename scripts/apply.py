"""Apply the telegram-platform patch set to the local Hermes install.

Usage:
    python3 ~/.hermes/skills/telegram-platform/scripts/apply.py
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
PATCH_FILE = SKILL_DIR / "patches" / "telegram-platform-v0.18.2.diff"


def find_hermes_agent() -> Path:
    home = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
    candidates = [
        home / "hermes-agent",
        Path.home() / "AppData" / "Local" / "hermes" / "hermes-agent",
        Path("/c/Users/Administrator/AppData/Local/hermes/hermes-agent"),
    ]
    for c in candidates:
        if (c / "gateway" / "slash_commands.py").exists():
            return c
    raise FileNotFoundError("Could not locate hermes-agent checkout")


def main() -> int:
    if not PATCH_FILE.exists():
        print(f"Patch file not found: {PATCH_FILE}")
        return 1

    repo = find_hermes_agent()
    print(f"Found Hermes agent at: {repo}")

    # Backup current files touched by the patch.
    touched = [
        "agent/insights.py",
        "gateway/slash_commands.py",
        "hermes_cli/commands.py",
        "hermes_cli/session_listing.py",
        "hermes_cli/suggestions_cmd.py",
        "hermes_cli/write_approval_commands.py",
        "plugins/platforms/telegram/adapter.py",
    ]
    backup_dir = repo / "telegram-platform-backup"
    backup_dir.mkdir(exist_ok=True)
    for rel in touched:
        src = repo / rel
        if src.exists():
            dst = backup_dir / rel.replace("/", "_")
            shutil.copy2(src, dst)

    # Apply patch. The diff was generated from the repo root with paths like
    # "agent/insights.py", so run from the repo root with -p0.
    result = subprocess.run(
        ["patch", "-p0", "-i", str(PATCH_FILE)],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print("PATCH FAILED:")
        print(result.stderr)
        return result.returncode

    print("Patch applied. Restart the gateway:")
    print("  hermes gateway restart --all")
    return 0


if __name__ == "__main__":
    sys.exit(main())
