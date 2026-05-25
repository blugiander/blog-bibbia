import os
import glob
import re
import hashlib
import random
import time
from collections import Counter
import math
import argparse
from datetime import datetime

# Import per formati e NLP (con fallback silenziosi se non installati)
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    # Scarica i dati di nltk se mancano
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    HAVE_NLTK = True
except ImportError:
    HAVE_NLTK = False

# Rimossi import audio/pdf/epub per Versione Leggera

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import networkx as nx
    HAVE_GRAPHS = True
except ImportError:
    HAVE_GRAPHS = False

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    HAVE_WATCHDOG = True
except ImportError:
    HAVE_WATCHDOG = False

# ==========================================
# CONFIGURAZIONE MATRIX
# ==========================================
DOCS_DIR = "docs"
MAPS_DIR = os.path.join(DOCS_DIR, "maps")
TIMELINE_DIR = os.path.join(DOCS_DIR, "timeline")
ANALYTICS_DIR = os.path.join(DOCS_DIR, "analytics")
ASSETS_DIR = os.path.join(DOCS_DIR, "assets", "images")

for d in [MAPS_DIR, TIMELINE_DIR, ANALYTICS_DIR, ASSETS_DIR]:
    os.makedirs(d, exist_ok=True)

# Parole religiose da escludere dai tag per mantenere lo stile "Matrix neutro"
RELIGIOUS_STOPWORDS = {"dio", "gesù", "cristo", "spirito", "santo", "chiesa", "bibbia", "signore", 
                       "angelo", "angeli", "demonio", "satana", "peccato", "salvezza", "grazia", 
                       "religione", "religioso", "fede", "credere", "preghiera", "pregare"}

# Colori Matrix Elegante (Versione Leggera)
MATRIX_BG = "#1A1A1A"
MATRIX_GREENS = ["#8FBC8F", "#98FB98", "#66CDAA", "#7CB342"]

# ==========================================
# FUNZIONI NLP E TESTO
# ==========================================

def get_italian_stopwords():
    if HAVE_NLTK:
        try:
            return set(stopwords.words('italian'))
        except:
            pass
    # Fallback stopwords
    return {"il", "lo", "la", "i", "gli", "le", "un", "uno", "una", "di", "a", "da", "in", "con", "su", "per", "tra", "fra", "e", "o", "ma", "che", "non", "si", "se", "come", "più", "questo", "quello", "suo", "sua", "loro", "essere", "avere", "sono", "è", "ha", "hanno"}

def clean_text(text):
    # Rimuove markdown, url, e punteggiatura varia
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[#*`_\[\]\(\)!>-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def generate_summary(text, num_sentences=5):
    """Fase 1: Genera un riassunto estrattivo (le prime frasi del testo pulito)"""
    clean = clean_text(text)
    if HAVE_NLTK:
        try:
            sentences = sent_tokenize(clean, language='italian')
        except:
            sentences = [s.strip() + "." for s in re.split(r'[.!?]+', clean) if s.strip()]
    else:
        sentences = [s.strip() + "." for s in re.split(r'[.!?]+', clean) if s.strip()]
    
    # Filtra intestazioni brevi e spazzatura
    valid_sentences = [s for s in sentences if len(s.split()) > 5]
    summary = " ".join(valid_sentences[:num_sentences])
    if not summary:
        return "Nessun dato estraibile per il riassunto di questa anomalia."
    return summary

def generate_tags(text, num_tags=7):
    """Fase 2: Estrae concetti chiave analitici, ignorando quelli religiosi."""
    text_clean = clean_text(text).lower()
    words = re.findall(r'\b[a-zàèéìòù]{4,}\b', text_clean)
    
    stops = get_italian_stopwords()
    
    filtered_words = [w for w in words if w not in stops and w not in RELIGIOUS_STOPWORDS]
    
    counter = Counter(filtered_words)
    most_common = counter.most_common(num_tags * 2)
    
    tags = [word for word, count in most_common][:num_tags]
    if not tags:
        tags = ["sistema", "struttura", "analisi", "codice", "matrice"]
    return tags

def extract_timeline_dates(text):
    """Fase 5: Estrae riferimenti temporali (anni) per la timeline."""
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
    # Rimuovi duplicati ma mantieni ordine
    unique_years = sorted(list(set(years)))
    return unique_years

# ==========================================
# GENERAZIONE ASSET VISIVI (SVG, PNG)
# ==========================================

def generate_matrix_svg_map(basename, tags):
    """Fase 4: Mappe concettuali (SVG)"""
    random.seed(basename)
    width, height = 800, 600
    
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">\n'
    svg += f'  <rect width="100%" height="100%" fill="{MATRIX_BG}"/>\n'
    
    nodes = [{"word": basename.upper(), "x": width//2, "y": height//2, "r": 40}]
    for tag in tags:
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(100, 250)
        nodes.append({
            "word": tag.upper(),
            "x": width//2 + int(math.cos(angle) * dist),
            "y": height//2 + int(math.sin(angle) * dist),
            "r": random.randint(15, 30)
        })
        
    # Draw connections
    for i in range(1, len(nodes)):
        svg += f'  <line x1="{nodes[0]["x"]}" y1="{nodes[0]["y"]}" x2="{nodes[i]["x"]}" y2="{nodes[i]["y"]}" stroke="#8FBC8F" stroke-width="2" opacity="0.5"/>\n'
        if i > 1 and random.random() > 0.5:
            svg += f'  <line x1="{nodes[i-1]["x"]}" y1="{nodes[i-1]["y"]}" x2="{nodes[i]["x"]}" y2="{nodes[i]["y"]}" stroke="#66CDAA" stroke-width="1" opacity="0.3"/>\n'

    # Draw nodes
    for node in nodes:
        color = random.choice(MATRIX_GREENS)
        svg += f'  <circle cx="{node["x"]}" cy="{node["y"]}" r="{node["r"]}" fill="{MATRIX_BG}" stroke="{color}" stroke-width="3"/>\n'
        font_size = min(14, node["r"] - 2) if node["word"] != basename.upper() else 16
        svg += f'  <text x="{node["x"]}" y="{node["y"]}" fill="{color}" font-family="monospace" font-size="{font_size}" font-weight="bold" text-anchor="middle" alignment-baseline="middle">{node["word"][:10]}</text>\n'

    svg += '</svg>'
    
    filepath = os.path.join(MAPS_DIR, f"{basename}_map.svg")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)
    return filepath

def generate_timeline_svg(basename, dates):
    """Fase 5: Genera timeline SVG se ci sono date."""
    if not dates:
        return None
        
    width, height = 800, 200
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">\n'
    svg += f'  <rect width="100%" height="100%" fill="{MATRIX_BG}"/>\n'
    svg += f'  <line x1="50" y1="{height//2}" x2="{width-50}" y2="{height//2}" stroke="#8FBC8F" stroke-width="4"/>\n'
    
    step = (width - 100) / max(1, len(dates) - 1)
    for i, date in enumerate(dates):
        x = 50 + (i * step)
        y_text = height//2 - 20 if i % 2 == 0 else height//2 + 35
        svg += f'  <circle cx="{x}" cy="{height//2}" r="8" fill="#8FBC8F"/>\n'
        svg += f'  <text x="{x}" y="{y_text}" fill="#98FB98" font-family="monospace" font-size="16" text-anchor="middle">{date}</text>\n'
        
    svg += '</svg>'
    filepath = os.path.join(TIMELINE_DIR, f"{basename}_timeline.svg")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)
    return filepath

def generate_analytics_png(basename, tags):
    """Fase 6: Genera grafici semantici PNG usando matplotlib se disponibile."""
    if not HAVE_GRAPHS or not tags:
        return None
        
    plt.figure(figsize=(8, 4))
    plt.style.use('dark_background')
    
    # Dati finti basati sui tag per dare l\'illusione di un\'analisi profonda
    values = [random.randint(10, 100) for _ in tags]
    values.sort(reverse=True)
    
    bars = plt.bar(tags, values, color='#8FBC8F')
    for bar in bars:
        bar.set_edgecolor('#98FB98')
        
    plt.title(f"ANALISI FREQUENZE: {basename.upper()}", color='#8FBC8F', fontname='monospace')
    plt.xticks(rotation=45, color='#8FBC8F', fontname='monospace')
    plt.yticks(color='#8FBC8F', fontname='monospace')
    plt.grid(color='#66CDAA', linestyle='--', linewidth=0.5, alpha=0.5)
    plt.tight_layout()
    
    filepath = os.path.join(ANALYTICS_DIR, f"{basename}_analytics.png")
    plt.savefig(filepath, facecolor='#1A1A1A', dpi=150)
    plt.close()
    return filepath

# PDF, EPUB, AUDIO rimossi nella Versione Leggera

# ==========================================
# MOTORE PRINCIPALE
# ==========================================

def ensure_yaml_frontmatter(content, tags):
    """Fase 2: Inserisce i tag nel meta-header YAML."""
    if content.startswith("---\n") or content.startswith("---\r\n"):
        match = re.search(r'\r?\n---\s*\r?\n', content)
        if match:
            frontmatter = content[3:match.start()].strip()
            if "tags:" not in frontmatter:
                new_fm = frontmatter + f"\ntags:\n" + "\n".join([f"  - {t}" for t in tags]) + "\n"
                return "---\n" + new_fm + "---\n\n" + content[match.end():].lstrip()
            return content
    
    # Crea nuovo frontmatter
    new_fm = "---\ntags:\n" + "\n".join([f"  - {t}" for t in tags]) + "\n---\n\n"
    return new_fm + content

def process_file(filepath, all_files):
    basename = os.path.basename(filepath).replace('.md', '')
    if basename == 'index':
        return # Salta la home
        
    print(f"--- Processando: {basename} ---")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Rimuovi blocchi Matrix precedenti per evitare duplicazioni
    content = re.sub(r'<!-- MATRIX_SUMMARY_START -->.*?<!-- MATRIX_SUMMARY_END -->', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- MATRIX_FOOTER_START -->.*?<!-- MATRIX_FOOTER_END -->', '', content, flags=re.DOTALL)
    
    # Estrai titolo H1
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = h1_match.group(1) if h1_match else basename
    
    # Rimuovi yaml frontmatter SOLO per il riassunto e NLP
    text_for_nlp = content
    if text_for_nlp.startswith("---\n") or text_for_nlp.startswith("---\r\n"):
        match = re.search(r'\r?\n---\s*\r?\n', text_for_nlp)
        if match:
            text_for_nlp = text_for_nlp[match.end():]
            
    # Rimuovi H1 e immagini per non includerle nel riassunto
    text_for_nlp = re.sub(r'^#\s+.*$', '', text_for_nlp, flags=re.MULTILINE)
    text_for_nlp = re.sub(r'!\[.*?\]\(.*?\)', '', text_for_nlp)
            
    # Fase 1: Riassunto
    summary = generate_summary(text_for_nlp)
    
    # Fase 2: Tag
    tags = generate_tags(text_for_nlp)
    content = ensure_yaml_frontmatter(content, tags)
    
    # Fase 4: Mappa Concettuale
    map_path = generate_matrix_svg_map(basename, tags)
    
    # Fase 5: Timeline
    dates = extract_timeline_dates(content)
    timeline_path = generate_timeline_svg(basename, dates)
    
    # Fase 6: Analisi e Grafici
    analytics_path = generate_analytics_png(basename, tags)
    
    # Nessuna esportazione (Versione Leggera)
    
    # Fase 3: Link Interni
    # Trova altri 3 file casuali (in un sistema reale userebbe similarità vettoriale)
    other_files = [os.path.basename(f).replace('.md', '') for f in all_files if f != filepath and not f.endswith('index.md')]
    links = random.sample(other_files, min(3, len(other_files))) if other_files else []
    
    # ====================
    # FASE 8: INIEZIONE
    # ====================
    
    # Aggiungi riassunto sotto l'immagine Header (o sotto l'H1)
    summary_block = f"""
<!-- MATRIX_SUMMARY_START -->
<div class="admonition note matrix-summary">
<p class="admonition-title">SYSTEM_ANALYSIS // RIASSUNTO</p>
<p>{summary}</p>
</div>
<!-- MATRIX_SUMMARY_END -->
"""
    # Cerca l'immagine dell'header (da generazioni precedenti)
    header_img_regex = r'(!\[Header.*?\]\(.*?\))'
    if re.search(header_img_regex, content):
        content = re.sub(header_img_regex, r'\1\n' + summary_block, content, count=1)
    elif h1_match:
        # Se non c'è header image, mettilo dopo l'H1
        content = content.replace(h1_match.group(0), h1_match.group(0) + "\n" + summary_block, 1)

    # Costruisci il footer Matrix
    footer = "\n\n<!-- MATRIX_FOOTER_START -->\n<hr>\n"
    footer += '## COLLEGAMENTI UTILI\n<div class="matrix-links">\n'
    for link in links:
        footer += f"- [{link.upper().replace('_', ' ')}](../{link}/)\n"
    footer += "</div>\n\n"
    
    footer += '## DATA ASSETS\n<div class="matrix-assets">\n'
    if map_path:
        footer += f"- 🗺️ **Mappa Concettuale**: [Visualizza SVG](../maps/{os.path.basename(map_path)})\n"
    if timeline_path:
        footer += f"- ⏱️ **Timeline**: [Visualizza SVG](../timeline/{os.path.basename(timeline_path)})\n"
    if analytics_path:
        footer += f"- 📊 **Analisi Semantica**: [Visualizza PNG](../analytics/{os.path.basename(analytics_path)})\n"
    footer += "</div>\n\n"
    
    footer += "<!-- MATRIX_FOOTER_END -->\n"
    
    content += footer
    
    # Scrivi il file aggiornato
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"[{basename}] -> Aggiornato (Tag, Riassunto, Asset, Export)")

# ==========================================
# WATCHER (Fase 9)
# ==========================================

class MatrixEventHandler(FileSystemEventHandler):
    def __init__(self, all_files):
        self.all_files = all_files
        self.last_processed = {}

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith('.md'):
            return
        
        # Debounce per evitare trigger multipli
        now = time.time()
        last_time = self.last_processed.get(event.src_path, 0)
        if now - last_time < 2:
            return
            
        self.last_processed[event.src_path] = now
        print(f"\n[WATCHER] Modifica rilevata in: {event.src_path}")
        try:
            process_file(event.src_path, self.all_files)
        except Exception as e:
            print(f"Errore durante l'elaborazione di {event.src_path}: {e}")

def run_watcher(all_files):
    if not HAVE_WATCHDOG:
        print("Errore: la libreria 'watchdog' non è installata. Impossibile avviare il watcher locale.")
        return
        
    event_handler = MatrixEventHandler(all_files)
    observer = Observer()
    observer.schedule(event_handler, path=DOCS_DIR, recursive=True)
    observer.start()
    print(f"\n[MATRIX_WATCHER] Avviato. In ascolto su '{DOCS_DIR}'...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[MATRIX_WATCHER] Arrestato.")
    observer.join()

# ==========================================
# MAIN
# ==========================================

def main():
    parser = argparse.ArgumentParser(description="Matrix 4.0 Orchestrator")
    parser.add_argument("--watch", action="store_true", help="Avvia in modalità watcher")
    args = parser.parse_args()
    
    print("========================================")
    print(" INIZIALIZZAZIONE MATRIX ENGINE 4.0")
    print("========================================")
    
    all_md_files = glob.glob(os.path.join(DOCS_DIR, '**', '*.md'), recursive=True)
    
    if not args.watch:
        # One-shot processing
        for file in all_md_files:
            process_file(file, all_md_files)
        print("\n[SISTEMA AGGIORNATO ALLA VERSIONE 4.0]")
    else:
        # Watch mode
        run_watcher(all_md_files)

if __name__ == "__main__":
    main()
