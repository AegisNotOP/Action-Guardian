# ActionGuardian: Simulated Consequences Before Real Email Dispatch 🛡️

> **VITMAS Cognition 2026 Hackathon Project**  
> *Category: Autonomous AI Agent Safety, Pre-Action Verification & Threat Sandboxing*

---

## 📌 1. Problem Statement & Motivation
High-stakes AI agent actions (sending customer emails, distributing credentials, or communicating with external clients) are **irreversible**. Once an email is dispatched over SMTP, **there is no undo button**.

Traditional agent systems allow language models to execute actions directly. **ActionGuardian** introduces a **Pre-Action Verification & Simulation Gateway** that intercepts outgoing emails before delivery:

```
[User / Agent Drafts Email] 
          │
          ▼
[DNS & Recipient Genuineness Check] ──► (Invalid Domain? ➔ Immediately Flagged)
          │
          ▼
[Threat Simulation Sandbox] ──────────► (Calculates Risk 0-100 & Detects Leaks)
          │
          ├── (Detected Risk? ➔ 1-Click AI Auto-Improve & Threat Scrubbing)
          │
          ▼
[Safety Commit Gate] ─────────────────► (Requires Human Confirmation)
          │
          ▼
[Real SMTP Email Dispatch] ───────────► (Dispatches to real inboxes with audit receipt)
```

---

## 🚀 2. Core Features Implemented

| Feature | Description |
| :--- | :--- |
| **Real Email Dispatch Backend** | Built using Python's native `smtplib` (`email.message.EmailMessage`). Dispatches real emails to user inboxes with TLS encryption and audit receipts. |
| **Recipient Genuineness & MX Check** | Verifies email syntax and performs live DNS domain lookups (`socket.getaddrinfo`). If a user inputs a fake or non-existent email domain (e.g. `@fake1239841.org`), it immediately warns that no mail can be delivered. |
| **Threat Simulation Engine** | Intercepts drafts and scans for: AWS Access Keys, secret tokens, database credentials, credit card numbers, Social Security Numbers, hostile HR harassment, and phishing links. |
| **✨ 1-Click AI Auto-Improve** | Automatically scrubs detected secrets (e.g. `AKIA...` ➔ `[REDACTED_AWS_ACCESS_KEY]`), neutralizes hostile wording to professional phrasing, and immediately recalculates the risk score from Red to Green. |
| **Clean Corporate UI/UX** | Professional, minimalist corporate SaaS aesthetic (neutral slate styling, clean typography, clear 2-column layout). |
| **Curated 8-Case Benchmark** | 8 high-impact scenarios (4 dangerous, 4 safe) with a 1-click **"Use This Test Case"** button to load, test, and auto-improve live in seconds. |
| **Future Scope (Roadmap)** | Features dedicated roadmap cards for Financial Payment Gateways and Docker Container Sandboxing. |

---

## 📊 3. Benchmark Evaluation Results

Running `python evaluate.py`:
```
================================================================================
 SUMMARY METRICS (8 CURATED SCENARIOS)
================================================================================
Total Test Cases Evaluated : 8
Total Risky Actions Tested : 4
Total Safe Actions Tested  : 4
True Positives (Caught)    : 4
True Negatives (Cleared)   : 4
False Positives (Alarm)    : 0
False Negatives (Missed)   : 0
--------------------------------------------------------------------------------
[+] RISK DETECTION RATE (RECALL) : 100.0%  (Target: >= 80%)
[+] SAFETY SPECIFICITY           : 100.0%
[+] PRECISION                    : 100.0%
[+] OVERALL ACCURACY             : 100.0%
[*] Total Evaluation Time        : ~0.005 seconds
================================================================================
```

---

## 💻 4. How to Run (1-Click)

### Option 1: Double-Click `run.bat` (Easiest)
In the project directory `Cognition 2026 VITMAS`:
1. Double-click **`run.bat`**.
2. A command terminal opens and your web browser automatically launches **`http://localhost:8000`**.

### Option 2: Run via Terminal
```bash
python app.py
```
Open **`http://localhost:8000`** in your browser.

---

## 🎬 5. Judge Pitch Demonstration Guide (3 Steps)

1. **Test Non-Existent Email Address**:
   * Type `test@fakedomainxyz9999.com` in the recipient box.
   * Notice the badge turn RED: *"✕ Email Does Not Exist: The email domain does not exist on DNS"*.
   * Then type a real email like your own Gmail address ➔ Badge turns GREEN: *"✓ Valid & DNS Verified"*.
2. **Test Threat Detection & 1-Click Auto-Improve**:
   * Scroll to the sample cases and click **"Use This Test Case"** on **`AWS & Database Password Leak`**.
   * Click **"Simulate & Scan for Threats"** ➔ Screen turns RED with **Score: 100/100 (CRITICAL)**.
   * Click **"✨ Auto-Improve & Rewrite with AI"** ➔ Watch the secrets get scrubbed into safe tokens and the score drop to **GREEN (0/100)**!
3. **Dispatch Email**:
   * Check the box: *"I verify the recipient email address..."*.
   * Click **"Send Real Email"** ➔ Generates a real dispatch receipt with an audit tracking ID.
