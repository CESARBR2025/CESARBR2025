import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(REPO_ROOT, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

WIDTH = 1180
HEIGHT = 54

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <linearGradient id="textGrad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="{c_g1}">
      <animate attributeName="stop-color" values="{c_g1};{c_g2};{c_g3};{c_g1}" dur="9s" repeatCount="indefinite"/>
    </stop>
    <stop offset="100%" stop-color="{c_g2}">
      <animate attributeName="stop-color" values="{c_g2};{c_g3};{c_g1};{c_g2}" dur="9s" repeatCount="indefinite"/>
    </stop>
  </linearGradient>
  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="{c_border1}"/>
    <stop offset="50%" stop-color="{c_border2}"/>
    <stop offset="100%" stop-color="{c_border3}"/>
  </linearGradient>
  <style>
    .title  {{ font-family: 'Courier New', Consolas, monospace; font-size: 20px; font-weight: bold; fill: url(#textGrad); letter-spacing: 2px; }}
    .prompt {{ font-family: 'Courier New', Consolas, monospace; font-size: 20px; font-weight: bold; fill: {c_accent}; }}
    .cursor {{ fill: {c_accent}; }}
  </style>
</defs>
<rect x="1" y="1" width="{width_m2}" height="{height_m2}" rx="12" fill="{c_bg}" fill-opacity="{bg_op}" stroke="url(#borderGrad)" stroke-width="1.5" opacity="0.9"/>
<text x="24" y="{text_y}" class="prompt">&gt;</text>
<text x="46" y="{text_y}" class="title">{title}</text>
<rect x="{cursor_x}" y="{cursor_y}" width="10" height="18" class="cursor">
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1.1s" repeatCount="indefinite"/>
</rect>
</svg>
"""

dark_colors = dict(
    c_g1="#22D3EE", c_g2="#7C3AED", c_g3="#10B981",
    c_border1="#7C3AED", c_border2="#22D3EE", c_border3="#10B981",
    c_bg="#0B1120", bg_op="0.55", c_accent="#22D3EE",
)

light_colors = dict(
    c_g1="#4F46E5", c_g2="#7C3AED", c_g3="#059669",
    c_border1="#7C3AED", c_border2="#0EA5E9", c_border3="#059669",
    c_bg="#FFFFFF", bg_op="0.7", c_accent="#0EA5E9",
)

SECTIONS = [
    ("header-projects", "FEATURED_PROJECTS.sh"),
    ("header-stack", "STACK.env"),
    ("header-orgs", "ORGANIZATIONS.sh"),
    ("header-network", "NETWORK.sh"),
    ("header-snake", "CONTRIBUTION_ACTIVITY.sh"),
]

CHAR_W = 14.2  # monospace advance at font-size 20px + 2px letter-spacing


def render(title, colors):
    text_y = HEIGHT // 2 + 7
    cursor_x = 46 + len(title) * CHAR_W + 10
    return TEMPLATE.format(
        width=WIDTH,
        height=HEIGHT,
        width_m2=WIDTH - 2,
        height_m2=HEIGHT - 2,
        text_y=text_y,
        cursor_x=cursor_x,
        cursor_y=text_y - 15,
        title=title,
        **colors,
    )


for slug, title in SECTIONS:
    for theme, colors in (("dark", dark_colors), ("light", light_colors)):
        svg = render(title, colors)
        path = os.path.join(ASSETS_DIR, f"{slug}-{theme}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {path}")
