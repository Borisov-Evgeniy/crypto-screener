import os

exclude = {'.git', '.gitignore', '__pycache__', '.venv', 'env'}

def print_tree(path, prefix=""):
    items = sorted(os.listdir(path))
    for i, name in enumerate(items):
        if name in exclude:
            continue
        full_path = os.path.join(path, name)
        connector = "└── " if i == len(items) - 1 else "├── "
        print(prefix + connector + name)
        if os.path.isdir(full_path):
            extension = "    " if i == len(items) - 1 else "│   "
            print_tree(full_path, prefix + extension)

if __name__ == "__main__":
    print_tree(".")
