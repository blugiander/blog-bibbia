#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_matrix_assets.py — Phase 2: Generazione asset SVG per il blog Matrix.

Questo script viene chiamato dalla GitHub Actions pipeline (deploy.yml).
Genera asset SVG minimi e garantisce che le cartelle necessarie esistano.
"""

import os
import glob
import re

DOCS_DIR = "docs"
ASSETS_DIR = os.path.join(DOCS_DIR, "assets")

# Colori del tema Cyber Minimal
MATRIX_BG = "#1A1A1A"
MATRIX_GREEN = "#6AF089"
MATRIX_DARK = "#161616"
MATRIX_BORDER = "#2A2A2A"


def ensure_dirs():
    """Garantisce che le cartelle necessarie esistano."""
    for d in [ASSETS_DIR, os.path.join(DOCS_DIR, "css"), os.path.join(DOCS_DIR, "js")]:
        os.makedirs(d, exist_ok=True)


def generate_favicon():
    """Genera un favicon SVG con il logo Matrix."""
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <rect width="32" height="32" fill="{MATRIX_BG}" rx="4"/>
  <text x="16" y="22" 
        font-family="'Fira Code', monospace" 
        font-size="18" 
        font-weight="700"
        fill="{MATRIX_GREEN}" 
        text-anchor="middle">S</text>
</svg>'''
    path = os.path.join(ASSETS_DIR, "favicon.svg")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[GENERATO] {path}")
    else:
        print(f"[OK] {path} (già esistente)")


def generate_logo():
    """Genera il logo SVG del sito."""
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 40" width="200" height="40">
  <rect width="200" height="40" fill="transparent"/>
  <text x="10" y="26" 
        font-family="'Fira Code', monospace" 
        font-size="14" 
        font-weight="300"
        fill="{MATRIX_GREEN}">I Segreti della Scrittura</text>
</svg>'''
    path = os.path.join(ASSETS_DIR, "logo.svg")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[GENERATO] {path}")
    else:
        print(f"[OK] {path} (già esistente)")


def generate_og_image():
    """Genera un'immagine Open Graph SVG per i social media."""
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <rect width="1200" height="630" fill="{MATRIX_BG}"/>
  <!-- Border -->
  <rect x="20" y="20" width="1160" height="590" fill="none" stroke="{MATRIX_BORDER}" stroke-width="1"/>
  <!-- Title -->
  <text x="600" y="260" 
        font-family="'Fira Code', monospace" 
        font-size="52" 
        font-weight="300"
        fill="{MATRIX_GREEN}" 
        text-anchor="middle">I Segreti della Scrittura</text>
  <!-- Subtitle -->
  <text x="600" y="330" 
        font-family="'Fira Code', monospace" 
        font-size="24" 
        font-weight="300"
        fill="#888888" 
        text-anchor="middle">Laboratorio di Analisi Multidisciplinare</text>
  <!-- URL -->
  <text x="600" y="560" 
        font-family="'Fira Code', monospace" 
        font-size="16" 
        fill="#444444" 
        text-anchor="middle">blugiander.github.io/blog-bibbia</text>
</svg>'''
    path = os.path.join(ASSETS_DIR, "og-image.svg")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[GENERATO] {path}")
    else:
        print(f"[OK] {path} (già esistente)")


def collect_stats():
    """Raccoglie statistiche sui file del blog."""
    md_files = glob.glob(os.path.join(DOCS_DIR, "**", "*.md"), recursive=True)
    total_words = 0
    for fp in md_files:
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
        # Rimuovi frontmatter
        content = re.sub(r"^---.*?---", "", content, flags=re.DOTALL)
        words = len(content.split())
        total_words += words
    return len(md_files), total_words


def main():
    print("=" * 50)
    print(" MATRIX ASSETS GENERATION — Phase 2")
    print("=" * 50)

    ensure_dirs()
    generate_favicon()
    generate_logo()
    generate_og_image()

    num_files, total_words = collect_stats()
    print(f"\n[STATS] {num_files} pagine | ~{total_words:,} parole totali")
    print("\n[COMPLETATO] Tutti gli asset sono stati generati.")


if __name__ == "__main__":
    main()
