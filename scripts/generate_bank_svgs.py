#!/usr/bin/env python3
"""
Generates 30 SVG illustrations for Part 1 questions in CHAPTER_02_BANK.md
- CH02-BNK-A01 to A10 (L01: Người và hành động)
- CH02-BNK-L01 to L10 (L02: Vị trí và đồ vật)
- CH02-BNK-V01 to V10 (L03: Bị động, trạng thái và suy diễn)
"""

import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK_PATH = os.path.join(ROOT_DIR, "CHAPTER_02_BANK.md")
IMG_DIR = os.path.join(ROOT_DIR, "images", "chapter-02")
os.makedirs(IMG_DIR, exist_ok=True)

def generate_svg(qid, desc, index, theme="indoor"):
    # Determine color palette based on theme
    palettes = {
        "indoor": {"bg1": "#f8fafc", "bg2": "#e2e8f0", "floor": "#cbd5e1", "accent": "#2563eb", "sec": "#64748b"},
        "outdoor": {"bg1": "#e0f2fe", "bg2": "#bae6fd", "floor": "#86efac", "accent": "#15803d", "sec": "#475569"},
        "warehouse": {"bg1": "#f1f5f9", "bg2": "#cbd5e1", "floor": "#94a3b8", "accent": "#ea580c", "sec": "#334155"}
    }
    pal = palettes.get(theme, palettes["indoor"])

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_{qid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{pal['bg1']}"/>
      <stop offset="100%" stop-color="{pal['bg2']}"/>
    </linearGradient>
  </defs>
  <rect width="600" height="400" fill="url(#bg_{qid})"/>
  <rect y="290" width="600" height="110" fill="{pal['floor']}"/>
  <!-- Decorative background elements -->
  <rect x="50" y="50" width="160" height="110" rx="4" fill="#ffffff" opacity="0.6" stroke="#94a3b8" stroke-width="2"/>
  <rect x="390" y="50" width="160" height="110" rx="4" fill="#ffffff" opacity="0.6" stroke="#94a3b8" stroke-width="2"/>
  <!-- Subject representation box/graphic -->
  <g transform="translate(150, 120)">
    <rect x="40" y="60" width="220" height="110" rx="8" fill="{pal['sec']}" opacity="0.85"/>
    <circle cx="150" cy="40" r="28" fill="{pal['accent']}"/>
    <rect x="110" y="75" width="80" height="8" rx="4" fill="#ffffff"/>
    <rect x="90" y="95" width="120" height="8" rx="4" fill="#ffffff" opacity="0.8"/>
  </g>
  <!-- Label bar -->
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#f8fafc" text-anchor="middle">{qid}: {desc[:70]}</text>
</svg>"""
    return svg

def main():
    with open(BANK_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    p1_tables = re.findall(r'## (A\d\.[^\n]+)\n\n(\| ID \|[^\n]+\|\n\|[-| :]+\|\n(?:\|[^\n]+\|\n?)+)', text)
    count = 0

    for sec_name, tbl in p1_tables:
        lines = [l.strip() for l in tbl.strip().split('\n') if l.strip()][2:]
        for idx, line in enumerate(lines):
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 2:
                item_code = parts[0]
                desc = parts[1]
                qid = f"CH02-BNK-{item_code}"
                fname = f"ch02-bnk-{item_code.lower()}.svg"
                fpath = os.path.join(IMG_DIR, fname)

                theme = "outdoor" if any(w in desc.lower() for w in ["cây", "sân", "ngoài trời", "đậu", "đỗ", "đường", "công viên"]) else "warehouse" if any(w in desc.lower() for w in ["kho", "thùng", "xe tải", "xưởng"]) else "indoor"
                svg_content = generate_svg(qid, desc, idx, theme)

                with open(fpath, "w", encoding="utf-8") as out_f:
                    out_f.write(svg_content.strip())
                count += 1

    print(f"Successfully generated {count} Part 1 bank SVG files in {IMG_DIR}!")

if __name__ == "__main__":
    main()
