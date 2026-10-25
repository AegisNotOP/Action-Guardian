txt = open('web/index.html', encoding='utf-8').read()
chk = [
    # Feature 3: Workflow bar
    ('wfbar present',           'id="wfbar"' in txt),
    ('wf0..wf5 steps',          all('id="wf'+str(i)+'"' in txt for i in range(6))),
    ('wf-step CSS',             '.wf-step{' in txt),
    ('wf-step.done CSS',        '.wf-step.done' in txt),
    ('wf-step.stale CSS',       '.wf-step.stale' in txt),
    ('wf-step.current CSS',     '.wf-step.current' in txt),
    ('renderWfBar function',    'function renderWfBar' in txt),
    ('wfScanned var',           'wfScanned=false' in txt),
    ('markFieldsDirty fn',      'function markFieldsDirty' in txt),
    ('input listener on es',    "addEventListener('input'" in txt),
    ('wfbar reset in useCase',  'wfScanned=false;wfScanDirty=false' in txt),
    # Feature 2: Score history
    ('score-hist present',      'id="score-hist"' in txt),
    ('sh-row present',          'id="sh-row"' in txt),
    ('updateScoreHistory fn',   'function updateScoreHistory' in txt),
    ('shOrigSim var',           'shOrigSim=null' in txt),
    ('Original scan label',     'Original scan' in txt),
    ('Preview est. label',      'Preview est.' in txt),
    ('shPillHTML fn',           'function shPillHTML' in txt),
    ('sh-delta.better CSS',     '.sh-delta.better' in txt),
    ('rscore-lbl id',           'id="rscore-lbl"' in txt),
    ('Preview Estimate label',  'Preview Estimate' in txt),
    ('Rescan Result label',     'Rescan Result' in txt),
    ('isRescan tracking',       'isRescan=wfScanned' in txt),
    # Feature 1: Annotated preview
    ('annot-wrap present',      'id="annot-wrap"' in txt),
    ('annot-body present',      'id="annot-body"' in txt),
    ('annot-legend present',    'id="annot-legend"' in txt),
    ('extractPhrase fn',        'function extractPhrase' in txt),
    ('buildAnnotatedPreview fn','function buildAnnotatedPreview' in txt),
    ('focusAnnotMark fn',       'function focusAnnotMark' in txt),
    ('clearAnnotPreview fn',    'function clearAnnotPreview' in txt),
    ('esc fn',                  'function esc(' in txt),
    ('hi-cr CSS',               '.hi-cr{' in txt),
    ('hi-hi CSS',               '.hi-hi{' in txt),
    ('hi-md CSS',               '.hi-md{' in txt),
    ('annot-hd CSS',            '.annot-hd{' in txt),
    ('annot-legend CSS',        '.annot-legend{' in txt),
    ('click handler for focus', 'focusAnnotMark(idx)' in txt),
    ('threat card clickable',   "it.style.cursor='pointer'" in txt),
    # No unintended side effects
    ('doScan still present',    'async function doScan' in txt),
    ('doSend still present',    'async function doSend' in txt),
    ('doRewrite still present', 'async function doRewrite' in txt),
    ('doRestore intact',        'function doRestore' in txt),
    ('sendButton untouched',    'id="sendb"' in txt),
    ('useCase intact',          'function useCase' in txt),
    ('closing html tag',        txt.strip().endswith('</html>')),
]
failures = []
for name, ok in chk:
    print(('OK  ' if ok else 'FAIL'), name)
    if not ok:
        failures.append(name)
print()
print('Failures:', failures if failures else 'None')
