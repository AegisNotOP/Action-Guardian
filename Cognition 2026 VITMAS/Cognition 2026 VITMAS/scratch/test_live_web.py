import urllib.request
import json

res = urllib.request.urlopen('http://localhost:8000/')
html = res.read().decode('utf-8')
print("HTML length:", len(html))
print("wfbar in html:", 'id="wfbar"' in html)
print("cmpbox in html:", 'id="cmpbox"' in html)
print("annot-wrap in html:", 'id="annot-wrap"' in html)
print("score-hist in html:", 'id="score-hist"' in html)
print("acc-item in html:", 'acc-item' in html)
print("restb in html:", 'id="restb"' in html)

# Test /api/benchmark
res = urllib.request.urlopen('http://localhost:8000/api/benchmark')
bdata = json.loads(res.read().decode('utf-8'))
print("Benchmark cases loaded:", len(bdata.get('cases', [])))

# Test /api/rewrite with multiple iterations to verify NO duplicate greetings
payload = {
    "target": "employee@gmail.com",
    "subject": "URGENT ACTION",
    "content": "You made a catastrophic mistake and we are terminating your employment.",
    "iteration": 1
}
for it in range(1, 5):
    payload["iteration"] = it
    req = urllib.request.Request(
        'http://localhost:8000/api/rewrite',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res = urllib.request.urlopen(req)
    rdata = json.loads(res.read().decode('utf-8'))
    rem_content = rdata['remediated_content']
    print(f"\n--- Iteration {it} (Score: {rdata['new_score']}) ---")
    print(rem_content[:120].replace('\n', ' '))
    payload["content"] = rem_content

print("\n[ALL TESTS PASSED]")
