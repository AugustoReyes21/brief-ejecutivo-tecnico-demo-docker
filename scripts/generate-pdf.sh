#!/bin/sh
set -eu

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
INPUT_HTML="$ROOT_DIR/docs/entrega.html"
OUTPUT_PDF="$ROOT_DIR/docs/brief-entrega.pdf"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

if [ ! -x "$CHROME" ]; then
  echo "Google Chrome no esta disponible en: $CHROME" >&2
  exit 1
fi

"$CHROME" \
  --headless=new \
  --disable-gpu \
  --allow-file-access-from-files \
  --virtual-time-budget=10000 \
  --print-to-pdf="$OUTPUT_PDF" \
  "file://$INPUT_HTML"

echo "PDF generado en: $OUTPUT_PDF"
