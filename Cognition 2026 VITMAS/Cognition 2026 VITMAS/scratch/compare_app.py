import difflib

with open("app.py", "r", encoding="utf-8") as f:
    cur_app = f.readlines()

with open("scratch/extracted_ui_zip/Cognition 2026 VITMAS/app.py", "r", encoding="utf-8") as f:
    att_app = f.readlines()

print(f"Current app.py: {len(cur_app)} lines, Attached app.py: {len(att_app)} lines")
diff = list(difflib.unified_diff(cur_app, att_app, fromfile="current", tofile="attached", n=1))
print("Diff lines count:", len(diff))
if len(diff) > 0:
    print("Sample diff:\n", "".join(diff[:40]))
