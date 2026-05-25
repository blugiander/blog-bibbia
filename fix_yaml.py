import os
import re

docs_dir = 'docs'
for filename in os.listdir(docs_dir):
    if not filename.endswith('.md'):
        continue
    filepath = os.path.join(docs_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def replacer(match):
        text = match.group(1)
        # Se c'è una virgoletta finale spaiata, la togliamo per pulizia
        if text.endswith('"'):
            text = text[:-1]
        if text.startswith('"'):
            text = text[1:]
        
        # Facciamo l'escape delle virgolette interne
        text = text.replace('"', '\\"')
        return f'description: "{text}"'
        
    # Cerchiamo "description: " seguito da eventuale "> "
    new_content = re.sub(r'^description:\s*">?\s*(.*)$', replacer, content, flags=re.MULTILINE)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {filename}")
