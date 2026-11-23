#!/usr/bin/env python3
"""
Generates the 3 missing SVGs for Chapter 2:
- ch02-l01-q05.svg
- ch02-l02-q05.svg
- ch02-l03-q05.svg
"""

import os

images_dir = "images/chapter-02"
os.makedirs(images_dir, exist_ok=True)

svg_data = {
    "ch02-l01-q05.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <defs>
    <linearGradient id="labBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#e2e8f0"/>
    </linearGradient>
    <linearGradient id="bench" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#94a3b8"/>
      <stop offset="100%" stop-color="#64748b"/>
    </linearGradient>
  </defs>
  <rect width="600" height="400" fill="url(#labBg)"/>
  <rect y="310" width="600" height="90" fill="#cbd5e1"/>
  <!-- Laboratory Bench -->
  <rect x="80" y="240" width="440" height="100" fill="url(#bench)" rx="4"/>
  <!-- Lab shelf with test tubes/flasks -->
  <rect x="100" y="80" width="220" height="12" fill="#64748b" rx="2"/>
  <rect x="120" y="55" width="18" height="25" fill="#38bdf8" opacity="0.8" rx="2"/>
  <rect x="150" y="50" width="22" height="30" fill="#a855f7" opacity="0.8" rx="2"/>
  <rect x="185" y="58" width="16" height="22" fill="#10b981" opacity="0.8" rx="2"/>
  <!-- Microscope -->
  <rect x="230" y="225" width="60" height="16" fill="#1e293b" rx="3"/>
  <rect x="250" y="165" width="16" height="60" fill="#334155"/>
  <path d="M 245 160 L 275 140 L 265 125 L 235 145 Z" fill="#0f172a"/>
  <circle cx="270" cy="130" r="8" fill="#38bdf8"/>
  <rect x="235" y="195" width="30" height="6" fill="#0f172a"/>
  <!-- Scientist standing, leaning slightly forward -->
  <rect x="330" y="240" width="22" height="90" fill="#1e293b"/>
  <rect x="365" y="240" width="22" height="90" fill="#1e293b"/>
  <!-- White lab coat -->
  <path d="M 320 160 L 390 160 L 405 270 L 310 270 Z" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
  <!-- Head with safety goggles -->
  <circle cx="340" cy="130" r="22" fill="#fed7aa"/>
  <rect x="325" y="125" width="22" height="8" rx="3" fill="#0284c7" opacity="0.9"/>
  <!-- Arm reaching toward microscope adjustment knob -->
  <path d="M 330 180 Q 295 200 270 205" stroke="#ffffff" stroke-width="16" fill="none" stroke-linecap="round"/>
  <circle cx="270" cy="205" r="7" fill="#fed7aa"/>
  <!-- Label bar -->
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L01-Q05: Scientist in lab coat looking through microscope</text>
</svg>""",

    "ch02-l02-q05.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <defs>
    <linearGradient id="skyBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#e0f2fe"/>
      <stop offset="100%" stop-color="#bae6fd"/>
    </linearGradient>
    <linearGradient id="patio" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f1f5f9"/>
      <stop offset="100%" stop-color="#cbd5e1"/>
    </linearGradient>
  </defs>
  <rect width="600" height="400" fill="url(#skyBg)"/>
  <!-- Patio / Outdoor cafe ground -->
  <rect y="240" width="600" height="160" fill="url(#patio)"/>
  <!-- Patio tile lines -->
  <line x1="0" y1="280" x2="600" y2="280" stroke="#94a3b8" stroke-width="1"/>
  <line x1="0" y1="330" x2="600" y2="330" stroke="#94a3b8" stroke-width="1"/>
  <!-- Background cafe building facade -->
  <rect x="0" y="60" width="600" height="180" fill="#f8fafc"/>
  <rect x="40" y="90" width="140" height="110" fill="#38bdf8" opacity="0.3" stroke="#64748b" stroke-width="2"/>
  <rect x="420" y="90" width="140" height="110" fill="#38bdf8" opacity="0.3" stroke="#64748b" stroke-width="2"/>
  <rect x="230" y="80" width="140" height="160" fill="#475569"/>
  <!-- Left Table & Umbrella -->
  <polygon points="150,80 70,150 230,150" fill="#ea580c"/>
  <line x1="150" y1="150" x2="150" y2="290" stroke="#334155" stroke-width="6"/>
  <!-- Round table -->
  <ellipse cx="150" cy="270" rx="45" ry="14" fill="#64748b"/>
  <!-- Empty chairs -->
  <rect x="85" y="245" width="20" height="45" fill="#475569" rx="2"/>
  <rect x="195" y="245" width="20" height="45" fill="#475569" rx="2"/>
  <!-- Right Table & Umbrella -->
  <polygon points="450,80 370,150 530,150" fill="#2563eb"/>
  <line x1="450" y1="150" x2="450" y2="290" stroke="#334155" stroke-width="6"/>
  <!-- Round table -->
  <ellipse cx="450" cy="270" rx="45" ry="14" fill="#64748b"/>
  <!-- Empty chairs -->
  <rect x="385" y="245" width="20" height="45" fill="#475569" rx="2"/>
  <rect x="495" y="245" width="20" height="45" fill="#475569" rx="2"/>
  <!-- Label bar -->
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L02-Q05: Outdoor cafe seating with opened umbrellas, no people</text>
</svg>""",

    "ch02-l03-q05.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <defs>
    <linearGradient id="lobbyWall" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <radialGradient id="lightGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fef08a" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#fef08a" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <!-- High ceiling lobby wall -->
  <rect width="600" height="400" fill="url(#lobbyWall)"/>
  <!-- Polished floor with reflection -->
  <rect y="310" width="600" height="90" fill="#334155"/>
  <!-- High architectural columns -->
  <rect x="40" y="0" width="35" height="310" fill="#475569"/>
  <rect x="525" y="0" width="35" height="310" fill="#475569"/>
  <!-- Multiple pendant lighting fixtures suspended from high ceiling -->
  <!-- Fixture 1 -->
  <line x1="150" y1="0" x2="150" y2="140" stroke="#94a3b8" stroke-width="2"/>
  <circle cx="150" cy="155" r="28" fill="url(#lightGlow)"/>
  <ellipse cx="150" cy="145" rx="18" ry="10" fill="#f59e0b"/>
  <circle cx="150" cy="150" r="8" fill="#ffffff"/>
  <!-- Fixture 2 (center, lower) -->
  <line x1="300" y1="0" x2="300" y2="170" stroke="#94a3b8" stroke-width="2"/>
  <circle cx="300" cy="185" r="32" fill="url(#lightGlow)"/>
  <ellipse cx="300" cy="175" rx="22" ry="12" fill="#f59e0b"/>
  <circle cx="300" cy="180" r="10" fill="#ffffff"/>
  <!-- Fixture 3 -->
  <line x1="450" y1="0" x2="450" y2="130" stroke="#94a3b8" stroke-width="2"/>
  <circle cx="450" cy="145" r="28" fill="url(#lightGlow)"/>
  <ellipse cx="450" cy="135" rx="18" ry="10" fill="#f59e0b"/>
  <circle cx="450" cy="140" r="8" fill="#ffffff"/>
  <!-- Floor reflections -->
  <ellipse cx="150" cy="330" rx="35" ry="8" fill="#fef08a" opacity="0.2"/>
  <ellipse cx="300" cy="340" rx="45" ry="10" fill="#fef08a" opacity="0.3"/>
  <ellipse cx="450" cy="330" rx="35" ry="8" fill="#fef08a" opacity="0.2"/>
  <!-- Label bar -->
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L03-Q05: Multiple pendant lighting fixtures suspended from high ceiling</text>
</svg>"""
}

for fname, content in svg_data.items():
    fpath = os.path.join(images_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Generated {fpath}")

print("Missing SVGs successfully created!")
