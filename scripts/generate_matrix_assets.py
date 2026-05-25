import os
import glob
import hashlib
import random
import re

def random_matrix_svg(seed_text, width, height):
    random.seed(seed_text)
    
    bg = "#1A1A1A"
    accent = "#6AF089"
    border = "#2A2A2A"
    
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">\n'
    svg += f'  <rect width="100%" height="100%" fill="{bg}"/>\n'
    
    # Griglia sottile minimale
    for i in range(1, 10):
        svg += f'  <line x1="0" y1="{i * height/10}" x2="{width}" y2="{i * height/10}" stroke="{border}" stroke-width="1" opacity="0.3"/>\n'
        svg += f'  <line x1="{i * width/10}" y1="0" x2="{i * width/10}" y2="{height}" stroke="{border}" stroke-width="1" opacity="0.3"/>\n'

    # Linee geometriche eleganti
    for _ in range(random.randint(3, 7)):
        y = random.randint(10, height-10)
        svg += f'  <line x1="0" y1="{y}" x2="{random.randint(50, width)}" y2="{y}" stroke="{accent}" stroke-width="1" opacity="0.5"/>\n'

    # Piccoli nodi o intersezioni
    for _ in range(random.randint(5, 12)):
        x = random.randint(10, width-10)
        y = random.randint(10, height-10)
        svg += f'  <circle cx="{x}" cy="{y}" r="2" fill="{accent}" opacity="0.7"/>\n'

    # Titolo elegante
    hash_short = hashlib.md5(seed_text.encode()).hexdigest()[:8]
    svg += f'  <text x="50%" y="50%" fill="#E0E0E0" font-family="monospace" font-size="28" font-weight="300" letter-spacing="4" text-anchor="middle" alignment-baseline="middle">ID::{hash_short.upper()}</text>\n'
    
    svg += '</svg>'
    return svg

def random_icon_svg(seed_text):
    random.seed(seed_text)
    bg = "#161616"
    accent = "#6AF089"
    
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">\n'
    svg += f'  <rect width="100" height="100" fill="{bg}" rx="8"/>\n'
    
    # Geometria minimale singola
    shape_type = random.choice(['rect', 'circle', 'line'])
    if shape_type == 'rect':
        svg += f'  <rect x="30" y="30" width="40" height="40" stroke="{accent}" fill="none" stroke-width="2"/>\n'
    elif shape_type == 'circle':
        svg += f'  <circle cx="50" cy="50" r="20" stroke="{accent}" fill="none" stroke-width="2"/>\n'
    else:
        svg += f'  <line x1="20" y1="50" x2="80" y2="50" stroke="{accent}" stroke-width="2"/>\n'
        svg += f'  <line x1="50" y1="20" x2="50" y2="80" stroke="{accent}" stroke-width="2"/>\n'
        
    svg += '</svg>'
    return svg

def process_file(filepath):
    filename = os.path.basename(filepath)
    basename = filename.replace('.md', '')
    
    assets_dir = os.path.join('docs', 'assets', 'images')
    os.makedirs(assets_dir, exist_ok=True)
    
    header_path = os.path.join(assets_dir, f'header_{basename}.svg')
    icon_path = os.path.join(assets_dir, f'icon_{basename}.svg')
    
    # Generate SVG
    header_svg = random_matrix_svg(basename, 800, 300)
    icon_svg = random_icon_svg(basename)
    
    with open(header_path, 'w', encoding='utf-8') as f:
        f.write(header_svg)
    with open(icon_path, 'w', encoding='utf-8') as f:
        f.write(icon_svg)
        
    # Read Markdown
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject Header Image after H1 if not already present
    if f"![Header {basename}]" not in content:
        # Regex to find H1
        h1_regex = r'^(# .+)$'
        match = re.search(h1_regex, content, re.MULTILINE)
        if match:
            h1 = match.group(1)
            img_tag = f"\n\n![Header {basename}](/blog-bibbia/assets/images/header_{basename}.svg)\n\n"
            new_content = content.replace(h1, h1 + img_tag, 1)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[SVG Inject] {filepath}")

def main():
    docs_pattern = os.path.join('docs', '**', '*.md')
    files = glob.glob(docs_pattern, recursive=True)
    for file in files:
        if not file.endswith('index.md'): # Skip index to not mess up homepage matrix
            process_file(file)

if __name__ == "__main__":
    print("Avvio Generazione SVG Matrix...")
    main()
    print("Generazione completata.")
