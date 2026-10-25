import re

with open("scratch/extracted_ui_zip/Cognition 2026 VITMAS/web/index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Look for titles, headings, sections, buttons, modals, scripts
headers = re.findall(r"<h[1-4][^>]*>(.*?)</h[1-4]>", text, re.IGNORECASE | re.DOTALL)
print("=== Headings in attached index.html ===")
for h in headers:
    clean_h = re.sub(r"<[^>]+>", "", h).strip()
    print("-", clean_h)

# Check sections
sections = re.findall(r"<section[^>]*id=[\"']([^\"']+)[\"'][^>]*>", text, re.IGNORECASE)
print("\n=== Sections in attached index.html ===")
for s in sections:
    print("-", s)

# Check major divs with ids
div_ids = re.findall(r"<div[^>]*id=[\"']([^\"']+)[\"'][^>]*>", text, re.IGNORECASE)
print("\n=== Div IDs ===")
for d in div_ids:
    print("-", d)
