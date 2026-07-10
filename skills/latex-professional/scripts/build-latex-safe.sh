#!/usr/bin/env sh
set -eu
ENGINE="pdf"
MAIN=""
ALLOW_SHELL_ESCAPE="${ALLOW_SHELL_ESCAPE:-0}"
usage() {
  echo "Usage: $0 [--pdf|--xelatex|--lualatex] [--allow-shell-escape] main.tex" >&2
}
while [ "$#" -gt 0 ]; do
  case "$1" in
    --pdf) ENGINE="pdf"; shift ;;
    --xelatex) ENGINE="pdfxe"; shift ;;
    --lualatex) ENGINE="pdflua"; shift ;;
    --allow-shell-escape) ALLOW_SHELL_ESCAPE="1"; shift ;;
    -*)
      echo "Unknown option: $1" >&2
      usage
      exit 2
      ;;
    *)
      MAIN="$1"
      shift
      ;;
  esac
done
if [ -z "$MAIN" ]; then
  usage
  exit 2
fi
if [ ! -f "$MAIN" ]; then
  echo "Main .tex file not found: $MAIN" >&2
  exit 2
fi
case "$ENGINE" in
  pdf) ENGINE_FLAG="-pdf" ;;
  pdfxe) ENGINE_FLAG="-pdfxe" ;;
  pdflua) ENGINE_FLAG="-pdflua" ;;
esac
SHELL_ESCAPE_FLAG=""
if [ "$ALLOW_SHELL_ESCAPE" = "1" ]; then
  echo "WARNING: shell escape explicitly enabled by user/environment." >&2
  SHELL_ESCAPE_FLAG="-shell-escape"
fi
exec latexmk "$ENGINE_FLAG" \
  -interaction=nonstopmode \
  -halt-on-error \
  -file-line-error \
  $SHELL_ESCAPE_FLAG \
  "$MAIN"
