txt = open('web/index.html', encoding='utf-8').read()

start = txt.index('async function doRewrite()')
end = txt.index('\nasync function doSend()')
fn = txt[start:end]

def pos(s): return fn.index(s) if s in fn else 999999

chk = [
    ('snapSub before btn.disabled',
        pos("var snapSub=") < pos('btn.disabled=true')),
    ('snapBody before btn.disabled',
        pos("var snapBody=") < pos('btn.disabled=true')),
    ('snapSim before btn.disabled',
        pos('var snapSim=prevSim') < pos('btn.disabled=true')),
    ('snapSub before await fetch',
        pos("var snapSub=") < pos('await fetch')),
    ('snapBody before await fetch',
        pos("var snapBody=") < pos('await fetch')),
    ('no stale sub= var before fetch',
        'var sub=' not in fn),
    ('no stale body= var before fetch',
        'var body=' not in fn),
    ('API payload uses snapSub.trim()',
        'snapSub.trim()' in fn),
    ('API payload uses snapBody.trim()',
        'snapBody.trim()' in fn),
    # eb written (rewritten content) before newBody is read
    ('eb written to before var newBody=',
        pos("getElementById('eb').value=d.remediated_content") < pos('var newBody=')),
    # es written (remediated_subject) before newSub is read
    ('es written before var newSub=',
        pos('d.remediated_subject') < pos('var newSub=')),
    ('newSub read after remediated_content',
        pos('var newSub=') > pos("getElementById('eb').value=d.remediated_content")),
    ('newBody read after remediated_content',
        pos('var newBody=') > pos("getElementById('eb').value=d.remediated_content")),
    ('renderComparison snapSim first',
        'renderComparison(snapSim,snapSub,snapBody,newSim,newSub,newBody' in fn),
    ('origSub = snapSub not newSub',
        'origSub=snapSub' in fn and 'origSub=newSub' not in fn),
    ('origBody = snapBody not newBody',
        'origBody=snapBody' in fn and 'origBody=newBody' not in fn),
    ('d.remediated_content applied to eb',      "getElementById('eb').value=d.remediated_content" in fn),
    ('d.remediated_subject applied to es',       'd.remediated_subject' in fn),
    ('renderSim called for clean_preview',       'renderSim(d.clean_preview)' in fn),
    ('restb shown after success',                "getElementById('restb').style.display='block'" in fn),
    ('comparison changes passed',                "renderComparison(snapSim,snapSub,snapBody,newSim,newSub,newBody,d.changes||[])" in fn),
    ('renderComparison function present',        'function renderComparison' in txt),
    ('clearComparison called 2x',               txt.count('clearComparison()') >= 2),
    ('scorePillStyle function present',          'function scorePillStyle' in txt),
    ('cmpbox element present',                   'id="cmpbox"' in txt),
    ('footer fixed',                             'position:fixed' in txt),
    ('closing html tag',                         txt.strip().endswith('</html>')),
]

failures = []
for name, ok in chk:
    print(('OK  ' if ok else 'FAIL'), name)
    if not ok: failures.append(name)
print()
print('Failures:', failures if failures else 'None')
