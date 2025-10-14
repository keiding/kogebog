import os

path = "content"

for root, dirs, files in os.walk(path):
    for filename in files:
        if filename.endswith(".md"):
            file_path = os.path.join(root, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if "ingredients" not in content.lower():
                os.remove(file_path)
                print(f"Removed (missing 'ingredients'): {file_path}")
                continue

            parts = content.split("---")
            if len(parts) >= 3:
                header = parts[1]
                body = "---".join(parts[2:])
                cleaned_header = []
                lines = header.splitlines()
                i = 0
                while i < len(lines):
                    line = lines[i]
                    if line.startswith("title:"):
                        cleaned_header.append(line)
                        i += 1
                    elif line.startswith("ingredients:"):
                        cleaned_header.append(line)
                        i += 1
                        # Capture indented lines following ingredients:
                        while i < len(lines) and (lines[i].startswith("  ") or lines[i].startswith("-")):
                            cleaned_header.append(lines[i])
                            i += 1
                    else:
                        i += 1

                new_content = "---\n" + "\n".join(cleaned_header) + "\n---\n" + body
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
