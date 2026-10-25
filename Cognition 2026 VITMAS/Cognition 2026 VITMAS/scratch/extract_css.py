with open("scratch/extracted_ui_zip/Cognition 2026 VITMAS/web/index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
style_match = re.search(r"<style>(.*?)</style>", text, re.DOTALL)
if style_match:
    css = style_match.group(1)
    with open("scratch/extracted_styles.css", "w", encoding="utf-8") as f_out:
        f_out.write(css)
    print("Extracted CSS length:", len(css))
