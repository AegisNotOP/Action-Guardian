import json
import math

json_path = 'C:/Users/samya/.gemini/antigravity/brain/85c41e0f-b9c8-41ad-b55a-19357d8417bd/unzipped_spec/actionguardian_scoring_v2.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

cfg = data['config']

def half_up(x):
    return int(math.floor(x + 0.5))

def score_email(inp, cfg):
    content = sum(cfg['content_rules'][r] for r in set(inp['content_rules']))
    if inp.get('role_allowed'):
        content = half_up(content * cfg['role_exception_content_multiplier'])
    content = min(100, content)
    
    intent = cfg['intent_points'][inp['intent_type']]
    if inp.get('intent_drift'):
        intent += cfg['intent_drift_points']
        
    n = sum(cfg['backfire_factors'][f] for f in inp['backfire_factors'])
    band = 'low' if n <= 1 else ('medium' if n <= 3 else 'high')
    p = cfg['backfire_bands'][band]
    
    imp = cfg['impact_severity'][inp['impact_category']]
    imp *= cfg['scope_multiplier'][inp['scope']]
    imp *= cfg['irreversible_multiplier'] if inp.get('irreversible') else 1.0
    imp = half_up(min(cfg['impact_cap'], imp))
    p_x_i = half_up(p * imp)
    
    total = min(100, content + intent + p_x_i)
    if inp.get('hard_floor'):
        total = max(total, cfg['hard_floor_score'])
        
    tier = next(t['name'] for t in cfg['tiers'] if t['min'] <= total <= t['max'])
    return {
        'content': content,
        'intent': intent,
        'backfire_factor_count': n,
        'backfire_band': band,
        'backfire_p': p,
        'impact': imp,
        'p_x_impact': p_x_i,
        'total': total,
        'tier': tier
    }

print(f"{'ID':<7} | {'TITLE':<40} | {'GOT TOTAL':<9} | {'EXP TOTAL':<9} | {'GOT TIER':<8} | {'EXP TIER':<8} | STATUS")
print("-" * 105)

mismatches = []
for sc in data['scenarios']:
    res = score_email(sc['inputs'], cfg)
    exp = sc['expected']
    sc_mismatches = {}
    for k in ['content', 'intent', 'backfire_factor_count', 'backfire_band', 'impact', 'p_x_impact', 'total', 'tier']:
        if res[k] != exp[k]:
            sc_mismatches[k] = {'got': res[k], 'expected': exp[k]}
            
    status = "MATCH" if not sc_mismatches else "MISMATCH"
    if sc_mismatches:
        mismatches.append({'id': sc['id'], 'title': sc['title'], 'diff': sc_mismatches})
        
    print(f"{sc['id']:<7} | {sc['title'][:40]:<40} | {res['total']:<9} | {exp['total']:<9} | {res['tier']:<8} | {exp['tier']:<8} | {status}")

print("-" * 105)
print(f"Total Scenarios Evaluated: {len(data['scenarios'])}")
print(f"Matches: {len(data['scenarios']) - len(mismatches)}")
print(f"Mismatches: {len(mismatches)}")

if mismatches:
    print("\nDetailed Mismatch Breakdown:")
    for m in mismatches:
        print(f"  Scenario {m['id']}: {m['title']}")
        for k, v in m['diff'].items():
            print(f"    - {k}: got {v['got']}, expected {v['expected']}")
else:
    print("\nALL 21 SCENARIOS MATCH 100% WITH EXPECTED SCORES AND TIERS!")
