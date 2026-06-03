import os, sys, re

def is_similar(line1, line2):
    if line1 == line2: return True
    # If one is a link and the other is just the text, they match when stripped
    s1 = re.sub(r'[*_\[\]`]', '', line1)
    s2 = re.sub(r'[*_\[\]`]', '', line2)
    s1 = re.sub(r'\s+', ' ', s1).strip()
    s2 = re.sub(r'\s+', ' ', s2).strip()
    if len(s1) > 10 and s1 == s2:
        return True
    return False

def is_better(new_l, old_l):
    # Prefer one with code ticks
    if '`' in new_l and '`' not in old_l: return True
    if '`' in old_l and '`' not in new_l: return False
    # Prefer link over text
    if '[' in new_l and '[' not in old_l: return True
    if '[' in old_l and '[' not in new_l: return False
    return len(new_l) > len(old_l)

def process_file(path, dry_run=False):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Normalize line endings
    content = content.replace('\r\n', '\n')

    # 2. Fix backlinks (make external links to learncpp into Obsidian internal links)
    def link_replacer(m):
        text = m.group(1)
        url = m.group(2)
        if 'learncpp.com' in url:
            return f"[[{text}]]"
        return m.group(0)
    
    content = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', link_replacer, content)

    # 3. Deduplicate exact duplicate cascading lines
    lines = content.split('\n')
    lines = [line.rstrip() for line in lines]

    deduped_lines = []
    last_non_empty = None
    last_non_empty_idx = -1

    for line in lines:
        if line == '':
            deduped_lines.append(line)
        else:
            if last_non_empty is not None and is_similar(line, last_non_empty):
                # Duplicate line. Decide which to keep.
                if is_better(line, last_non_empty):
                    deduped_lines[last_non_empty_idx] = line
                    last_non_empty = line
            else:
                deduped_lines.append(line)
                last_non_empty = line
                last_non_empty_idx = len(deduped_lines) - 1

    # 4. Clean up formatting
    new_content = '\n'.join(deduped_lines)
    # Fix heading spacing (ensure single space after #)
    new_content = re.sub(r'^(#+)([^#\s])', r'\1 \2', new_content, flags=re.MULTILINE)
    # Collapse multiple blank lines into a single blank line
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)

    if new_content != content:
        if not dry_run:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        return True
    return False

def main(root):
    changed_files = 0
    for dirpath, _, filenames in os.walk(root):
        if '.git' in dirpath or '.syncthing' in dirpath:
            continue
        for fn in filenames:
            if fn.lower().endswith('.md'):
                full = os.path.join(dirpath, fn)
                try:
                    if process_file(full):
                        changed_files += 1
                        print(f"Fixed {full}")
                except Exception as e:
                    print(f"Error processing {full}: {e}", file=sys.stderr)
    print(f"Changed {changed_files} files.")

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
