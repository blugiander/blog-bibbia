import os
from PIL import Image, ImageDraw, ImageFont
import random

artifact_dir = r"C:\Users\giand\.gemini\antigravity-ide\brain\4621d51c-3aa9-4f37-83c4-8cec26648acf"
docs_dir = r"c:\Users\giand\Documents\segreti_scrittura\docs"

images_map = {
    "copertina_matrix_1779736100842.png": "copertina-matrix.jpg",
    "missione_matrix_1779736113808.png": "missione-matrix.jpg",
    "metodo_matrix_1779736128574.png": "metodo-matrix.jpg",
    "antico_testamento_1779736142515.png": "sezione-antico-testamento.jpg",
    "nuovo_testamento_1779736166138.png": "sezione-nuovo-testamento.jpg",
    "sezione_profeti_1779736178956.png": "sezione-profeti.jpg",
    "sezione_vangeli_1779736192426.png": "sezione-vangeli.jpg",
    "sezione_apocalisse_1779736205125.png": "sezione-apocalisse.jpg"
}

# 1. Convert and copy main images
for src, dst in images_map.items():
    src_path = os.path.join(artifact_dir, src)
    dst_path = os.path.join(docs_dir, dst)
    if os.path.exists(src_path):
        img = Image.open(src_path).convert("RGB")
        img.save(dst_path, "JPEG")
        print(f"Saved {dst_path}")

# 2. Generate Backgrounds
backgrounds = [
    "sfondo-home.jpg", "sfondo-missione.jpg", "sfondo-metodo.jpg", 
    "sfondo-antico.jpg", "sfondo-nuovo.jpg", "sfondo-profeti.jpg", 
    "sfondo-vangeli.jpg", "sfondo-apocalisse.jpg"
]

for bg in backgrounds:
    img = Image.new('RGB', (1920, 1080), color=(5, 10, 5))
    draw = ImageDraw.Draw(img)
    # Draw faint grid
    for x in range(0, 1920, 100):
        draw.line([(x, 0), (x, 1080)], fill=(0, 30, 0), width=1)
    for y in range(0, 1080, 100):
        draw.line([(0, y), (1920, y)], fill=(0, 30, 0), width=1)
    # Add some random code-like noise
    for _ in range(500):
        x = random.randint(0, 1920)
        y = random.randint(0, 1080)
        draw.text((x, y), str(random.randint(0, 1)), fill=(0, 50, 0))
        
    img.save(os.path.join(docs_dir, bg), "JPEG")
    print(f"Saved {bg}")

# 3. Generate Icons (512x512 PNG)
icons = [
    "genesi", "esodo", "numeri", "giudici", "rut", "samuele", "re", 
    "esdra", "giobbe", "salmi", "proverbi", "cantico", "isaia", 
    "lamentazioni", "ezechiele", "daniele", "matteo", "giovanni", "atti"
]

for icon in icons:
    img = Image.new('RGB', (512, 512), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer border
    draw.rectangle([10, 10, 502, 502], outline=(0, 255, 0), width=5)
    
    # Geometric inner pattern
    draw.line([(256, 10), (502, 256), (256, 502), (10, 256), (256, 10)], fill=(0, 150, 0), width=3)
    draw.ellipse([156, 156, 356, 356], outline=(0, 200, 0), width=2)
    
    # Simulate a matrix node
    for _ in range(10):
        cx, cy = random.randint(156, 356), random.randint(156, 356)
        draw.rectangle([cx, cy, cx+10, cy+10], fill=(0, 255, 0))
        draw.line([(256, 256), (cx, cy)], fill=(0, 100, 0), width=1)
        
    img.save(os.path.join(docs_dir, icon + ".png"), "PNG")
    print(f"Saved {icon}.png")

print("All assets generated!")
