import re

def clean_previous_headers_and_signoffs(text: str) -> str:
    cleaned = text.strip()
    
    # Strip stacked greetings and headers
    header_patterns = [
        r'^(?:(?:\s*(?:Dear\s+[^\n,]+|Executive\s+Directive|Formal\s+Action\s+Memo|Formal\s+Performance\s+Directive|Notice\s+of\s+Administrative\s+Action|Final\s+Executive\s+Notice|Student|Sameer|Team|Security\s+Notice\s+to\s+Staff),?\s*\n+)+)',
    ]
    for p in header_patterns:
        cleaned = re.sub(p, '', cleaned, flags=re.IGNORECASE).strip()

    # Strip stacked signoffs
    signoff_patterns = [
        r'(?:\n+\s*(?:Best\s+regards|Warm\s+regards|Regards|Sincerely|Management|Executive\s+Leadership|Executive\s+Office|Corporate\s+Operations|Department\s+Leadership|Faculty\s+Administration|Talent\s+Acquisition|People\s+Operations|Human\s+Resources|Security\s+Operations|IT\s+Systems\s+Administration|Accounts\s+Receivable|Finance\s+&\s+Accounts\s+Department|Customer\s+Operations\s+Lead|Customer\s+Support)[^\n]*)+$'
    ]
    for p in signoff_patterns:
        cleaned = re.sub(p, '', cleaned, flags=re.IGNORECASE).strip()

    # Strip stacked standard directives
    cleaned = re.sub(r'(?:\n+\s*(?:Please\s+ensure\s+alignment|Immediate\s+execution\s+is\s+expected|Compliance\s+with\s+this\s+directive|Please\s+note:\s+This\s+instruction|Handover\s+materials\s+and\s+documentation)[^\n]*)+', '', cleaned, flags=re.IGNORECASE).strip()
    
    # Strip bullets
    lines = []
    for line in cleaned.split('\n'):
        l = line.strip()
        if l.startswith('•') or l.startswith('-') or l.startswith('*'):
            l = l.lstrip('•-* ').strip()
        lines.append(l)
    return "\n".join(lines).strip()

def rewrite_pass(text: str, iteration: int = 1) -> str:
    cleaned = clean_previous_headers_and_signoffs(text)
    if iteration == 1:
        return f"Dear Team,\n\n{cleaned}\n\nBest regards,\nCorporate Operations"
    elif iteration == 2:
        return f"Executive Directive,\n\n{cleaned}\n\nImmediate execution is expected.\n\nManagement"
    elif iteration == 3:
        lines = [l for l in cleaned.split('\n') if l.strip()]
        bulleted = "\n".join([f"• {l}" for l in lines])
        return f"Formal Action Memo,\n\n{bulleted}\n\nDepartment Leadership"
    else:
        return f"Final Executive Notice,\n\n{cleaned}\n\nExecutive Office"

cur = "We need to finalize the Q3 project deliverables by tomorrow."
for i in range(1, 6):
    cur = rewrite_pass(cur, iteration=i)
    print(f"\n--- PASS #{i} ---")
    print(cur)
    assert cur.count("Dear Team") <= 1
    assert cur.count("Executive Directive") <= 1
    assert cur.count("Formal Action Memo") <= 1
    assert cur.count("Final Executive Notice") <= 1

print("\nSUCCESS! Perfectly clean across 5 passes!")
