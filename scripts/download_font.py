import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "css", "fonts")
os.makedirs(FONT_DIR, exist_ok=True)

url = 'https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,600&display=swap'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

print("Fetching Google Fonts CSS for Be Vietnam Pro...")
with urllib.request.urlopen(req) as res:
    css_content = res.read().decode('utf-8')

# Find all font-face blocks
blocks = re.findall(r'/\* ([^*]+) \*/\s*@font-face\s*\{([^}]+)\}', css_content)
print(f"Found {len(blocks)} font blocks")

local_css_lines = []
downloaded_files = {}

for subset, block in blocks:
    subset = subset.strip()
    # We especially want vietnamese and latin subsets
    if subset not in ["vietnamese", "latin", "latin-ext"]:
        continue

    # Extract properties
    style = re.search(r'font-style:\s*([^;]+);', block)
    weight = re.search(r'font-weight:\s*([^;]+);', block)
    src_url = re.search(r'url\((https://[^)]+\.woff2)\)', block)
    unicode_range = re.search(r'unicode-range:\s*([^;]+);', block)

    if not (style and weight and src_url):
        continue

    style_val = style.group(1).strip()
    weight_val = weight.group(1).strip()
    remote_url = src_url.group(1).strip()
    range_val = unicode_range.group(1).strip() if unicode_range else ""

    filename = f"be-vietnam-pro-{subset}-{weight_val}-{style_val}.woff2"
    filepath = os.path.join(FONT_DIR, filename)

    if not os.path.exists(filepath):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(remote_url, filepath)

    local_css_lines.append(f"""/* {subset} */
@font-face {{
  font-family: 'Be Vietnam Pro';
  font-style: {style_val};
  font-weight: {weight_val};
  font-display: swap;
  src: url('fonts/{filename}') format('woff2');
  {f"unicode-range: {range_val};" if range_val else ""}
}}""")

css_output_path = os.path.join(ROOT, "css", "fonts.css")
with open(css_output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(local_css_lines))

print(f"Successfully generated {css_output_path} with {len(local_css_lines)} local @font-face rules!")
