path = 'web/build_html.py'
txt = open(path, encoding='utf-8').read()

# The problematic line contains a JS regex with \b\w inside a Python string.
# Find it by a unique substring and replace just that line.
marker = 'return map[raw]||raw.replace(/_/g,'
replacement = "  return map[raw]||raw.split('_').map(function(w){return w.charAt(0).toUpperCase()+w.slice(1).toLowerCase();}).join(' ');\n"

lines = txt.splitlines(keepends=True)
found = False
for i, line in enumerate(lines):
    if marker in line:
        lines[i] = replacement
        found = True
        break

if found:
    open(path, 'w', encoding='utf-8').write(''.join(lines))
    print('Patched OK at line', i+1)
else:
    print('NOT FOUND — marker missing')
