import os
import re

CONTENT_DIR = 'content'

def transform_markdown(file_path):
    with open(file_path, encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'^title:\s*(.+)', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else None

    # Extract ingredients block
    ingredients_match = re.search(r'^ingredients:\s*\n((?:\s*-\s*.+\n)+)', content, re.MULTILINE)
    ingredients_block = ingredients_match.group(1) if ingredients_match else ''

    # Convert ingredients to Markdown list, filtering out placeholders
    ingredients_lines = re.findall(r'-\s*(.+)', ingredients_block)
    cleaned_ingredients = [line.strip() for line in ingredients_lines if line.strip() != '--']
    formatted_ingredients = '\n'.join(f'- {line}' for line in cleaned_ingredients)

    # Remove frontmatter
    content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)

    # Remove original title and ingredients block
    content = re.sub(r'^title:.*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^ingredients:\s*\n((?:\s*-\s*.+\n)+)', '', content, flags=re.MULTILINE)

    # Assemble new content
    new_parts = []
    if title:
        new_parts.append(f'# {title}\n')
    if formatted_ingredients:
        new_parts.append('## Ingredienser\n')
        new_parts.append(f'{formatted_ingredients}\n')
        new_parts.append('## Opskrift\n')

    new_parts.append(content.strip())
    new_content = '\n\n'.join(new_parts)

    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f'✅ Updated: {file_path}')

# Walk through content directory recursively
for root, _, files in os.walk(CONTENT_DIR):
    for file in files:
        if file.endswith('.md'):
            transform_markdown(os.path.join(root, file))
