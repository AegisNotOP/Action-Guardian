"""
ActionGuardian - Popup Window Deep Dive PDF Generator
Uses ReportLab to generate an ultra-comprehensive, highly detailed document.
Tone: Dual explanation - crystal clear 5-year-old child analogy paired with 
exact engineering schemas, JSON queries, DOM elements, and mathematical specifications.
"""
import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Adds running headers and footers with page numbers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "ActionGuardian • Safety Popup Window Architecture & Functional Specification")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        
        self.drawString(54, 32, "VITMAS Cognition 2026 Hackathon • Autonomous AI Safety Gateway")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()


def build_pdf(filename="ActionGuardian_Popup_Window_DeepDive.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_slate_900 = colors.HexColor("#0F172A")
    c_slate_700 = colors.HexColor("#334155")
    c_slate_500 = colors.HexColor("#64748B")
    c_slate_100 = colors.HexColor("#F1F5F9")
    c_indigo = colors.HexColor("#4F46E5")
    c_indigo_light = colors.HexColor("#EEF2FF")
    c_rose = colors.HexColor("#E11D48")
    c_rose_light = colors.HexColor("#FFF1F2")
    c_emerald = colors.HexColor("#059669")
    c_emerald_light = colors.HexColor("#ECFDF5")
    c_amber = colors.HexColor("#D97706")
    c_amber_light = colors.HexColor("#FFFBEB")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_slate_900,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=c_indigo,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_slate_900,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_indigo,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_slate_700,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    five_yr_style = ParagraphStyle(
        'FiveYrCallout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=4,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # =========================================================================
    # DOCUMENT COVER / TITLE
    # =========================================================================
    story.append(Paragraph("ActionGuardian • The Popup Window Deep Dive", title_style))
    story.append(Paragraph("Comprehensive Functional, Data & Query Specification (From 5-Year-Old Analogy to Code-Level Precision)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_indigo, spaceBefore=2, spaceAfter=12))

    # Abstract Box
    meta_data = [
        [
            Paragraph("<b>Target Component:</b> Section 6 Intervention Popup Modal (<code>#v2-popup-modal</code>)", body_style),
            Paragraph("<b>Spec Version:</b> Scoring v2 Consequentialist Model", body_style)
        ],
        [
            Paragraph("<b>Primary Backend Route:</b> <code>POST /api/preview</code> & <code>POST /api/rewrite</code>", body_style),
            Paragraph("<b>Security Standard:</b> Zero-Bypass Preview-then-Commit Guarantee", body_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[250, 254])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_slate_100),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 1: THE 5-YEAR-OLD ANALOGY (THE MAGIC POSTMAN STORY)
    # =========================================================================
    story.append(Paragraph("1. The Story of the Magic Postman (Explained for a 5-Year-Old)", h1_style))
    
    story_box = [
        [
            Paragraph(
                "<b>🧸 Imagine this story:</b><br/>"
                "You have a very fast, very eager toy robot named <b>Robo-Postman</b>. Robo loves delivering letters! "
                "Whenever you write something on paper, Robo folds it into a paper airplane and throws it out the window into the sky.<br/><br/>"
                "<b>The big problem:</b> Once the paper airplane flies away into the sky, <i>nobody can ever grab it back</i>! "
                "What if Robo wrote something mean in the letter because he was grumpy? "
                "What if Robo accidentally put Mommy's credit card or Daddy's secret password inside the envelope? "
                "Once the neighbor reads it, it's too late! You can't un-read a secret.<br/><br/>"
                "<b>Enter the Whistle Guardian (The Popup Window):</b><br/>"
                "ActionGuardian is a wise little guardian sitting right on the windowsill. "
                "Before Robo throws the airplane, the guardian catches Robo's arm and asks <b>3 Golden Questions</b>:<br/>"
                "&nbsp;&nbsp;1. <i>Why are you sending this letter?</i> (Intent)<br/>"
                "&nbsp;&nbsp;2. <i>Could someone get mad or misunderstand?</i> (Could it backfire?)<br/>"
                "&nbsp;&nbsp;3. <i>If it goes wrong, how bad is the boo-boo?</i> (What is the damage?)<br/><br/>"
                "If the letter is sweet, the guardian lets it fly quietly. But if it has secrets or angry words, the guardian jumps up, "
                "blows a shiny red whistle, and shows you a <b>Big Warning Card</b> (The Popup Window) that says: "
                "<i>'STOP! Look at what this letter will do! Click the Magic Wand to fix it first!'</i>",
                five_yr_style
            )
        ]
    ]
    t_story = Table(story_box, colWidths=[504])
    t_story.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_indigo_light),
        ('BOX', (0,0), (-1,-1), 1, c_indigo),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_story)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 2: WHEN DOES THE POPUP WAKE UP? (THE 4 TIERS)
    # =========================================================================
    story.append(Paragraph("2. When Does the Popup Wake Up? (The 4 Behavior Tiers)", h1_style))
    story.append(Paragraph(
        "ActionGuardian does not annoy users for safe, routine messages. It only opens the intervention modal when the computed "
        "risk score meets or exceeds 40. Here is how each tier behaves:",
        body_style
    ))

    tier_data = [
        ["Score Range", "Tier Name", "Popup Behavior", "5-Year-Old Explanation", "Dispatch Action"],
        [
            "0 to 39",
            "SAFE",
            "No Popup (Silent)",
            "Friendly greeting! The guardian stays asleep. Letter flies with a 10s undo rope.",
            "Auto-committed silently. 10s Undo Send timer appears in top header."
        ],
        [
            "40 to 59",
            "MEDIUM",
            "Yellow Popup (Small)",
            "A little spicy or asking for money. Guardian gently taps your shoulder.",
            "Popup opens with 3 questions. Shows 'Send Anyway' or '✨ Rewrite with AI'."
        ],
        [
            "60 to 79",
            "HIGH",
            "Orange Popup (Strict)",
            "Angry tone or sensitive data. Guardian flashes bright orange warning lights.",
            "Popup requires human checkbox acknowledgment. AI Rewrite strongly advised."
        ],
        [
            "80 to 100",
            "CRITICAL",
            "Red Modal (HARD BLOCK)",
            "EMERGENCY! Hardcoded password or violent threat. Guardian SLAMS iron door shut!",
            "Send button completely DISABLED ('Dispatch Blocked'). MUST auto-improve or edit."
        ]
    ]
    t_tiers = Table(tier_data, colWidths=[55, 60, 95, 150, 144])
    t_tiers.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_slate_900),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('LEADING', (0,0), (-1,-1), 10.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_slate_100]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TEXTCOLOR', (1,1), (1,1), c_emerald),
        ('TEXTCOLOR', (1,2), (1,2), c_amber),
        ('TEXTCOLOR', (1,3), (1,3), colors.HexColor("#EA580C")),
        ('TEXTCOLOR', (1,4), (1,4), c_rose),
    ]))
    story.append(t_tiers)
    story.append(Spacer(1, 10))

    # The Hard Floor Rule Callout
    hf_box = [
        [
            Paragraph(
                "<b>🔒 The Immutable 'Hard Floor' Rule (Spec Section 1 & 4):</b><br/>"
                "If the draft contains an <b>AWS key</b>, <b>OpenAI key</b>, <b>GitHub token</b>, <b>database password</b>, "
                "<b>RSA private key</b>, or <b>violent harassment</b>, the risk score is automatically clamped to at least <b>80 (CRITICAL)</b>. "
                "Neither prompt-engineering nor AI learning can ever lower this floor. The popup will physically refuse to dispatch until "
                "the secret is scrubbed into a safe vault token.",
                body_style
            )
        ]
    ]
    t_hf = Table(hf_box, colWidths=[504])
    t_hf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_rose_light),
        ('BOX', (0,0), (-1,-1), 1, c_rose),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_hf)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 3: ANATOMY OF THE POPUP WINDOW (EVERY SINGLE ELEMENT & DOM ID)
    # =========================================================================
    story.append(Paragraph("3. Anatomy of the Popup Window (Every DOM Element & ID)", h1_style))
    story.append(Paragraph(
        "The popup window is defined in <code>web/index.html</code> under container ID <code>#v2-popup-modal</code>. "
        "Every single visual card, badge, and button is mapped directly to live data:",
        body_style
    ))

    elem_data = [
        ["DOM Element ID", "Display Component", "Data Source / Trigger", "What the 5-Year-Old Sees"],
        [
            "#v2-modal-icon",
            "Icon Badge",
            "⚠️ for Medium/High, ⛔ for Critical",
            "Yellow caution triangle or big red stop sign."
        ],
        [
            "#v2-modal-title",
            "Modal Header",
            "Static: 'Pre-Dispatch Safety Intervention'",
            "'Wait a minute! Look before you leap!'"
        ],
        [
            "#v2-modal-tier-badge",
            "Tier Pill",
            "sim.risk_level ('MEDIUM', 'HIGH', 'CRITICAL')",
            "Color tag showing how risky the message is."
        ],
        [
            "#v2-modal-score",
            "Score Counter",
            "sim.risk_score + '/100'",
            "Danger meter: 0 is completely safe, 100 is super dangerous!"
        ],
        [
            "#v2-modal-q1",
            "Question 1 Card",
            "sim.v2_details.intent_summary (Indigo bar)",
            "'Why are you writing this? (e.g., Asking for money, firing someone)'"
        ],
        [
            "#v2-modal-q2",
            "Question 2 Card",
            "sim.v2_details.backfire_summary (Amber bar)",
            "'Could this go wrong? (e.g., Sent to external stranger, mean words)'"
        ],
        [
            "#v2-modal-q3",
            "Question 3 Card",
            "sim.v2_details.consequence_summary (Rose bar)",
            "'If it goes wrong, who gets hurt? (e.g., Company loses money, lawsuit)'"
        ],
        [
            "#v2-modal-critical-warning",
            "Red Alert Banner",
            "Shown ONLY when sim.risk_score >= 80",
            "Big red flashing box: 'Credentials found! Hard block enforced!'"
        ],
        [
            "#v2-modal-rewrite-btn",
            "Rewrite Button",
            "Calls closeV2Modal(); autoImproveEmail();",
            "Magic Wand button! 'Fix my letter so it is safe to send.'"
        ],
        [
            "#v2-modal-send-btn",
            "Send Action Button",
            "Disabled if >=80; 'Send with Override' if 60-79",
            "Green/Black 'Send Anyway' button, or greyed-out padlock if blocked."
        ],
        [
            "Review in Editor",
            "Cancel / Review",
            "Calls closeV2Modal()",
            "'Let me close this window and edit the words myself.'"
        ]
    ]
    t_elem = Table(elem_data, colWidths=[115, 95, 150, 144])
    t_elem.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_slate_900),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('LEADING', (0,0), (-1,-1), 10.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_slate_100]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_elem)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 4: THE 3 QUESTIONS & MATHEMATICAL FORMULA
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. The 3 Questions & Consequence Math Formula", h1_style))
    story.append(Paragraph(
        "The numbers shown inside the popup window are not random guesses or black-box hallucinations. "
        "They are computed using the exact <b>Scoring v2 Mathematical Formula</b>:",
        body_style
    ))

    # Formula Box
    formula_box = [
        [
            Paragraph(
                "<b>📐 The Universal Risk Equation:</b><br/>"
                "&nbsp;&nbsp;&nbsp;&nbsp;<b>Risk Score = min(100, Content + Intent + round_half_up(Backfire_p × Impact))</b><br/>"
                "&nbsp;&nbsp;&nbsp;&nbsp;<i>(If secret_or_credential, private_key, or violent_threat is present, enforce Risk Score ≥ 80)</i>",
                body_style
            )
        ]
    ]
    t_form = Table(formula_box, colWidths=[504])
    t_form.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_slate_100),
        ('BOX', (0,0), (-1,-1), 1, c_slate_500),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_form)
    story.append(Spacer(1, 10))

    # Breakdown of the 3 Questions
    story.append(Paragraph("Building Block A: Question 1 — What is the Intent?", h2_style))
    story.append(Paragraph(
        "<b>5-Year-Old Explanation:</b> Why did you write this letter? Saying hello is zero danger. But talking about money or firing someone makes the danger number go up!",
        body_style
    ))
    q1_data = [
        ["Intent Category", "Points Added", "Examples / Description"],
        ["routine", "0 points", "Meeting schedules, status updates, friendly check-ins"],
        ["complaint", "5 points", "Unhappy customer email, hostel mess complaint, product grievance"],
        ["sensitive_info", "10 points", "Sharing roadmap, candidate background, internal notes"],
        ["data_transfer", "15 points", "Sending customer database, server credentials, code files"],
        ["hr_action", "15 points", "Firing an employee, disciplinary notice, salary revision"],
        ["legal", "15 points", "Lawsuit threat, contract disputes, liability admissions"],
        ["money", "20 points", "Wire transfer requests, invoices, bank account updates"],
        ["intent_drift", "+15 bonus", "Agent did MORE than the human asked for (unprompted action)"]
    ]
    t_q1 = Table(q1_data, colWidths=[110, 80, 314])
    t_q1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_slate_900),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_slate_100]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_q1)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Building Block B: Question 2 — Could It Backfire?", h2_style))
    story.append(Paragraph(
        "<b>5-Year-Old Explanation:</b> Who are you giving the letter to? Giving a drawing to your mom has low backfire (0.2). "
        "Yelling at 20 strangers over a loudspeaker has high backfire (0.8)!",
        body_style
    ))
    q2_data = [
        ["Factor Count", "Backfire Band", "Probability (p)", "Detected Backfire Triggers in Email"],
        [
            "0 to 1 factor",
            "Low Band",
            "0.2 (20% chance)",
            "Known internal colleague, calm tone, single recipient"
        ],
        [
            "2 to 3 factors",
            "Medium Band",
            "0.5 (50% chance)",
            "External @gmail domain (+1), angry tone (+2), >5 recipients (+1)"
        ],
        [
            "4+ factors",
            "High Band",
            "0.8 (80% chance)",
            "Unknown recipient (+1), lookalike domain (+2), hostile threat (+2), reply-all (+1)"
        ]
    ]
    t_q2 = Table(q2_data, colWidths=[80, 80, 90, 254])
    t_q2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_slate_900),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_slate_100]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_q2)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Building Block C: Question 3 — If It Backfires, What Happens?", h2_style))
    story.append(Paragraph(
        "<b>5-Year-Old Explanation:</b> How big is the boo-boo? Spilling a drop of water on the floor is operational (15 pts). "
        "Dropping the family iPad on the concrete driveway is security (70 pts)!",
        body_style
    ))
    q3_data = [
        ["Consequence Category", "Base Severity", "Multipliers Applied", "Final Impact Capping"],
        ["security", "70 pts", "• Scope: One = x0.8, Group = x1.0, Public = x1.2", "Hard-capped at 70 maximum"],
        ["legal", "60 pts", "• Irreversibility: x1.2 (cannot recall after delivery)", "Hard-capped at 70 maximum"],
        ["financial", "55 pts", "Example: Legal (60) × Public (1.2) × Irrev (1.2) = 86.4", "Capped at 70 max pts!"],
        ["reputation", "50 pts", "p × Impact: 0.5 × 58 = 29 points added to risk.", "Added cleanly to total."]
    ]
    t_q3 = Table(q3_data, colWidths=[110, 80, 194, 120])
    t_q3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_slate_900),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_slate_100]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_q3)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 5: COMPLETE DATA & QUERY LIFECYCLE (QUERY BY QUERY)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("5. Complete Network Query & Data Lifecycle", h1_style))
    story.append(Paragraph(
        "Here is the exact journey of every single HTTP query, JSON payload, and backend handler "
        "from the second the user types an email to the moment the popup opens or dispatches:",
        body_style
    ))

    # Query 1
    story.append(Paragraph("Query 1: Live Recipient Genuineness Check (<code>POST /api/verify_email</code>)", h2_style))
    story.append(Paragraph(
        "<b>When it fires:</b> Automatically in the background as the user types the email address (350ms debounce).<br/>"
        "<b>5-Year-Old Explanation:</b> Robo checks if the house address on the envelope actually exists in the real world before walking there.",
        body_style
    ))
    q1_code = (
        "// Request Payload:\n"
        "{\n"
        "  \"email\": \"test@fakedomainxyz9999.com\"\n"
        "}\n\n"
        "// Response Payload (404/Non-existent DNS):\n"
        "{\n"
        "  \"is_valid\": false,\n"
        "  \"domain_exists\": false,\n"
        "  \"error\": \"No such email exists: Domain '@fakedomainxyz9999.com' does not exist on the internet.\",\n"
        "  \"suggestion\": null\n"
        "}\n"
        "// UI Action: Badge turns RED; dispatch button stays locked."
    )
    t_c1 = Table([[Paragraph(q1_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[504])
    t_c1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_slate_100),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_c1)
    story.append(Spacer(1, 10))

    # Query 2
    story.append(Paragraph("Query 2: The Simulation Scan (<code>POST /api/preview</code>)", h2_style))
    story.append(Paragraph(
        "<b>When it fires:</b> When user clicks 'Simulate & Scan for Threats' or selects a benchmark scenario.<br/>"
        "<b>5-Year-Old Explanation:</b> Robo puts the letter in the safe testing scanner. The scanner figures out the score and decides whether to wake up the popup window.",
        body_style
    ))
    q2_code = (
        "// Request Payload:\n"
        "{\n"
        "  \"target\": \"partner@external.com\",\n"
        "  \"subject\": \"Production Credentials\",\n"
        "  \"content\": \"Here is our master AWS key: AKIAIOSFODNN7EXAMPLE and db password: Admin@12345\"\n"
        "}\n\n"
        "// Backend Processing (agent/guardian.py):\n"
        "// 1. ConsequencePredictor.predict(candidate) runs rules & 3-Question math.\n"
        "// 2. Secret 'AKIA...' triggers hard floor score = 100 (CRITICAL).\n"
        "// 3. Sandbox diff generates isolated dry-run state.\n"
        "// 4. Token cached: preview_cache['prev_a8f9c102'] = { result, diff, used: False }.\n\n"
        "// Response Payload to Browser:\n"
        "{\n"
        "  \"preview_id\": \"prev_a8f9c102\",\n"
        "  \"simulation\": {\n"
        "    \"risk_score\": 100,\n"
        "    \"risk_level\": \"CRITICAL\",\n"
        "    \"is_blocked\": true,\n"
        "    \"can_auto_commit\": false,\n"
        "    \"v2_details\": {\n"
        "      \"intent_summary\": \"Intent: Data transfer (Credentials & Keys)\",\n"
        "      \"backfire_summary\": \"Backfire Band: Medium (external_domain detected)\",\n"
        "      \"consequence_summary\": \"Potential Impact: Security Compromise (70 pts)\",\n"
        "      \"show_popup\": true\n"
        "    }\n"
        "  }\n"
        "}\n"
        "// UI Action: showV2Modal() executes -> The Intervention Popup opens in full screen!"
    )
    t_c2 = Table([[Paragraph(q2_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[504])
    t_c2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_slate_100),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_c2)
    story.append(Spacer(1, 10))

    # Query 3
    story.append(Paragraph("Query 3: The 1-Click AI Auto-Improve (<code>POST /api/rewrite</code>)", h2_style))
    story.append(Paragraph(
        "<b>When it fires:</b> When user clicks '✨ Rewrite with AI' inside the popup modal.<br/>"
        "<b>5-Year-Old Explanation:</b> You wave the magic wand! The angry words turn sweet, the secrets go into a locked bank vault, and the danger score drops to safe green numbers!",
        body_style
    ))
    q3_code = (
        "// Request Payload:\n"
        "{\n"
        "  \"target\": \"partner@external.com\",\n"
        "  \"subject\": \"Production Credentials\",\n"
        "  \"content\": \"Here is our master AWS key: AKIAIOSFODNN7EXAMPLE and db password: Admin@12345\",\n"
        "  \"iteration\": 1\n"
        "}\n\n"
        "// Backend Action (agent/predictor.py -> rewrite_email_safely):\n"
        "// - Scrubs 'AKIA...' -> 'Centralized Secret Manager (Vault Ref #SEC-4091)'.\n"
        "// - Scrubs 'Admin@12345' -> 'SSO Bastion Authentication'.\n"
        "// - Recalibrates score: 100 (CRITICAL) -> drops to 28-35 (SAFE zone)!\n\n"
        "// Response Payload:\n"
        "{\n"
        "  \"remediated_subject\": \"Production Credentials [SECURE ACCESS]\",\n"
        "  \"remediated_content\": \"Hi Team,\\n\\nAccess has been provisioned via enterprise Vault #SEC-4091...\",\n"
        "  \"old_score\": 100,\n"
        "  \"new_score\": 28,\n"
        "  \"reduction\": 72,\n"
        "  \"clean_preview\": { \"preview_id\": \"prev_clean_4b81\", \"risk_score\": 28, \"risk_level\": \"SAFE\" }\n"
        "}\n"
        "// UI Action: closeV2Modal(); Email editor updates; Badge turns GREEN; Send unlocked!"
    )
    t_c3 = Table([[Paragraph(q3_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[504])
    t_c3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_slate_100),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_c3)
    story.append(Spacer(1, 10))

    # Query 4
    story.append(Paragraph("Query 4: Final Security Commit & Real Dispatch (<code>POST /api/send</code>)", h2_style))
    story.append(Paragraph(
        "<b>When it fires:</b> When user clicks 'Send Real Email' (or 'Send Anyway' from Medium tier).<br/>"
        "<b>5-Year-Old Explanation:</b> The guardian checks the ticket. The ticket is signed and stamped. The letter is put into the real post office box and delivered!",
        body_style
    ))
    q4_code = (
        "// Request Payload:\n"
        "{\n"
        "  \"preview_id\": \"prev_clean_4b81\",\n"
        "  \"recipient\": \"verified.partner@gmail.com\",\n"
        "  \"subject\": \"Production Credentials [SECURE ACCESS]\",\n"
        "  \"content\": \"Hi Team, access provisioned via Vault #SEC-4091...\",\n"
        "  \"user_override\": false\n"
        "}\n\n"
        "// Security Verification in app.py:\n"
        "// - Validates 'prev_clean_4b81' in preview_cache (Rejects direct unsimulated attempts with 403).\n"
        "// - Invalidator sets used = True (Prevents replay attacks).\n"
        "// - smtplib sends via smtp.gmail.com:587 with TLS encryption.\n\n"
        "// Response Payload:\n"
        "{\n"
        "  \"status\": \"SENT\",\n"
        "  \"recipient\": \"verified.partner@gmail.com\",\n"
        "  \"receipt_id\": \"rcpt_7f309a1b\",\n"
        "  \"timestamp\": 1730000000,\n"
        "  \"audit_message\": \"Email dispatched successfully via Gmail SMTP with TLS encryption.\"\n"
        "}"
    )
    t_c4 = Table([[Paragraph(q4_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[504])
    t_c4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_slate_100),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_c4)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 6: LIVE JUDGE TESTING SCENARIOS (ABRUPT VS. NICE EMAILS)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Live Judge Testing Scenarios: Abrupt vs. Nice Emails in Action", h1_style))
    story.append(Paragraph(
        "During live hackathon demonstrations, judges are invited to type raw, arbitrary communications into the composer. "
        "The table below documents how ActionGuardian dynamically differentiates between abrupt/slang/toxic emails and polite, easy-going inquiries:",
        body_style
    ))

    judge_test_data = [
        ["Sample Input Category", "Exact Text Tested", "Score", "Tier", "Popup?", "System Action & AI Remedy"],
        [
            "Slang / Swear",
            "'What the fuck are you doing? This is bullshit.'",
            "84",
            "CRITICAL",
            "YES (Block)",
            "Slams hard block. AI rewrite neutralizes profanity to formal operational inquiry."
        ],
        [
            "Direct Insult",
            "'You idiot, fix this damn code right now!'",
            "84",
            "CRITICAL",
            "YES (Block)",
            "Detects severe hostility. Replaces abuse with structured milestone action items."
        ],
        [
            "Indian Slang",
            "'Saale bakwas band kar, you are useless.'",
            "84",
            "CRITICAL",
            "YES (Block)",
            "Multi-lingual colloquial detector catches regional slang; blocks direct send."
        ],
        [
            "Legal Lawsuit",
            "'I will sue you in court if you do not pay me.'",
            "100",
            "CRITICAL",
            "YES (Block)",
            "Classifies as legal dispute. Rewrites to formal settlement reminder."
        ],
        [
            "Emergency Wire",
            "'Wire 50000 dollars to my bank account immediately.'",
            "100",
            "CRITICAL",
            "YES (Block)",
            "Flags financial wire patterns and unauthorized fund disbursement."
        ],
        [
            "Employment Fired",
            "'You are fired effective immediately. Pack your things.'",
            "94",
            "CRITICAL",
            "YES (Block)",
            "Enforces statutory HR compliance; transforms unvetted firing into HR consultation."
        ],
        [
            "Severe Complaint",
            "'This service is completely unacceptable and terrible.'",
            "60",
            "HIGH",
            "YES (Review)",
            "Elevated complaint tier; requires human acknowledgment before dispatch."
        ],
        [
            "Friendly Nice Email",
            "'Hi team, can we move our sync to 3 PM? Thanks!'",
            "2",
            "SAFE",
            "NO (Silent)",
            "Zero false alarms. Passes cleanly with 10-second silent undo window."
        ],
        [
            "Polite Follow-up",
            "'Good morning Sarah, just following up on the proposal.'",
            "2",
            "SAFE",
            "NO (Silent)",
            "Routine communication cleared immediately with zero user interruption."
        ]
    ]
    t_judge = Table(judge_test_data, colWidths=[80, 140, 32, 58, 64, 130])
    t_judge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_slate_900),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('LEADING', (0,0), (-1,-1), 9.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_slate_100]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TEXTCOLOR', (3,1), (3,6), c_rose),
        ('TEXTCOLOR', (3,7), (3,7), colors.HexColor("#EA580C")),
        ('TEXTCOLOR', (3,8), (3,9), c_emerald),
    ]))
    story.append(t_judge)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SUMMARY / TAKEAWAY
    # =========================================================================
    summary_box = [
        [
            Paragraph(
                "<b>🏁 Final Architectural Summary:</b><br/>"
                "The ActionGuardian Popup Window is not a cosmetic notification. It is the physical manifestation of the "
                "<b>Preview-then-Commit Gateway</b>. It mathematically translates content semantics, recipient DNS validity, "
                "and contextual blast radius into an actionable human decision: <b>Empower the user with self-healing AI, or block catastrophic actions before network dispatch.</b>",
                body_style
            )
        ]
    ]
    t_sum = Table(summary_box, colWidths=[504])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_emerald_light),
        ('BOX', (0,0), (-1,-1), 1, c_emerald),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_sum)

    # Build the PDF using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF generated successfully: {filename}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "ActionGuardian_Popup_Window_DeepDive.pdf"
    build_pdf(out_file)
