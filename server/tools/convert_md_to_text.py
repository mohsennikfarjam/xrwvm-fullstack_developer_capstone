import os
import re
import html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT_DIR = os.path.join(ROOT, 'submission_artifacts', 'plain_text')

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def md_to_text(content):
    # Remove code fences
    content = re.sub(r'```[\s\S]*?```', '', content)
    # Replace images with alt text removed
    content = re.sub(r'!\[([^\]]*)\]\([^\)]*\)', r'\1', content)
    # Replace links [text](url) -> text
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
    # Remove headings, emphasis, inline code markers
    content = re.sub(r'(^|\n)#{1,6}\s*', '\n', content)
    content = re.sub(r'[*_]{1,3}', '', content)
    content = re.sub(r'`+', '', content)
    # Remove leftover HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    # Unescape HTML entities
    content = html.unescape(content)
    # Normalize whitespace
    content = re.sub(r'\r\n', '\n', content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()

def html_to_text(content):
    # Simple HTML tag stripper and unescape
    text = re.sub(r'<script[\s\S]*?</script>', '', content, flags=re.I)
    text = re.sub(r'<style[\s\S]*?</style>', '', text, flags=re.I)
    text = re.sub(r'<[^>]+>', '', text)
    return html.unescape(text).strip()

def process_file(path, rel_root):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        data = f.read()
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.md', '.markdown') or path.endswith('.md.html'):
        out = md_to_text(data)
    elif ext in ('.html', '.htm'):
        out = html_to_text(data)
    else:
        # fallback: remove tags
        out = md_to_text(data)

    out_path = os.path.join(OUT_DIR, rel_root + '.txt')
    ensure_dir(os.path.dirname(out_path))
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(out)
    print(f'Wrote: {out_path}')

def main():
    ensure_dir(OUT_DIR)
    for dirpath, dirs, files in os.walk(ROOT):
        # skip virtual envs and node_modules and submission_artifacts
        if any(part in ('node_modules', '.venv', 'venv', 'submission_artifacts') for part in dirpath.split(os.sep)):
            continue
        for fn in files:
            if fn.lower().endswith(('.md', '.markdown', '.html', '.htm')) or fn.lower().endswith('.md.html'):
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, ROOT).replace(os.sep, '/')
                rel_no_ext = os.path.splitext(rel)[0]
                process_file(full, rel_no_ext)

if __name__ == '__main__':
    main()
