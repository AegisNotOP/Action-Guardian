import difflib

with open("web/index.html", "r", encoding="utf-8") as f:
    current = f.readlines()

extracted_path = "scratch/extracted_ui_zip/Cognition 2026 VITMAS/web/index.html"
with open(extracted_path, "r", encoding="utf-8") as f:
    attached = f.readlines()

print(f"Current lines: {len(current)}, Attached lines: {len(attached)}")

# Find differences
diff = list(difflib.unified_diff(current, attached, fromfile="current", tofile="attached", n=2))
print("Diff lines count:", len(diff))

# Let's write the diff to a scratch file so we can read it easily
with open("scratch/ui_diff.txt", "w", encoding="utf-8") as f:
    f.writelines(diff[:500])

print("Wrote first 500 diff lines to scratch/ui_diff.txt")
