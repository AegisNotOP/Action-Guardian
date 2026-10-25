"""
Generates the 10-slide PowerPoint presentation matching the Cognition 2026 VITMAS template.
Tone: Accessible, less technical, high-impact, business & safety focused.
"""
import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck(filename="ActionGuardian_Final_Pitch_Deck.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette - Modern Corporate Safety Slate & Tech Indigo
    COLOR_BG = RGBColor(248, 250, 252)        # Slate 50
    COLOR_PRIMARY = RGBColor(15, 23, 42)      # Slate 900
    COLOR_ACCENT = RGBColor(79, 70, 229)      # Indigo 600
    COLOR_ACCENT_BG = RGBColor(238, 242, 255) # Indigo 50
    COLOR_MUTED = RGBColor(100, 116, 139)     # Slate 500
    COLOR_CARD = RGBColor(255, 255, 255)      # White
    COLOR_BORDER = RGBColor(226, 232, 240)    # Slate 200
    COLOR_RED = RGBColor(225, 29, 72)         # Rose 600
    COLOR_GREEN = RGBColor(16, 185, 129)      # Emerald 600
    COLOR_AMBER = RGBColor(217, 119, 6)       # Amber 600

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="ACTIONGUARDIAN | VITMAS COGNITION 2026"):
        # Header category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_ACCENT

        # Slide Title (Exact match to template)
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf = t_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD, border_color=COLOR_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
        return shape

    # =========================================================================
    # SLIDE 1: Title Slide (Template Page 1)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = add_card(s1, Inches(0), Inches(0), Inches(13.333), Inches(7.5), bg_color=COLOR_BG, border_color=COLOR_BG)
    
    # Hero Center Card
    add_card(s1, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1), bg_color=COLOR_CARD)
    
    # Badge
    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.7), Inches(1.6), Inches(3.933), Inches(0.45))
    b1.fill.solid()
    b1.fill.fore_color.rgb = COLOR_ACCENT_BG
    b1.line.color.rgb = COLOR_ACCENT
    p_b1 = b1.text_frame.paragraphs[0]
    p_b1.text = "VITMAS COGNITION 2026 • FINAL REVIEW 3"
    p_b1.alignment = PP_ALIGN.CENTER
    p_b1.font.size = Pt(11)
    p_b1.font.bold = True
    p_b1.font.color.rgb = COLOR_ACCENT

    # Problem Statement Title
    t1 = s1.shapes.add_textbox(Inches(2.0), Inches(2.2), Inches(9.333), Inches(1.8))
    tf1 = t1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "ActionGuardian"
    p1.alignment = PP_ALIGN.CENTER
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_PRIMARY

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Simulated Consequences Before Real Email Dispatch 🛡️"
    p1_sub.alignment = PP_ALIGN.CENTER
    p1_sub.font.size = Pt(20)
    p1_sub.font.color.rgb = COLOR_MUTED

    # Team & Members Section
    div1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.5), Inches(4.3), Inches(6.333), Inches(0.02))
    div1.fill.solid()
    div1.fill.fore_color.rgb = COLOR_BORDER
    div1.line.fill.background()

    info1 = s1.shapes.add_textbox(Inches(2.0), Inches(4.5), Inches(9.333), Inches(1.4))
    tf_info1 = info1.text_frame
    tf_info1.word_wrap = True
    
    p_team = tf_info1.paragraphs[0]
    p_team.text = "Team Name: Team ActionGuardian"
    p_team.alignment = PP_ALIGN.CENTER
    p_team.font.size = Pt(16)
    p_team.font.bold = True
    p_team.font.color.rgb = COLOR_PRIMARY

    p_track = tf_info1.add_paragraph()
    p_track.text = "Track: Autonomous Agentic AI & AI/ML Safety"
    p_track.alignment = PP_ALIGN.CENTER
    p_track.font.size = Pt(13)
    p_track.font.color.rgb = COLOR_ACCENT

    p_members = tf_info1.add_paragraph()
    p_members.text = "Members: Sahaj & Team"
    p_members.alignment = PP_ALIGN.CENTER
    p_members.font.size = Pt(13)
    p_members.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 2: Problem Statement & Objectives (Template Page 2)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement & Objectives")

    # Left: The Problem
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb2_left = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf2_l = tb2_left.text_frame
    tf2_l.word_wrap = True
    
    p = tf2_l.paragraphs[0]
    p.text = "⚠️ THE PROBLEM"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED

    points_prob = [
        ("Once an Email is Sent, There is No Undo Button:", "Language models are increasingly trusted to draft and send emails directly. But unlike text chats, real email delivery over SMTP is completely irreversible."),
        ("Catastrophic Accidental Leaks:", "Agents routinely leak passwords, AWS keys, private medical records, and salary sheets to external vendors by mistake."),
        ("Hostile Language & Reputational Firestorms:", "Under ambiguous user instructions, agents can send harsh, career-ending, or legally binding commitments with zero human review."),
        ("Fake or Mistyped Recipients:", "Dispatching sensitive messages to mistyped addresses (e.g. '@gmial.com' or nonexistent domains) causes instant exfiltration or delivery failure.")
    ]
    for title, desc in points_prob:
        p_t = tf2_l.add_paragraph()
        p_t.text = f"• {title} "
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = COLOR_PRIMARY
        p_d = tf2_l.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_MUTED

    # Right: Objectives
    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb2_right = s2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf2_r = tb2_right.text_frame
    tf2_r.word_wrap = True

    p = tf2_r.paragraphs[0]
    p.text = "🎯 OUR OBJECTIVES"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    points_obj = [
        ("1. Pre-Action Flight Simulator:", "Create an isolated safety sandbox where outgoing drafts are tested for real-world consequences before touching the internet."),
        ("2. Meaningful 3-Question Consequence Model:", "Move beyond dumb keyword blocks. Calculate real-world Intent, Backfire Probability, and Worst-Case Impact."),
        ("3. Live Recipient & DNS Verification:", "Verify whether recipient email domains physically exist on live internet DNS before allowing dispatch."),
        ("4. 1-Click Self-Healing AI Auto-Improve:", "Don't just yell at the user—automatically sanitize secrets and polish hostile tones into professional language with 1 click."),
        ("5. Bulletproof Security Gate:", "Make direct dispatch physically impossible without a signed safety preview token.")
    ]
    for title, desc in points_obj:
        p_t = tf2_r.add_paragraph()
        p_t.text = f"• {title} "
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = COLOR_PRIMARY
        p_d = tf2_r.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 3: Proposed Solution & Key Innovation (Template Page 3)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Proposed Solution & Key Innovation")

    # 3 Solution Cards across
    col_w = Inches(3.64)
    gap = Inches(0.4)
    top_pos = Inches(1.6)
    h_pos = Inches(5.2)

    # Card 1: The Gateway
    add_card(s3, Inches(0.8), top_pos, col_w, h_pos)
    tb3_1 = s3.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf3_1 = tb3_1.text_frame
    tf3_1.word_wrap = True
    p = tf3_1.paragraphs[0]
    p.text = "🛡️ 1. The Safety Gateway"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT

    items1 = [
        ("Physical Interception Gate:", "Direct agent-to-SMTP execution is completely blocked at code level."),
        ("Simulation Sandbox:", "Emails are staged in a mock environment that mimics real delivery."),
        ("Cryptographic Preview Token:", "The server only delivers emails that hold a valid, uncommitted preview receipt issued by the sandbox."),
        ("Zero Latency (<2ms):", "Instantaneous evaluation so users experience zero friction.")
    ]
    for t, d in items1:
        p_t = tf3_1.add_paragraph()
        p_t.text = f"• {t}"
        p_t.font.bold = True
        p_t.font.size = Pt(11)
        p_t.font.color.rgb = COLOR_PRIMARY
        p_d = tf3_1.add_paragraph()
        p_d.text = f"   {d}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = COLOR_MUTED

    # Card 2: Key Innovation - 3-Question Model
    add_card(s3, Inches(0.8) + col_w + gap, top_pos, col_w, h_pos)
    tb3_2 = s3.shapes.add_textbox(Inches(1.0) + col_w + gap, top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf3_2 = tb3_2.text_frame
    tf3_2.word_wrap = True
    p = tf3_2.paragraphs[0]
    p.text = "💡 2. The 3-Question Model"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    items2 = [
        ("Q1. What is the Intent?", "Classifies purpose (Routine=0, Complaint=5, Legal/HR=15, Money=20) and detects dangerous 'Intent Drift'."),
        ("Q2. Could it Backfire?", "Counts 11 real-world factors (external domains, reply-all, hostile tone) into reliable probability bands."),
        ("Q3. What is the Damage?", "Measures worst-case liability (Security, Legal, Financial) multiplied by reach and irreversibility."),
        ("Hard Floor Protection:", "Zero tolerance for leaked AWS keys, private RSA certificates, or violent threats (fixed >=80 CRITICAL).")
    ]
    for t, d in items2:
        p_t = tf3_2.add_paragraph()
        p_t.text = f"• {t}"
        p_t.font.bold = True
        p_t.font.size = Pt(11)
        p_t.font.color.rgb = COLOR_PRIMARY
        p_d = tf3_2.add_paragraph()
        p_d.text = f"   {d}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = COLOR_MUTED

    # Card 3: Self-Healing AI
    add_card(s3, Inches(0.8) + (col_w + gap)*2, top_pos, col_w, h_pos)
    tb3_3 = s3.shapes.add_textbox(Inches(1.0) + (col_w + gap)*2, top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf3_3 = tb3_3.text_frame
    tf3_3.word_wrap = True
    p = tf3_3.paragraphs[0]
    p.text = "✨ 3. 1-Click Auto-Healing"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    items3 = [
        ("Secret Scrubbing:", "Converts live AWS keys and passwords into safe organizational vault references (e.g. [Vault Ref #SEC-4091])."),
        ("Tone De-escalation:", "Rewrites furious, unprofessional rants into calm, constructive, legally defensible communications."),
        ("Iterative Calibration:", "First rewrite brings risk to 28-35 (SAFE zone), subsequent refinements drop it to 14-18."),
        ("Full Human Oversight:", "The user inspects the clean version before giving final approval.")
    ]
    for t, d in items3:
        p_t = tf3_3.add_paragraph()
        p_t.text = f"• {t}"
        p_t.font.bold = True
        p_t.font.size = Pt(11)
        p_t.font.color.rgb = COLOR_PRIMARY
        p_d = tf3_3.add_paragraph()
        p_d.text = f"   {d}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 4: System Architecture & Workflow (Template Page 4)
    # Includes Track Evidence: Agentic AI Workflow & Failure Handling
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "System Architecture & Workflow")

    # Workflow 5 Step Horizontal Pipeline
    pipe_top = Inches(1.6)
    step_w = Inches(2.18)
    step_gap = Inches(0.2)
    step_h = Inches(2.2)

    steps = [
        ("1. Draft Initiated", "Agent or user drafts an email with target, subject, & content.", COLOR_PRIMARY),
        ("2. Recipient DNS", "Live DNS test validates domain reachability & catches typos.", COLOR_ACCENT),
        ("3. Consequence Sim", "Scoring Engine computes Intent, Backfire, & Impact.", COLOR_AMBER),
        ("4. Safety Gate", "Intervention Popup: 0-39 Auto, 40-79 Review, 80+ Blocked.", COLOR_RED),
        ("5. SMTP Dispatch", "Dispatches real email with TLS & issues audit receipt.", COLOR_GREEN)
    ]

    for idx, (stitle, sdesc, scolor) in enumerate(steps):
        s_left = Inches(0.8) + idx * (step_w + step_gap)
        c = add_card(s4, s_left, pipe_top, step_w, step_h)
        tb_s = s4.shapes.add_textbox(s_left + Inches(0.1), pipe_top + Inches(0.15), step_w - Inches(0.2), step_h - Inches(0.3))
        tfs = tb_s.text_frame
        tfs.word_wrap = True
        ps = tfs.paragraphs[0]
        ps.text = stitle
        ps.font.size = Pt(12)
        ps.font.bold = True
        ps.font.color.rgb = scolor
        
        ps_d = tfs.add_paragraph()
        ps_d.text = sdesc
        ps_d.font.size = Pt(10)
        ps_d.font.color.rgb = COLOR_MUTED

    # Bottom Section: Agentic AI Required Evidence (Slide 10)
    add_card(s4, Inches(0.8), Inches(4.1), Inches(11.7), Inches(2.7), bg_color=COLOR_ACCENT_BG, border_color=COLOR_ACCENT)
    tb_ev = s4.shapes.add_textbox(Inches(1.0), Inches(4.2), Inches(11.3), Inches(2.5))
    tf_ev = tb_ev.text_frame
    tf_ev.word_wrap = True

    p_ev = tf_ev.paragraphs[0]
    p_ev.text = "🤖 AGENTIC AI TRACK EVIDENCE: AGENT WORKFLOW & FAILURE HANDLING"
    p_ev.font.size = Pt(13)
    p_ev.font.bold = True
    p_ev.font.color.rgb = COLOR_ACCENT

    ev_bullets = [
        ("Two-Phase 'Preview-then-Commit' Protocol:", "Separates reasoning and simulation from physical tool execution. Agents cannot bypass the sandbox because the dispatch tool demands a valid 'preview_id'."),
        ("Token Replay Prevention:", "Once a preview token is committed or modified, it is invalidated immediately to prevent double-spending or replay attacks."),
        ("Graceful Failure & DNS Fallback:", "If DNS resolution fails or times out, the system degrades to RFC 5322 syntax validation with explicit human warning rather than crashing."),
        ("Deterministic Hard Block Enforcement:", "If an agent hallucinates that sharing credentials is 'safe', the Hard-Rule Floor overrides the LLM, preventing accidental disaster.")
    ]
    for title, desc in ev_bullets:
        p_b = tf_ev.add_paragraph()
        p_b.text = f"• {title} "
        p_b.font.bold = True
        p_b.font.size = Pt(10.5)
        p_b.font.color.rgb = COLOR_PRIMARY
        p_b_d = tf_ev.add_paragraph()
        p_b_d.text = f"   {desc}"
        p_b_d.font.size = Pt(10)
        p_b_d.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 5: Technology Stack & Implementation (Template Page 5)
    # Includes AI/ML Track Evidence: Dataset, Model Selection & Metrics
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Technology Stack & Implementation")

    # Left: Architecture Stack
    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb5_l = s5.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf5_l = tb5_l.text_frame
    tf5_l.word_wrap = True

    p = tf5_l.paragraphs[0]
    p.text = "⚙️ TECHNOLOGY STACK"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    stack_items = [
        ("Zero-Dependency Server:", "Built on Python's native http.server and socket libraries. No bloated npm/pip web servers; lightweight and ultra-reliable."),
        ("Native SMTP & TLS:", "Direct integration with smtplib and email.message.EmailMessage over secure Port 587 with STARTTLS encryption."),
        ("Live DNS Socket Engine:", "Uses socket.getaddrinfo to query internet nameservers in real time to verify recipient domains."),
        ("Responsive Modern Frontend:", "Tailwind CSS styling with live status badges, side-by-side risk diffs, and zero disruptive browser alert boxes.")
    ]
    for t, d in stack_items:
        p_t = tf5_l.add_paragraph()
        p_t.text = f"• {t}"
        p_t.font.bold = True
        p_t.font.size = Pt(11)
        p_t.font.color.rgb = COLOR_ACCENT
        p_d = tf5_l.add_paragraph()
        p_d.text = f"   {d}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = COLOR_MUTED

    # Right: AI/ML Track Evidence (Slide 10)
    add_card(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb5_r = s5.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf5_r = tb5_r.text_frame
    tf5_r.word_wrap = True

    p = tf5_r.paragraphs[0]
    p.text = "📊 AI/ML TRACK EVIDENCE: DATASET & METRICS"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    ml_items = [
        ("Curated 21-Scenario Benchmark:", "Diverse ground-truth dataset spanning 7 categories: Routine, Complaint, Sensitive Info, Data Transfer, Legal, HR Action, and Financial."),
        ("Mathematical Consequentialist Engine:", "Risk = min(100, Content + Intent + round_half_up(Backfire_p * Impact)). Balances LLM intent analysis with deterministic rules."),
        ("100% Risk Detection Recall:", "Caught 16/16 risky scenarios with zero false negatives (exceeding the >=80% target)."),
        ("100% Specificity (Zero False Alarms):", "Cleared 5/5 benign emails without harassing the user."),
        ("Ultra-Low Latency Inference:", "Complete simulation, rule extraction, and consequence scoring executes in ~0.002 seconds.")
    ]
    for t, d in ml_items:
        p_t = tf5_r.add_paragraph()
        p_t.text = f"• {t}"
        p_t.font.bold = True
        p_t.font.size = Pt(11)
        p_t.font.color.rgb = COLOR_GREEN
        p_d = tf5_r.add_paragraph()
        p_d.text = f"   {d}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 6: Key Features & Functionalities (Template Page 6)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Key Features & Functionalities")

    # 4 Feature Grid Cards
    f_w = Inches(5.6)
    f_h = Inches(2.4)
    coords = [
        (Inches(0.8), Inches(1.6)),
        (Inches(6.8), Inches(1.6)),
        (Inches(0.8), Inches(4.3)),
        (Inches(6.8), Inches(4.3)),
    ]

    features = [
        ("🔍 1. Real DNS & Recipient Genuineness", 
         "Validates recipient syntax (RFC 5322), flags common typos (@gmial.com -> @gmail.com), and actively pings public DNS. Prevents accidental delivery to malicious lookalikes.",
         COLOR_ACCENT),
        ("🛡️ 2. Comprehensive 25+ Threat Detector",
         "Intercepts AWS keys, GitHub tokens, database passwords, private keys, Credit Cards, SSNs, HIPAA medical records, toxic HR language, and wire fraud scams.",
         COLOR_RED),
        ("📊 3. 3-Question Risk Intervention Popup",
         "Presents human operators with clear, explainable risk: Q1. Intent, Q2. Backfire Band, Q3. Worst-Case Consequence. Silent for safe emails (<40); strict for dangerous drafts.",
         COLOR_AMBER),
        ("✨ 4. 1-Click AI Auto-Improve & Real Dispatch",
         "Automatically redacts credentials into safe token pointers, de-escalates aggressive phrasing, recalculates risk score, and dispatches via authenticated Gmail TLS with audit receipt.",
         COLOR_GREEN)
    ]

    for (x, y), (ftitle, fdesc, fcolor) in zip(coords, features):
        add_card(s6, x, y, f_w, f_h)
        tb_f = s6.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), f_w - Inches(0.4), f_h - Inches(0.4))
        tff = tb_f.text_frame
        tff.word_wrap = True
        pf = tff.paragraphs[0]
        pf.text = ftitle
        pf.font.size = Pt(13)
        pf.font.bold = True
        pf.font.color.rgb = fcolor
        
        pf_d = tff.add_paragraph()
        pf_d.text = fdesc
        pf_d.font.size = Pt(11)
        pf_d.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 7: Live Demo / Working Prototype (Template Page 7)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Live Demo / Working Prototype")

    # 3 Demonstration Steps
    demo_w = Inches(3.64)
    demo_h = Inches(5.2)

    demo_cards = [
        ("Demo Step 1", "Typo & Fake Domain Test",
         "1. Enter test@fakedomainxyz9999.com.\n\n"
         "2. Real-time badge immediately flashes RED:\n"
         "   '✕ Domain does not exist on DNS'.\n\n"
         "3. Type a real address (e.g. Gmail) ➔ Badge turns GREEN: '✓ Valid & DNS Verified'.\n\n"
         "Result: Catches typos and non-existent domains before network transmission.",
         COLOR_RED),
        ("Demo Step 2", "Threat Scan & Auto-Improve",
         "1. Load 'AWS & Database Password Leak' from test cases.\n\n"
         "2. Click 'Simulate & Scan' ➔ Risk Score 100/100 (CRITICAL).\n\n"
         "3. Intervention Popup blocks direct send.\n\n"
         "4. Click '✨ Auto-Improve with AI' ➔ Secret redacted to [Vault Ref #SEC-4091] & score drops to 28/100 (SAFE)!\n\n"
         "Result: Self-healing AI removes danger instantly.",
         COLOR_AMBER),
        ("Demo Step 3", "Safety Commit & Real Dispatch",
         "1. With score in the Green zone, click 'Send Real Email'.\n\n"
         "2. ActionGuardian verifies preview token authenticity.\n\n"
         "3. Native SMTP dispatches email to recipient's real inbox via TLS.\n\n"
         "4. Live Audit Receipt generated with unique Tracking ID and timestamp.\n\n"
         "Result: Irreversible actions executed with 100% confidence.",
         COLOR_GREEN)
    ]

    for idx, (dstep, dtitle, dbody, dcolor) in enumerate(demo_cards):
        dx = Inches(0.8) + idx * (demo_w + gap)
        add_card(s7, dx, Inches(1.6), demo_w, demo_h)
        tbd = s7.shapes.add_textbox(dx + Inches(0.2), Inches(1.8), demo_w - Inches(0.4), demo_h - Inches(0.4))
        tfd = tbd.text_frame
        tfd.word_wrap = True

        p_s = tfd.paragraphs[0]
        p_s.text = dstep.upper()
        p_s.font.size = Pt(11)
        p_s.font.bold = True
        p_s.font.color.rgb = dcolor

        p_t = tfd.add_paragraph()
        p_t.text = dtitle
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_PRIMARY

        p_b = tfd.add_paragraph()
        p_b.text = dbody
        p_b.font.size = Pt(10.5)
        p_b.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 8: Future Scope (Template Page 8)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Future Scope")

    # 3 Forward-Looking Expansion Horizons
    h_w = Inches(3.64)
    h_h = Inches(5.2)

    horizons = [
        ("Horizon 1", "Financial & Payment Gateways",
         "• Pre-Transaction Wire Verification:\n  Simulate banking API calls before funds leave accounts.\n\n"
         "• Anomaly & Threshold Failsafes:\n  Detect anomalous wire requests exceeding typical agent spending limits.\n\n"
         "• Multi-Signature Approvals:\n  Require secondary executive confirmation for transfers over configured amounts.",
         COLOR_ACCENT),
        ("Horizon 2", "Multi-Agent Framework Proxy",
         "• Universal Middleware Proxy:\n  Plug-and-play middleware for LangChain, AutoGen, CrewAI, and LangGraph.\n\n"
         "• Cloud Sandbox Interceptor:\n  Intercept shell commands to prevent catastrophic 'DROP TABLE' or 'rm -rf' in production containers.\n\n"
         "• Agent Swarm Auditing:\n  Trace inter-agent communications for privilege escalation attempts.",
         COLOR_PRIMARY),
        ("Horizon 3", "Enterprise Policy Engines",
         "• Custom Regulatory Profiles:\n  One-click compliance packs for HIPAA, GDPR, SOC-2, and ITAR.\n\n"
         "• Adaptive Learning Models:\n  Learn organizational tone and communication norms over time without sacrificing safety floors.\n\n"
         "• SIEM / Splunk Integration:\n  Stream structured audit receipts into enterprise security dashboards.",
         COLOR_GREEN)
    ]

    for idx, (hstep, htitle, hbody, hcolor) in enumerate(horizons):
        hx = Inches(0.8) + idx * (h_w + gap)
        add_card(s8, hx, Inches(1.6), h_w, h_h)
        tbh = s8.shapes.add_textbox(hx + Inches(0.2), Inches(1.8), h_w - Inches(0.4), h_h - Inches(0.4))
        tfh = tbh.text_frame
        tfh.word_wrap = True

        p_s = tfh.paragraphs[0]
        p_s.text = hstep.upper()
        p_s.font.size = Pt(11)
        p_s.font.bold = True
        p_s.font.color.rgb = hcolor

        p_t = tfh.add_paragraph()
        p_t.text = htitle
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_PRIMARY

        p_b = tfh.add_paragraph()
        p_b.text = hbody
        p_b.font.size = Pt(10.5)
        p_b.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 9: Conclusion (Template Page 9)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Conclusion")

    # Hero Summary Card
    add_card(s9, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tbc = s9.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(10.9), Inches(4.6))
    tfc = tbc.text_frame
    tfc.word_wrap = True

    p = tfc.paragraphs[0]
    p.text = "ActionGuardian: The Essential Safety Seatbelt for Autonomous AI"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    bullets_conc = [
        ("Bridging the Trust Gap:", "Autonomous AI agents cannot achieve enterprise adoption if a single hallucination can dispatch confidential secrets or spark a legal catastrophe."),
        ("Physical Consequence Guarantee:", "By enforcing 'Preview-then-Commit', ActionGuardian ensures that no physical action occurs in the real world without a verified consequence preview."),
        ("Self-Correcting, Not Paralyzing:", "Traditional security stops work by shouting 'Access Denied'. ActionGuardian empowers users with 1-click self-healing rewrites that turn dangerous drafts into safe, professional communications."),
        ("Proven Reliability:", "100% Risk Recall, 100% Specificity across 21 rigorous benchmarks, zero external server dependencies, and full TLS-secured delivery."),
        ("The Bottom Line:", "'Never let an AI agent act in the real world without simulating its consequences first.'")
    ]

    for title, desc in bullets_conc:
        p_t = tfc.add_paragraph()
        p_t.text = f"• {title} "
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = COLOR_ACCENT
        p_d = tfc.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_MUTED

    # Save Presentation
    prs.save(filename)
    print(f"[SUCCESS] PowerPoint deck created successfully: {filename}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "ActionGuardian_Final_Pitch_Deck.pptx"
    create_deck(out_file)
