"""Fix __init__.py files that have plain text instead of valid Python."""

import os

base = r"C:\Users\thiri\multimind-ai-platform"

files_to_fix = [
    "src/multimind/agents/__init__.py",
    "src/multimind/knowledge/__init__.py",
    "src/multimind/memory/__init__.py",
    "src/multimind/security/__init__.py",
    "src/multimind/simulator/__init__.py",
    "src/multimind/health/__init__.py",
    "src/multimind/silent/__init__.py",
    "src/multimind/dashboards/__init__.py",
    "src/multimind/utils/__init__.py",
]

for fpath in files_to_fix:
    full = os.path.join(base, fpath)
    with open(full, "r", encoding="utf-8") as f:
        content = f.read()

    stripped = content.strip()

    # Check if it starts with a valid Python string (triple-quote)
    if stripped.startswith('"""') or stripped.startswith("'''"):
        print(f"OK: {fpath}")
        continue

    # Check if it's a simple docstring-style text
    if stripped and not stripped.startswith("#"):
        # Wrap in triple quotes
        new_content = '"""' + stripped + '"""\n'
        with open(full, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed: {fpath}")
    else:
        print(f"Skipped (empty/comment): {fpath}")

# Fix the data __init__.py which has unicode characters
data_init = os.path.join(base, "src/multimind/data/__init__.py")
with open(data_init, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the euro symbol and other problematic chars
content = content.replace("\u20ac", "EUR")
with open(data_init, "w", encoding="utf-8") as f:
    f.write(content)
print(f"Fixed unicode in: src/multimind/data/__init__.py")

# Also fix the data directory __init__.py (the data/ at root)
data_root = os.path.join(base, "data/__init__.py")
if os.path.exists(data_root):
    with open(data_root, "r", encoding="utf-8") as f:
        c = f.read()
    c = c.replace("\u20ac", "EUR")
    with open(data_root, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"Fixed unicode in: data/__init__.py")

print("\nDone fixing __init__.py files!")
