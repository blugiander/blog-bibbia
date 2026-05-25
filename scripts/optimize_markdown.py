import os
import glob
import re
import string

def extract_description(content):
    """Extracts a short snippet for meta description (first ~160 chars of actual text)."""
    # Remove YAML frontmatter if present (simplified check)
    text = re.sub(r'^---.*?---', '', content, flags=re.DOTALL)
    # Remove ATX headers
    text = re.sub(r'^#+ .*$', '', text, flags=re.MULTILINE)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove markdown links
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    # Remove images
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove bold/italic markers
    text = re.sub(r'[*_]{1,2}', '', text)
    
    # Normalize whitespace
    text = ' '.join(text.split())
    if not text:
        return "Un viaggio nei codici e nelle strutture nascoste."
        
    desc = text[:155]
    if len(text) > 155:
        desc = desc[:desc.rfind(' ')] + "..."
    return desc

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Parse Frontmatter
    frontmatter = ""
    body = content
    title = os.path.basename(filepath).replace('.md', '').capitalize()
    
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        frontmatter_text = match.group(1)
        body = match.group(2)
        # Extract title from frontmatter
        title_match = re.search(r'^title:\s*[\'"]?([^\'"\n]+)[\'"]?', frontmatter_text, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
    else:
        # If no frontmatter, maybe there's a title in an H1
        h1_match = re.search(r'^# (.+)$', body, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1).strip()

    # 2. Check and Fix H1
    if not re.search(r'^# ', body, re.MULTILINE):
        # Promote first H2 to H1, or add H1 if no H2
        if re.search(r'^## ', body, re.MULTILINE):
            body = re.sub(r'^## ', '# ', body, count=1, flags=re.MULTILINE)
        else:
            body = f"# {title}\n\n" + body

    # 3. Clean Spacing (max 2 consecutive newlines)
    body = re.sub(r'\n{3,}', '\n\n', body)
    
    # 4. Generate SEO Metadata
    desc = extract_description(body)
    keywords = f"Matrix, codici, {title.split()[0].lower()}, analisi, teologia, geometria"

    # Reconstruct Frontmatter
    # Preserve existing title if it exists, otherwise add it
    new_frontmatter = f"---\ntitle: \"{title}\"\ndescription: \"{desc}\"\nkeywords: \"{keywords}\"\n---\n"
    
    new_content = new_frontmatter + body.lstrip()
    
    # Only write if changed
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[Ottimizzato] {filepath}")
    else:
        print(f"[OK] {filepath}")

def main():
    docs_pattern = os.path.join('docs', '**', '*.md')
    files = glob.glob(docs_pattern, recursive=True)
    for file in files:
        process_file(file)

if __name__ == "__main__":
    print("Avvio Auto-Ottimizzazione Matrix...")
    main()
    print("Ottimizzazione completata.")
