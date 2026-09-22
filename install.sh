#!/usr/bin/env bash
# Install every skill in this repo into Kiro's skill directories by symlink.
#   ./install.sh              -> global: ~/.kiro/skills (IDE + CLI) and ~/.kiro/crew/skills (Crew)
#   ./install.sh --workspace  -> also link into ./.kiro/skills of the current project
#                                (required for Kiro Web/Mobile, which read workspace skills only)
#   ./install.sh --copy       -> copy instead of symlink (for machines that dislike symlinks)
# Re-running is safe: existing links are replaced, existing copies are refreshed.
# Update everything later with:  git -C "$(dirname "$0")" pull
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIRO_HOME="${KIRO_HOME:-$HOME/.kiro}"
CREW_HOME="${KIROCREW_HOME:-$HOME/.kiro/crew}"
MODE="link"; WORKSPACE=0
for arg in "$@"; do
  case "$arg" in
    --copy) MODE="copy" ;;
    --workspace) WORKSPACE=1 ;;
    -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
    *) echo "unknown flag: $arg" >&2; exit 2 ;;
  esac
done

TARGETS=("$KIRO_HOME/skills" "$CREW_HOME/skills")
[ "$WORKSPACE" = 1 ] && TARGETS+=("$PWD/.kiro/skills")

place() { # $1 = skill dir in repo, $2 = target skills dir
  local src="$1" dst_dir="$2" name; name="$(basename "$src")"
  mkdir -p "$dst_dir"
  local dst="$dst_dir/$name"
  if [ -e "$dst" ] && [ ! -L "$dst" ] && [ "$MODE" = "link" ]; then
    echo "  skip  $dst  (real directory exists; remove it or use --copy)"; return
  fi
  rm -rf "$dst"
  if [ "$MODE" = "link" ]; then ln -s "$src" "$dst"; echo "  link  $dst -> $src"
  else cp -R "$src" "$dst"; echo "  copy  $dst"; fi
}

echo "kiro-skills installer ($MODE)"
for skill in "$HERE"/*/; do
  [ -f "$skill/SKILL.md" ] || continue
  skill="${skill%/}"
  echo "$(basename "$skill"):"
  for t in "${TARGETS[@]}"; do place "$skill" "$t"; done
  find "$skill/scripts" -name '*.py' -exec chmod +x {} + 2>/dev/null || true
done
echo
echo "Done. Restart Kiro IDE/CLI (or start a new chat in Crew) to pick up the skills."
echo "Invoke with /blog-writer or just ask: \"write a blog about what I built\"."
