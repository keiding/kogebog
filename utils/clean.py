import os

path = "content"

for root, dirs, files in os.walk(path):
    for filename in files:
        if filename.startswith('.') or filename.startswith('_'):
            file_path = os.path.join(root, filename)
            os.remove(file_path)
            print(f"Removed: {file_path}")
