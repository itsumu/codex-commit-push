#!/bin/sh
set -eu
src=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)/commit-push
dst=${CODEX_HOME:-"$HOME/.codex"}/skills/commit-push
alias_value="!codex '\$commit-push'"
current=$(git config --global --get-all alias.codex-push || :)
fail() { printf '%s\n' "$*" >&2; exit 1; }
case "${1:-install}" in
  install)
    command -v codex >/dev/null || fail 'Missing Codex CLI'
    command -v python3 >/dev/null || fail 'Missing Python 3'
    [ -z "$current" ] || [ "$current" = "$alias_value" ] || fail 'Conflicting git alias: codex-push'
    if [ -e "$dst" ] || [ -L "$dst" ]; then
      diff -qr "$src" "$dst" >/dev/null || fail 'Existing skill differs; leaving it untouched.'
    else
      mkdir -p "$(dirname "$dst")"
      cp -R "$src" "$dst"
    fi
    if [ -z "$current" ]; then git config --global alias.codex-push "$alias_value"; fi
    printf '%s\n' 'Ready: git codex-push'
    ;;
  --uninstall)
    if [ -d "$dst" ]; then
      [ ! -L "$dst" ] && diff -qr "$src" "$dst" >/dev/null || fail 'Skill changed; refusing to remove it.'
      rm -- "$dst/SKILL.md" "$dst/scripts/publish.py"
      rmdir -- "$dst/scripts" "$dst"
    fi
    if [ "$current" = "$alias_value" ]; then git config --global --unset alias.codex-push; fi
    ;;
  *) fail 'Usage: sh install.sh [--uninstall]' ;;
esac
