import os
import json
import re

CONTENT_DIR = 'content'
CATEGORY_MAP_FILE = 'data/category_map.json'
OUTPUT_FILE = 'data/index.json'

# Load category mapping
try:
    with open(CATEGORY_MAP_FILE, encoding='utf-8') as f:
        category_map = json.load(f)
except FileNotFoundError:
    print(f'⚠️ No category_map.json found at {CATEGORY_MAP_FILE}. Using folder names as-is.')
    category_map = {}

index = []

for root, _, files in os.walk(CONTENT_DIR):
    for file in files:
        if file.endswith('.md'):
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, '.').replace('\\', '/')

            # Extract category from first-level folder inside /content
            parts = rel_path.split('/')
            category_key = parts[1] if len(parts) > 1 else 'uncategorized'
            category = category_map.get(category_key, category_key)

            # Read file content
            with open(full_path, encoding='utf-8') as f:
                content = f.read()

            # 🔹 Extract title from first Markdown H1
            h1_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
            title = h1_match.group(1).strip() if h1_match else os.path.splitext(file)[0]

            # 🔹 Extract ingredients section (between "## Ingredienser" and next "##")
            ingredients_match = re.search(
                r'##\s*Ingredienser\s*\n+([\s\S]+?)(?:\n##|\Z)', content, re.IGNORECASE
            )
            ingredients_block = ingredients_match.group(1).strip() if ingredients_match else ''

            # 🔹 Extract individual ingredients (lines starting with "-")
            raw_ingredients = re.findall(r'^\s*-\s*(.+)', ingredients_block, re.MULTILINE)

            # 🔹 Normalize ingredients into tags
            tags = set()
            for item in raw_ingredients:
                words = re.findall(r'\b\w+\b', item.lower())
                tags.update(words)

            index.append({
                'title': title,
                'path': rel_path,
                'category': category,
                'tags': sorted(tags)
            })

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# Write JSON
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(index, f, indent=2, ensure_ascii=False)

print(f'✅ Generated {len(index)} entries in {OUTPUT_FILE}')
