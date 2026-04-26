"""
inline_dashboard.py
===================
Read grant_overview_dashboard.html and replace the two `fetch(...)` calls
with inline JSON. The result is a single self-contained HTML file that
can be opened directly with a double-click — no local web server needed.
This matters for live conference presentation use.
"""

import json
from pathlib import Path

VIZ_DIR = Path("/sessions/charming-dreamy-thompson/mnt/climate-disability-risk/visualizations")
SRC = VIZ_DIR / "grant_overview_dashboard.html"
OUT = VIZ_DIR / "grant_overview_dashboard_standalone.html"

TOPO_JSON = (VIZ_DIR / "_dashboard_counties_topo.json").read_text()
DATA_JSON = (VIZ_DIR / "_dashboard_county_data.json").read_text()

html = SRC.read_text()

# Build the inline-data block. We expose the payloads as window globals
# so the existing fetch() block can use them as a fallback.
inline_block = (
    "<script id=\"inline-data\">\n"
    "// Pre-baked payloads — inlined so this file works via file://\n"
    f"window.__COUNTIES_TOPO__ = {TOPO_JSON};\n"
    f"window.__COUNTIES_DATA__ = {DATA_JSON};\n"
    "</script>\n"
)

# Inject inline block right before the main <script> that boots the app.
marker = "<script>\n// ---------------------------------------------------------------\n// Data plumbing — loaded from sibling JSON files at runtime."
assert marker in html, "Boot script marker not found — file structure changed."
html = html.replace(marker, inline_block + marker)

# Replace the Promise.all([fetch(TOPO_URL).then(r => r.json()), fetch(DATA_URL).then(r => r.json())])
# block with a synchronous resolution from window globals.
old_fetch = (
    "Promise.all([\n"
    "  fetch(TOPO_URL).then(r => r.json()),\n"
    "  fetch(DATA_URL).then(r => r.json()),\n"
    "]).then(([topo, data]) => {"
)
new_fetch = (
    "Promise.resolve([window.__COUNTIES_TOPO__, window.__COUNTIES_DATA__])\n"
    "  .then(([topo, data]) => {"
)
assert old_fetch in html, "fetch block not found — file structure changed."
html = html.replace(old_fetch, new_fetch)

OUT.write_text(html)
print(f"Wrote {OUT}  ({OUT.stat().st_size/1024:.0f} KB)")
