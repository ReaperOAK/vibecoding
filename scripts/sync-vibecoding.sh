#!/usr/bin/env bash
# sync-vibecoding.sh — One-way sync from ReaperOAK/vibecoding into this project
#
# Syncs:
#   .github/*  (EXCLUDING memory-bank/)
#   agents.md
#   todo_visual.py
#
# Does NOT sync:
#   README.md (repo-specific)
#   .github/memory-bank/ (project-specific persistent state)
#
# Usage:
#   ./scripts/sync-vibecoding.sh          # sync from main
#   ./scripts/sync-vibecoding.sh <branch>  # sync from a specific branch
#   bash scripts/sync-vibecoding.sh

set -euo pipefail

REPO="https://github.com/ReaperOAK/vibecoding.git"
BRANCH="${1:-main}"
DRY_RUN="${DRY_RUN:-}"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMPDIR="$(mktemp -d)"

cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# ---- Safety: stash uncommitted changes before destructive sync ----------
if git -C "$PROJECT_ROOT" diff --quiet && git -C "$PROJECT_ROOT" diff --cached --quiet; then
  STASHED=false
else
  echo "==> Stashing uncommitted changes..."
  git -C "$PROJECT_ROOT" stash push -m "sync-vibecoding: auto-stash before sync $(date +%F_%T)"
  STASHED=true
fi

echo "==> Syncing from ReaperOAK/vibecoding (branch: $BRANCH)..."
echo "    Project root: $PROJECT_ROOT"
echo "    Temp dir: $TMPDIR"
[[ -n "$DRY_RUN" ]] && echo "    *** DRY RUN — no files will be modified ***"

# Shallow clone (fast, minimal bandwidth)
echo "==> Cloning (shallow)..."
if ! git clone --depth 1 --branch "$BRANCH" "$REPO" "$TMPDIR/vibecoding" 2>&1 | tail -1; then
  echo "ERROR: Clone failed. Aborting sync." >&2
  [[ "$STASHED" == true ]] && git -C "$PROJECT_ROOT" stash pop
  exit 1
fi

SRC="$TMPDIR/vibecoding"

# ---- Validate source has expected structure ----------------------------
for required in .github agents.md todo_visual.py; do
  if [[ ! -e "$SRC/$required" ]]; then
    echo "ERROR: Expected '$required' not found in upstream clone. Aborting." >&2
    [[ "$STASHED" == true ]] && git -C "$PROJECT_ROOT" stash pop
    exit 1
  fi
done

# --- Sync .github/ (excluding memory-bank/) ---
echo "==> Syncing .github/ (excluding memory-bank/)..."

if [[ -z "$DRY_RUN" ]]; then
  # Delete everything in .github/ EXCEPT memory-bank/
  # This ensures removed upstream files are also removed locally
  find "$PROJECT_ROOT/.github" -mindepth 1 -maxdepth 1 \
    ! -name 'memory-bank' \
    -exec rm -rf {} +
fi

# Copy everything from source .github/ EXCEPT memory-bank/
cd "$SRC/.github"
for item in *; do
  if [ "$item" = "memory-bank" ]; then
    echo "    Skipping memory-bank/ (project-specific)"
    continue
  fi
  if [[ -n "$DRY_RUN" ]]; then
    echo "    [dry-run] Would copy .github/$item"
  else
    cp -r "$item" "$PROJECT_ROOT/.github/$item"
    echo "    Copied .github/$item"
  fi
done

# --- Sync root-level files ---
echo "==> Syncing root files..."

for file in agents.md todo_visual.py; do
  if [ -f "$SRC/$file" ]; then
    if [[ -n "$DRY_RUN" ]]; then
      echo "    [dry-run] Would copy $file"
    else
      cp "$SRC/$file" "$PROJECT_ROOT/$file"
      echo "    Copied $file"
    fi
  fi
done

# ---- Restore stash if we stashed earlier --------------------------------
if [[ "$STASHED" == true ]]; then
  echo "==> Restoring stashed changes..."
  git -C "$PROJECT_ROOT" stash pop || echo "WARN: stash pop had conflicts — resolve manually."
fi

# --- Summary ---
echo ""
echo "==> Sync complete!"
echo "    Source: ReaperOAK/vibecoding@$BRANCH"
echo "    Preserved: .github/memory-bank/"
echo "    Skipped: README.md"
echo ""
echo "    Review changes with: git diff --stat"
echo "    Commit with: git add .github/ agents.md todo_visual.py && git commit -m 'chore: sync vibecoding infrastructure from upstream'"
