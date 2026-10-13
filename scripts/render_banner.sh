#!/usr/bin/env bash
# Render assets/askajay-github-banner.svg to a 2x JPEG with the brand fonts.
# Needs macOS (sips), Google Chrome and a checkout of aiexponent-brand (for the font files).
# Usage: BRAND_ROOT=/path/to/aiexponent-brand scripts/render_banner.sh
set -euo pipefail
cd "$(dirname "$0")/.."

: "${BRAND_ROOT:?set BRAND_ROOT to your aiexponent-brand checkout}"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
FONTS="$BRAND_ROOT/foundation/fonts"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

cat > "$WORK/banner.html" <<HTML
<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Clash Display';font-weight:400;src:url('file://$FONTS/clash-display-400.woff2')}
@font-face{font-family:'Clash Display';font-weight:500;src:url('file://$FONTS/clash-display-500.woff2')}
@font-face{font-family:'Clash Display';font-weight:600;src:url('file://$FONTS/clash-display-600.woff2')}
@font-face{font-family:'JetBrains Mono';font-weight:500;src:url('file://$FONTS/jetbrains-500.woff2')}
@font-face{font-family:'Playfair Display';font-weight:400;src:url('file://$FONTS/playfair-400.woff2')}
@font-face{font-family:'Playfair Display';font-weight:700;src:url('file://$FONTS/playfair-700.woff2')}
html,body{margin:0;padding:0;background:#0A0A0A}
svg{display:block;width:1280px;height:320px}
</style></head><body>
$(cat assets/askajay-github-banner.svg)
</body></html>
HTML

"$CHROME" --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files \
  --force-device-scale-factor=2 --window-size=1280,320 --virtual-time-budget=3000 \
  --screenshot="$WORK/banner.png" "file://$WORK/banner.html" 2>/dev/null
sips -s format jpeg -s formatOptions 88 "$WORK/banner.png" --out assets/askajay-github-banner.jpg >/dev/null
echo "wrote assets/askajay-github-banner.jpg"
