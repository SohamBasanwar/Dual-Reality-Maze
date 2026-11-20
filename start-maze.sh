#!/usr/bin/env bash
# Launch the standalone game beside this script. No server or packages required.
set -euo pipefail
maze_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
maze_file="$maze_dir/Dual_Reality_Maze_Story_Edition.html"
if [[ ! -f "$maze_file" ]]; then
  printf 'Game file not found: %s\n' "$maze_file" >&2
  exit 1
fi
if [[ "${1:-}" == '--check' ]]; then
  printf 'Ready to open: %s\n' "$maze_file"
  exit 0
fi
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*)
    maze_windows_file="$(cygpath -w "$maze_file")"
    MAZE_HTML_PATH="$maze_windows_file" powershell.exe -NoProfile -Command 'Invoke-Item -LiteralPath $env:MAZE_HTML_PATH'
    ;;
  Darwin*) open "$maze_file" ;;
  Linux*)
    if command -v wslpath >/dev/null 2>&1 && command -v powershell.exe >/dev/null 2>&1; then
      maze_windows_file="$(wslpath -w "$maze_file")"
      MAZE_HTML_PATH="$maze_windows_file" WSLENV="${WSLENV:+$WSLENV:}MAZE_HTML_PATH" powershell.exe -NoProfile -Command 'Invoke-Item -LiteralPath $env:MAZE_HTML_PATH'
    elif command -v xdg-open >/dev/null 2>&1; then
      xdg-open "$maze_file"
    else
      printf 'Open this file in your browser: %s\n' "$maze_file"
    fi
    ;;
  *) printf 'Open this file in your browser: %s\n' "$maze_file" ;;
esac
