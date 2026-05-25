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

# Rimossi import per grafici e reti

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

# Parole religiose da escludere dai tag per mantenere lo stile "Matrix neutro"
RELIGIOUS_STOPWORDS = {"dio", "gesù", "cristo", "spirito", "santo", "chiesa", "bibbia", "signore", 
                       "angelo", "angeli", "demonio", "satana", "peccato", "salvezza", "grazia", 
                       "religione", "religioso", "fede", "credere", "preghiera", "pregare"}

# Colori Cyber Minimal
MATRIX_BG = "#1A1A1A"
MATRIX_GREENS = ["#6AF089", "#5CE07A", "#4CD06A", "#78F596"]

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

# Funzioni SVG, Timeline, e Grafici rimosse per tema Cyber Minimal.

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
    
    # Mappe, timeline e analytics rimossi per tema Cyber Minimal.
    
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
    # Inserisci riassunto dopo l'H1
    if h1_match:
        content = content.replace(h1_match.group(0), h1_match.group(0) + "\n" + summary_block, 1)

    # Costruisci il footer Matrix
    footer = "\n\n<!-- MATRIX_FOOTER_START -->\n<hr>\n"
    footer += '## COLLEGAMENTI UTILI\n<div class="matrix-links">\n'
    for link in links:
        footer += f"- [{link.upper().replace('_', ' ')}](../{link}/)\n"
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
