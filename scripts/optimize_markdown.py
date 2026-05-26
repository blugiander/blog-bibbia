#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
optimize_markdown.py — Phase 1: SEO optimization for all Markdown files.
Adds/updates YAML frontmatter with title, description, and keywords.
"""
import os
import glob
import re


def extract_description(content: str) -> str:
    """Extracts a short snippet for meta description (~160 chars of actual text)."""
    # Remove YAML frontmatter
    text = re.sub(r'^---.*?---', '', content, flags=re.DOTALL)
    # Remove ATX headers
    text = re.sub(r'^#+\s+.*$', '', text, flags=re.MULTILINE)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove markdown links
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    # Remove images
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove bold/italic markers
    text = re.sub(r'[*_]{1,3}', '', text)
    # Remove backticks
    text = re.sub(r'`+[^`]*`+', '', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    if not text:
        return "Un viaggio nei codici e nelle strutture nascoste della Scrittura."
    desc = text[:155]
    if len(text) > 155:
        last_space = desc.rfind(' ')
        if last_space > 100:
            desc = desc[:last_space] + "..."
        else:
            desc = desc + "..."
    return desc


def parse_frontmatter(content: str):
    """
    Parses YAML frontmatter from content.
    Returns (frontmatter_dict, body) where frontmatter_dict is a simple key→value map.
    Handles both LF and CRLF.
    """
    content_lf = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Check for frontmatter
    if not content_lf.startswith('---\n'):
        return {}, content_lf
    
    end = content_lf.find('\n---\n', 3)
    if end == -1:
        return {}, content_lf
    
    fm_text = content_lf[4:end]
    body = content_lf[end + 5:]  # skip '\n---\n'
    
    # Parse simple key: "value" pairs
    fm_dict = {}
    for line in fm_text.split('\n'):
        m = re.match(r'^(\w[\w_]*):\s*(.*)', line)
        if m:
            key = m.group(1)
            val = m.group(2).strip()
            # Remove surrounding quotes
            if (val.startswith('"') and val.endswith('"')) or \
               (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            fm_dict[key] = val
    
    return fm_dict, body


def process_file(filepath: str) -> None:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Normalize line endings to LF
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Parse existing frontmatter
    fm_dict, body = parse_frontmatter(content)
    
    # Extract title: always prefer H1 from body (more reliable than potentially truncated frontmatter)
    title = ''
    h1_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    if h1_match:
        title = h1_match.group(1).strip()
    
    if not title:
        # Fallback to frontmatter title (may be truncated)
        title = fm_dict.get('title', '')
    
    if not title:
        title = os.path.basename(filepath).replace('.md', '').replace('_', ' ').capitalize()

    
    # Ensure H1 exists in body
    if not re.search(r'^#\s+', body, re.MULTILINE):
        if re.search(r'^##\s+', body, re.MULTILINE):
            body = re.sub(r'^##\s+', '# ', body, count=1, flags=re.MULTILINE)
        else:
            body = f"# {title}\n\n" + body
    
    # Clean spacing (max 2 consecutive newlines)
    body = re.sub(r'\n{3,}', '\n\n', body)
    
    # Generate SEO metadata
    desc = extract_description(body)
    # Use first meaningful word for keywords (skip emoji/punctuation)
    words = [w for w in title.split() if re.match(r'[a-zA-ZàèéìòùÀÈÉÌÒÙ]', w)]
    first_word = re.sub(r'[^a-zA-ZàèéìòùÀÈÉÌÒÙ]', '', words[0]).lower() if words else 'bibbia'
    keywords = f"Matrix, codici, {first_word}, analisi, teologia, bibbia, scrittura"
    
    # Escape quotes in values for YAML
    title_escaped = title.replace('"', '\\"')
    desc_escaped = desc.replace('"', '\\"')
    keywords_escaped = keywords.replace('"', '\\"')
    
    # Build new frontmatter
    new_fm = (
        f'---\n'
        f'title: "{title_escaped}"\n'
        f'description: "{desc_escaped}"\n'
        f'keywords: "{keywords_escaped}"\n'
        f'---\n'
    )
    
    new_content = new_fm + body.lstrip('\n')
    
    # Write only if changed
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)
        print(f"[Ottimizzato] {filepath}")
    else:
        print(f"[OK] {filepath}")


def main():
    docs_pattern = os.path.join('docs', '**', '*.md')
    files = sorted(glob.glob(docs_pattern, recursive=True))
    for filepath in files:
        try:
            process_file(filepath)
        except Exception as e:
            print(f"[ERRORE] {filepath}: {e}")


if __name__ == "__main__":
    print("Avvio Auto-Ottimizzazione Matrix...")
    main()
    print("Ottimizzazione completata.")
