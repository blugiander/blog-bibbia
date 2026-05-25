import os
import glob
import hashlib
import random
import re

def random_matrix_svg(seed_text, width, height):
    random.seed(seed_text)
    
    # Colori
    bg = "#030303"
    greens = ["#00FF41", "#008F11", "#003B00", "#33FF66"]
    
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">\n'
    svg += f'  <rect width="100%" height="100%" fill="{bg}"/>\n'
    
    # Genera geometrie casuali (glitch boxes)
    for _ in range(random.randint(10, 30)):
        x = random.randint(0, width)
        y = random.randint(0, height)
        w = random.randint(5, 50)
        h = random.randint(2, 10)
        color = random.choice(greens)
        opacity = random.uniform(0.1, 0.7)
        svg += f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" opacity="{opacity}"/>\n'
    
    # Genera linee di dati
    for _ in range(random.randint(5, 15)):
        y = random.randint(0, height)
        stroke_w = random.randint(1, 3)
        color = random.choice(greens)
        opacity = random.uniform(0.2, 0.5)
        svg += f'  <line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="{color}" stroke-width="{stroke_w}" opacity="{opacity}"/>\n'
        
    # Genera stringhe di codice
    chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$*&^%"
    for _ in range(random.randint(20, 60)):
        x = random.randint(0, width)
        y = random.randint(0, height)
        fontsize = random.randint(8, 24)
        color = random.choice(greens)
        opacity = random.uniform(0.3, 0.9)
        text = "".join(random.choices(chars, k=random.randint(1, 8)))
        svg += f'  <text x="{x}" y="{y}" fill="{color}" font-family="monospace" font-size="{fontsize}" opacity="{opacity}">{text}</text>\n'

    # Titolo o hash in centro
    hash_short = hashlib.md5(seed_text.encode()).hexdigest()[:8]
    svg += f'  <text x="50%" y="50%" fill="#00FF41" font-family="monospace" font-size="32" font-weight="bold" text-anchor="middle" alignment-baseline="middle" opacity="0.8">SYSTEM__{hash_short.upper()}</text>\n'
    
    svg += '</svg>'
    return svg

def random_icon_svg(seed_text):
    random.seed(seed_text)
    bg = "#000000"
    green = "#00FF41"
    
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">\n'
    svg += f'  <rect width="100" height="100" fill="{bg}" rx="10"/>\n'
    
    shape_type = random.choice(['rects', 'circles', 'paths'])
    if shape_type == 'rects':
        for _ in range(5):
            x = random.randint(10, 70)
            y = random.randint(10, 70)
            w = random.randint(10, 30)
            h = random.randint(10, 30)
            svg += f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" stroke="{green}" fill="none" stroke-width="3"/>\n'
    elif shape_type == 'circles':
        for _ in range(5):
            x = random.randint(30, 70)
            y = random.randint(30, 70)
            r = random.randint(10, 25)
            svg += f'  <circle cx="{x}" cy="{y}" r="{r}" stroke="{green}" fill="none" stroke-width="3"/>\n'
    else:
        d = f"M {random.randint(10,30)} {random.randint(10,30)} "
        for _ in range(4):
            d += f"L {random.randint(10,90)} {random.randint(10,90)} "
        d += "Z"
        svg += f'  <path d="{d}" stroke="{green}" fill="none" stroke-width="3"/>\n'
        
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
