import datetime
import json
import os
import urllib.request
from html import escape

GITHUB_USER = "CESARBR2025"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
ASCII_PATH = os.path.join(SCRIPT_DIR, "ascii_lines.txt")

with open(ASCII_PATH) as f:
    ascii_lines = f.read().splitlines()


def fetch_github_stats():
    headers = {"User-Agent": "profile-card-script"}
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{GITHUB_USER}", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            profile = json.load(r)

        req = urllib.request.Request(f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            repos = json.load(r)
    except Exception as e:
        print(f"WARN: could not fetch GitHub stats ({e}), using fallback values")
        return {"public_repos": "-", "top_langs": "-", "last_push": "-"}

    public_repos = profile.get("public_repos", len(repos))

    lang_counts = {}
    for r in repos:
        if r.get("fork"):
            continue
        lang = r.get("language")
        if lang:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
    top_langs = sorted(lang_counts, key=lang_counts.get, reverse=True)[:3]

    active_repos = [r for r in repos if not r.get("fork") and r.get("pushed_at")]
    last_push = "-"
    if active_repos:
        latest = max(active_repos, key=lambda r: r["pushed_at"])
        dt = datetime.datetime.strptime(latest["pushed_at"], "%Y-%m-%dT%H:%M:%SZ").date()
        last_push = f"{dt.isoformat()} ({latest['name']})"

    return {
        "public_repos": str(public_repos),
        "top_langs": ", ".join(top_langs) if top_langs else "-",
        "last_push": last_push,
    }


STATS = fetch_github_stats()

# ---- info rows: (kind, key, value) ----
# kind: "header" | "field" | "field2" | "blank" | "section"
rows = [
    ("header", "cesar@devos", None),
    ("field", "Subject", "Cesar Ivan Barcenas Rosales"),
    ("field", "Role", "Full-Stack Developer"),
    ("field", "Origin", "San Juan del Rio, Qro. Mexico"),
    ("field", "Education", "Ing. Sistemas Computacionales (ITSJR)"),
    ("field", "Status", "Employed - Open to freelance projects"),
    ("field", "ToolChain", "VS Code, Git, Docker, GitHub"),
    ("blank", None, None),
    ("field2", "Core.Lang", "JavaScript/TypeScript, Python"),
    ("field2", "Core.Frontend", "Next.js, React"),
    ("field2", "Core.Backend", "Django, FastAPI, Node.js"),
    ("field2", "Core.Database", "PostgreSQL (Supabase)"),
    ("field2", "Core.Infra", "Docker, GitHub Actions"),
    ("blank", None, None),
    ("section", "Contact", None),
    ("field2", "Grid.Mail", "barcenasrosalescesarivan@gmail.com"),
    ("field2", "Grid.Portfolio", "portafolio-personal-six-phi.vercel.app"),
    ("field2", "Grid.Github", "CESARBR2025"),
    ("blank", None, None),
    ("section", "Live Stats", None),
    ("field2", "Public Repos", STATS["public_repos"]),
    ("field2", "Top Langs", STATS["top_langs"]),
    ("field2", "Last Push", STATS["last_push"]),
]

ROW_HEIGHT = 20


def dots(n):
    return "." * max(n, 2)


def build_rows_markup():
    clip_defs = []
    groups = []
    for i, (kind, key, value) in enumerate(rows):
        rect_y = 26 + i * ROW_HEIGHT
        text_y = rect_y + 16
        begin = 0.75 + i * 0.105
        clip_id = f"lc{i}"
        clip_defs.append(
            f'<clipPath id="{clip_id}"><rect x="500" y="{rect_y:.2f}" width="0" height="{ROW_HEIGHT + 2}">'
            f'<animate attributeName="width" from="0" to="690" dur="0.35s" begin="{begin:.2f}s" fill="freeze"/>'
            f'</rect></clipPath>'
        )

        if kind == "header":
            inner = (
                f'<tspan x="520" y="{text_y}" class="head">{escape(key)}</tspan>'
                f'<tspan class="cc"> -—————————————————————————————————————————————-—-</tspan>'
            )
        elif kind == "section":
            inner = (
                f'<tspan x="520" y="{text_y}" class="accent">- {escape(key)}</tspan>'
                f'<tspan class="cc"> -————————————————————————————————————————————-—-</tspan>'
            )
        elif kind == "blank":
            inner = f'<tspan x="520" y="{text_y}" class="cc">. </tspan>'
        elif kind in ("field", "field2"):
            prefix_len = 2 + len(key) + 2
            target = 34
            max_total = 66
            max_dot = max_total - prefix_len - 1 - len(value)
            dot_count = max(3, min(target - prefix_len, max_dot))
            if "." in key:
                first, rest = key.split(".", 1)
                key_markup = f'<tspan class="key">{escape(first)}</tspan><tspan class="cc">.</tspan><tspan class="key">{escape(rest)}</tspan>'
            else:
                key_markup = f'<tspan class="key">{escape(key)}</tspan>'
            inner = (
                f'<tspan x="520" y="{text_y}" class="cc">. </tspan>'
                f'{key_markup}'
                f'<tspan class="cc">: {dots(dot_count)} </tspan>'
                f'<tspan class="value">{escape(value)}</tspan>'
            )
        groups.append(f'<g clip-path="url(#{clip_id})"><text x="520" y="0" fill="#dbeafe">{inner}</text></g>')

    last_i = len(rows) - 1
    cursor_y = 26 + last_i * ROW_HEIGHT + 1
    cursor_begin = 0.75 + len(rows) * 0.105 + 0.5
    return "".join(clip_defs), "".join(groups), cursor_y, cursor_begin


CLIP_DEFS, ROW_GROUPS, CURSOR_Y, CURSOR_BEGIN = build_rows_markup()

ASCII_TSPANS = "\n".join(
    f'<tspan x="30" y="{79.98 + i * 7.55:.2f}" xml:space="preserve">{escape(line) if line.strip() else " "}</tspan>'
    for i, line in enumerate(ascii_lines)
)

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610">
<defs>
  <linearGradient id="asciiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{c_ascii1}">
      <animate attributeName="stop-color" values="{c_ascii1};{c_ascii2};{c_ascii3};{c_ascii1}" dur="9s" repeatCount="indefinite"/>
    </stop>
    <stop offset="100%" stop-color="{c_ascii2}">
      <animate attributeName="stop-color" values="{c_ascii2};{c_ascii3};{c_ascii1};{c_ascii2}" dur="9s" repeatCount="indefinite"/>
    </stop>
  </linearGradient>
  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{c_border1}"/>
    <stop offset="50%" stop-color="{c_border2}"/>
    <stop offset="100%" stop-color="{c_border3}"/>
  </linearGradient>
  <radialGradient id="bgGlow" cx="30%" cy="20%" r="80%">
    <stop offset="0%" stop-color="{c_bg1}"/>
    <stop offset="100%" stop-color="{c_bg2}"/>
  </radialGradient>
  <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%" stop-color="{c_scan}" stop-opacity="0"/>
  <stop offset="45%" stop-color="{c_scan}" stop-opacity="{scan_op1}"/>
  <stop offset="50%" stop-color="{c_scan_mid}" stop-opacity="{scan_op2}"/>
  <stop offset="55%" stop-color="{c_scan}" stop-opacity="{scan_op1}"/>
  <stop offset="100%" stop-color="{c_border1}" stop-opacity="0"/>
</linearGradient>
  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
  <rect width="4" height="1" fill="{c_scanline}" opacity="{scanline_op}"/>
</pattern>
  <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="4" result="blur"/>
  <feMerge>
    <feMergeNode in="blur"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
  <mask id="revealMask" maskUnits="userSpaceOnUse" x="0" y="0" width="1180" height="620">
  <rect x="0" y="0" width="1180" height="0" fill="#fff">
    <animate attributeName="height" from="0" to="560" dur="2.6s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
  </rect>
</mask>
  {clip_defs}
  <style>
    .ascii  {{ font-family: 'Courier New', Consolas, monospace; font-size: 7.4px; fill: url(#asciiGrad); letter-spacing: -0.2px; }}
    .key    {{ font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: {c_key}; font-weight: bold; }}
    .value  {{ font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: {c_value}; }}
    .cc     {{ font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: {c_cc}; }}
    .head   {{ font-family: 'Courier New', Consolas, monospace; font-size: 17px; fill: {c_head}; font-weight: bold; }}
    .accent {{ font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: {c_accent}; font-weight: bold; }}
    text, tspan {{ white-space: pre; }}

    .term-label {{ font-family: 'Courier New', Consolas, monospace; font-size: 12px; fill: {c_term}; letter-spacing: 0.5px; }}
    .scan-label {{ font-family: 'Courier New', Consolas, monospace; font-size: 10px; fill: {c_scanlabel}; letter-spacing: 1px; }}
    .panel-title {{ font-family: 'Courier New', Consolas, monospace; font-size: 11px; fill: {c_paneltitle}; letter-spacing: 2px; opacity: {paneltitle_op}; }}
    .cursor-blink {{ fill: {c_cursor}; }}

  </style>
</defs>

<rect width="1180" height="610" rx="18" fill="url(#bgGlow)"/>
<rect width="1180" height="610" rx="18" fill="url(#scanlines)"/>

<g id="titlebar">
  <rect x="3" y="3" width="1174" height="34" rx="16" fill="{c_titlebar}" fill-opacity="{titlebar_op}"/>
  <circle cx="24" cy="20" r="5" fill="{c_dot1}"><animate attributeName="opacity" values="1;0.55;1" dur="4s" repeatCount="indefinite"/></circle>
  <circle cx="42" cy="20" r="5" fill="{c_dot2}"><animate attributeName="opacity" values="1;0.55;1" dur="4s" begin="0.3s" repeatCount="indefinite"/></circle>
  <circle cx="60" cy="20" r="5" fill="{c_dot3}"><animate attributeName="opacity" values="1;0.55;1" dur="4s" begin="0.6s" repeatCount="indefinite"/></circle>
  <text x="590" y="25" text-anchor="middle" class="term-label">cesar@devos ~ % ./profile.sh --live</text>
  <circle cx="1122" cy="20" r="4" fill="{c_scandot}">
    <animate attributeName="opacity" values="1;0.15;1" dur="1.1s" repeatCount="indefinite"/>
  </circle>
  <text x="1132" y="24" class="scan-label">SCANNING</text>
</g>

<g transform="translate(0,38)">
  <rect x="14" y="26" width="488" height="468" rx="14" fill="{c_panel}" fill-opacity="{panel_op}" stroke="url(#borderGrad)" stroke-width="1" opacity="0.35"/>
  <rect x="508" y="10" width="655" height="500" rx="14" fill="{c_panel}" fill-opacity="{panel_op}" stroke="url(#borderGrad)" stroke-width="1" opacity="0.35"/>
  <text x="30" y="24" class="panel-title">VISUAL.MAP</text>
  <text x="524" y="24" class="panel-title">SYSTEM.INFO</text>

  <g mask="url(#revealMask)">
  <text x="30" y="0" class="ascii">

{ascii_tspans}

  </text>
  </g>

  {row_groups}

  <rect x="522" y="{cursor_y:.1f}" width="9" height="16" class="cursor-blink" opacity="0">
    <animate attributeName="opacity" values="0;0;1;0;1;0;1;0" keyTimes="0;0.01;0.02;0.3;0.5;0.7;0.85;1" dur="1.4s" begin="{cursor_begin:.2f}s" repeatCount="indefinite"/>
  </rect>
</g>

<rect x="0" y="-70" width="1180" height="70" fill="url(#scanGrad)" opacity="0.7" style="mix-blend-mode:screen">
  <animateTransform attributeName="transform" type="translate" from="0 -70" to="0 680" dur="4.2s" repeatCount="indefinite"/>
</rect>

<rect x="3" y="3" width="1174" height="604" rx="16" fill="none" stroke="url(#borderGrad)" stroke-width="2" opacity="0.8">
  <animate attributeName="opacity" values="0.5;0.95;0.5" dur="3.2s" repeatCount="indefinite"/>
</rect>
</svg>
"""

dark_colors = dict(
    c_ascii1="#22D3EE", c_ascii2="#7C3AED", c_ascii3="#38BDF8",
    c_border1="#7C3AED", c_border2="#22D3EE", c_border3="#10B981",
    c_bg1="#0B1120", c_bg2="#050816",
    c_scan="#22D3EE", c_scan_mid="#A5F3FC", scan_op1="0.05", scan_op2="0.65",
    c_scanline="#7DD3FC", scanline_op="0.05",
    c_key="#22D3EE", c_value="#E5E7EB", c_cc="#475569", c_head="#7C3AED", c_accent="#10B981",
    c_term="#64748B", c_scanlabel="#F87171", c_paneltitle="#38BDF8", paneltitle_op="0.7",
    c_cursor="#22D3EE",
    c_titlebar="#0B1120", titlebar_op="0.85",
    c_dot1="#EF4444", c_dot2="#F59E0B", c_dot3="#10B981", c_scandot="#F87171",
    c_panel="#0B1120", panel_op="0.35",
)

light_colors = dict(
    c_ascii1="#4F46E5", c_ascii2="#7C3AED", c_ascii3="#0EA5E9",
    c_border1="#7C3AED", c_border2="#0EA5E9", c_border3="#059669",
    c_bg1="#F8FAFC", c_bg2="#E2E8F0",
    c_scan="#0EA5E9", c_scan_mid="#38BDF8", scan_op1="0.06", scan_op2="0.55",
    c_scanline="#334155", scanline_op="0.035",
    c_key="#0284C7", c_value="#1E293B", c_cc="#94A3B8", c_head="#7C3AED", c_accent="#059669",
    c_term="#64748B", c_scanlabel="#DC2626", c_paneltitle="#0284C7", paneltitle_op="0.75",
    c_cursor="#0EA5E9",
    c_titlebar="#FFFFFF", titlebar_op="0.9",
    c_dot1="#F87171", c_dot2="#FBBF24", c_dot3="#34D399", c_scandot="#EF4444",
    c_panel="#FFFFFF", panel_op="0.55",
)

for name, colors in (("dark", dark_colors), ("light", light_colors)):
    svg = TEMPLATE.format(
        clip_defs=CLIP_DEFS,
        ascii_tspans=ASCII_TSPANS,
        row_groups=ROW_GROUPS,
        cursor_y=CURSOR_Y,
        cursor_begin=CURSOR_BEGIN,
        **colors,
    )
    out_path = os.path.join(REPO_ROOT, f"{name}.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {out_path} ({len(svg)} bytes)")
