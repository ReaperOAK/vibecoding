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
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMPDIR="$(mktemp -d)"

cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

echo "==> Syncing from ReaperOAK/vibecoding (branch: $BRANCH)..."
echo "    Project root: $PROJECT_ROOT"
echo "    Temp dir: $TMPDIR"

# Shallow clone (fast, minimal bandwidth)
echo "==> Cloning (shallow)..."
git clone --depth 1 --branch "$BRANCH" "$REPO" "$TMPDIR/vibecoding" 2>&1 | tail -1

SRC="$TMPDIR/vibecoding"

# --- Sync .github/ (excluding memory-bank/) ---
echo "==> Syncing .github/ (excluding memory-bank/)..."

# Delete everything in .github/ EXCEPT memory-bank/
# This ensures removed upstream files are also removed locally
find "$PROJECT_ROOT/.github" -mindepth 1 -maxdepth 1 \
  ! -name 'memory-bank' \
  -exec rm -rf {} +

# Copy everything from source .github/ EXCEPT memory-bank/
cd "$SRC/.github"
for item in *; do
  if [ "$item" = "memory-bank" ]; then
    echo "    Skipping memory-bank/ (project-specific)"
    continue
  fi
  cp -r "$item" "$PROJECT_ROOT/.github/$item"
  echo "    Copied .github/$item"
done

# --- Sync root-level files ---
echo "==> Syncing root files..."

for file in agents.md todo_visual.py; do
  if [ -f "$SRC/$file" ]; then
    cp "$SRC/$file" "$PROJECT_ROOT/$file"
    echo "    Copied $file"
  fi
done

# --- Summary ---
echo ""
echo "==> Sync complete!"
echo "    Source: ReaperOAK/vibecoding@$BRANCH"
echo "    Preserved: .github/memory-bank/"
echo "    Skipped: README.md"
echo ""
echo "    Review changes with: git diff --stat"
echo "    Commit with: git add .github/ agents.md todo_visual.py && git commit -m 'chore: sync vibecoding infrastructure from upstream'"
