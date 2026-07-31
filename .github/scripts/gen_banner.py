#!/usr/bin/env python3
"""
Generate the animated terminal hero banner for the u1amd999 profile README.

Emits two files, dark.svg and light.svg, using the same design language as the
arifhaxn profile: macOS window chrome, animated accent gradient, an ASCII-art
panel with staggered fade-in, a SYSTEM.INFO panel with staggered slide-in rows,
a pulsing LIVE dot and a blinking block cursor.

Theme: matrix green / cyan / violet on near-black. Hacking / red-team flavor.
Run from repo root: python3 .github/scripts/gen_banner.py
"""
import os, html

# ---------------- themes ----------------
THEMES = {
    "dark": {
        "BG": "#0A0A12", "BG2": "#0E0E18", "TITLE_BAR": "#0C0C16",
        "TITLE_LINE": "rgba(248,250,252,0.08)", "TITLE_TXT": "#8B949E",
        "PANEL_STROKE": "rgba(34,211,238,0.45)", "PANEL_FILL": "#0B0B14",
        "LABEL": "#22D3EE", "VALUE": "#F8FAFC", "MUTED": "#8B949E",
        "DOTS": "rgba(248,250,252,0.18)", "SEP": "#475569",
        "ACC_0": "#22D3EE", "ACC_1": "#A78BFA", "ACC_2": "#10B981",
        "ACC_3": "#22D3EE",
        "SKULL": "#22D3EE", "SKULL2": "#A78BFA", "GLOW": "#22D3EE",
        "LIVE": "#DC2626", "FOOT": "#94A3B8", "CURSOR": "#00FF41",
    },
    "light": {
        "BG": "#F8FAFC", "BG2": "#EEF2F7", "TITLE_BAR": "#F1F5F9",
        "TITLE_LINE": "rgba(15,23,42,0.10)", "TITLE_TXT": "#475569",
        "PANEL_STROKE": "rgba(8,145,178,0.45)", "PANEL_FILL": "#FFFFFF",
        "LABEL": "#0E7490", "VALUE": "#0F172A", "MUTED": "#475569",
        "DOTS": "rgba(15,23,42,0.18)", "SEP": "#94A3B8",
        "ACC_0": "#0891B2", "ACC_1": "#7C3AED", "ACC_2": "#059669",
        "ACC_3": "#0891B2",
        "SKULL": "#0891B2", "SKULL2": "#7C3AED", "GLOW": "#0891B2",
        "LIVE": "#DC2626", "FOOT": "#475569", "CURSOR": "#059669",
    },
}

# ---------------- ASCII skull (44 x 29) ----------------
# '#' = solid bone, ' ' = hollow (eyes/nose/background)
SKULL = [
    "                    ####                    ",
    "                ############                ",
    "             ##################             ",
    "          ########################          ",
    "        ############################        ",
    "      ################################      ",
    "     ##################################     ",
    "    ####################################    ",
    "   ######################################   ",
    "   ######                    ##########    ",
    "   ######                    ##########    ",
    "   #######                  ###########    ",
    "   #######       ####        ###########    ",
    "   #######       ####        ###########    ",
    "   #######       ####        ###########    ",
    "   ########      ####       ############    ",
    "   ####################################    ",
    "    ####################################    ",
    "    ####################################    ",
    "    ####################################    ",
    "     ##################################     ",
    "      ######                  ######      ",
    "     ######                    ######     ",
    "     ######                    ######     ",
    "    ######                      ######    ",
    "    ######                      ######    ",
    "     #################################     ",
    "      ###############################      ",
    "        ###########################        ",
]

# ---------------- right panel rows ----------------
ROWS = [
    ("Operator",   "u1"),
    ("Division",   "Red Team / Offensive Security"),
    ("Motto",      "trust nothing, verify everything"),
    ("Status",     "ACTIVE - HUNTING IN THE WILD"),
    ("ToolChain",  "Nmap, Burp, ffuf, nuclei, sqlmap"),
    ("Core.Lang",  "Python, Go, Bash, JavaScript"),
    ("Core.Infra", "Kali, Docker, Git, Cloud VPS"),
    None,  # separator
    ("Mail",       "u1.999@proton.me"),
    ("GitHub",     "@u1amd999"),
]

W, H = 1180, 610
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

def esc(s):
    return html.escape(str(s), quote=True)

def dots_for(label, value, width=50):
    n = width - len(label) - len(value) - 2
    return "." * max(4, n)

def build(theme):
    t = THEMES[theme]
    a = []
    ap = a.append
    ap(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}" role="img" aria-label="u1 -- profile.sh --live">')
    ap('<defs>')
    ap(f'<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">')
    ap(f'<stop offset="0" stop-color="{t["ACC_0"]}"><animate attributeName="stop-color" values="{t["ACC_0"]};{t["ACC_1"]};{t["ACC_2"]};{t["ACC_0"]}" dur="10s" repeatCount="indefinite"/></stop>')
    ap(f'<stop offset="0.5" stop-color="{t["ACC_1"]}"><animate attributeName="stop-color" values="{t["ACC_1"]};{t["ACC_2"]};{t["ACC_0"]};{t["ACC_1"]}" dur="10s" repeatCount="indefinite"/></stop>')
    ap(f'<stop offset="1" stop-color="{t["ACC_2"]}"><animate attributeName="stop-color" values="{t["ACC_2"]};{t["ACC_0"]};{t["ACC_1"]};{t["ACC_2"]}" dur="10s" repeatCount="indefinite"/></stop>')
    ap('</linearGradient>')
    ap(f'<linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["BG"]}"/><stop offset="1" stop-color="{t["BG2"]}"/></linearGradient>')
    ap('<filter id="glow8" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="8"/></filter>')
    ap('<filter id="glow3" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3"/></filter>')
    ap(f'<filter id="txtGlow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="0.9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    ap('<clipPath id="winClip"><rect x="2" y="2" width="1176" height="606" rx="18"/></clipPath>')
    ap('</defs>')
    ap(f'<rect x="2" y="2" width="1176" height="606" rx="18" fill="{t["BG"]}"/>')
    ap('<g clip-path="url(#winClip)">')
    ap(f'<rect x="2" y="2" width="1176" height="606" fill="url(#panelGrad)"/>')
    ap(f'<rect x="2" y="2" width="1176" height="46" fill="{t["TITLE_BAR"]}"/>')
    ap(f'<line x1="2" y1="48" x2="1178" y2="48" stroke="{t["TITLE_LINE"]}"/>')
    ap('<circle cx="30" cy="25.0" r="5.5" fill="#ff5f56"/>')
    ap('<circle cx="50" cy="25.0" r="5.5" fill="#ffbd2e"/>')
    ap('<circle cx="70" cy="25.0" r="5.5" fill="#27c93f"/>')
    ap(f'<text x="590.0" y="29.0" text-anchor="middle" font-size="12" fill="{t["TITLE_TXT"]}">u1@kali:~/red-team$ ./u1.sh --live</text>')
    ap(f'<text x="38" y="74" font-size="10" letter-spacing="3" fill="{t["MUTED"]}">VISUAL.SCAN</text>')

    # --- left panel: ASCII skull, staggered fade-in per band ---
    ap(f'<rect x="36" y="84" width="400" height="492" rx="10" fill="none" stroke="{t["ACC_0"]}" stroke-width="2" opacity="0.45" filter="url(#glow3)"/>')
    ap(f'<rect x="36" y="84" width="400" height="492" rx="10" fill="{t["PANEL_FILL"]}" stroke="{t["PANEL_STROKE"]}"/>')
    cell_w = 400.0 / len(SKULL[0])
    cell_h = 492.0 / len(SKULL)
    begin = 0.2
    for row_idx, row in enumerate(SKULL):
        band = row_idx // 6  # 5 bands, each fades in sequence
        cols = [i for i, ch in enumerate(row) if ch == "#"]
        if not cols:
            continue
        ap(f'<g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.9s" begin="{begin + band * 0.30:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".4 0 .2 1"/>')
        for i in cols:
            x = 36 + i * cell_w + 1
            y = 84 + row_idx * cell_h + 1
            w = cell_w - 2
            h = cell_h - 2
            ap(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{t["SKULL"]}" shape-rendering="crispEdges"/>')
        ap('</g>')

    # --- right panel: SYSTEM.INFO ---
    ap(f'<text x="470" y="106" font-size="13" letter-spacing="2" fill="{t["LABEL"]}" filter="url(#txtGlow)">SYSTEM.INFO</text>')
    ap(f'<text x="1125" y="106" text-anchor="end" font-size="12" fill="{t["LIVE"]}" font-weight="700"><tspan>&#9679;</tspan> LIVE<animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></text>')

    y = 136
    delay = 0.6
    for row in ROWS:
        if row is None:
            ap(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay:.2f}s" fill="freeze"/><text x="470" y="{y}" font-size="14" fill="{t["SEP"]}">- Contact -------------------------------------------------------------------</text></g>')
            delay += 0.12
            y += 23
            continue
        label, value = row
        ap(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay:.2f}s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="{delay:.2f}s" fill="freeze"/><text x="470" y="{y}" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="{t["LABEL"]}">{esc(label)} </tspan><tspan fill="{t["DOTS"]}">{dots_for(label, value)}</tspan><tspan fill="{t["VALUE"]}" font-weight="600"> {esc(value)}</tspan></text></g>')
        delay += 0.12
        y += 23

    ap(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay + 0.2:.2f}s" fill="freeze"/>')
    ap(f'<text x="470" y="{y + 8}" font-size="14" fill="{t["FOOT"]}">&#9656; More about me &amp; projects below in README &#8595; <tspan fill="{t["CURSOR"]}">&#9608;<animate attributeName="fill-opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>')
    ap('</g>')
    ap('</g>')
    ap(f'<rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#accent)" stroke-width="3" opacity="0.55" filter="url(#glow8)"/>')
    ap(f'<rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#accent)" stroke-width="1.6"/>')
    ap('</svg>')
    return "".join(a)

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(os.path.dirname(here))
    for theme in ("dark", "light"):
        path = os.path.join(root, f"{theme}.svg")
        with open(path, "w") as f:
            f.write(build(theme))
        print(f"wrote {path}: {os.path.getsize(path) // 1024}KB")
