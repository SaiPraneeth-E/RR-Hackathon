import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(0.5 * inch, 10.5 * inch, "SupeRR Selector Season 2 — Behind the Scenes: Journey & Breakthroughs")
            self.drawRightString(8.0 * inch, 10.5 * inch, "Rajasthan Royals Round 1 Challenge")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(0.5 * inch, 10.42 * inch, 8.0 * inch, 10.42 * inch)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.0 * inch, 0.35 * inch, page_text)
        self.drawString(0.5 * inch, 0.35 * inch, "Author: E Sai Praneeth • Platform: https://github.com/SaiPraneeth-E/RR-Hackathon")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(0.5 * inch, 0.45 * inch, 8.0 * inch, 0.45 * inch)
        self.restoreState()


def build_journey_pdf():
    pdf_filename = "MY_JOURNEY_STEP_BY_STEP.pdf"
    alt_filename = "E_SAI_PRANEETH_JOURNEY.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.6 * inch
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    rr_pink = colors.HexColor("#E91E63")
    rr_navy = colors.HexColor("#0F172A")
    rr_blue = colors.HexColor("#1E3A8A")
    accent_gold = colors.HexColor("#D97706")
    text_dark = colors.HexColor("#1E293B")
    card_bg = colors.HexColor("#F8FAFC")
    border_subtle = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=rr_navy,
        alignment=0,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=rr_pink,
        spaceAfter=12
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#64748B")
    )

    h1_style = ParagraphStyle(
        'StepH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=rr_navy,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'StepH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=text_dark,
        spaceAfter=6
    )

    quote_style = ParagraphStyle(
        'QuoteStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=4,
        spaceAfter=4
    )

    callout_title = ParagraphStyle(
        'CalloutTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=rr_pink
    )

    table_header = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=text_dark,
        alignment=1
    )

    story = []

    # Title & Header Banner
    story.append(Paragraph("SUPERR SELECTOR SEASON 2 — BEHIND THE SCENES", title_style))
    story.append(Paragraph("The Data Science Journey: How We Built the Pressure Reliability Index (PRI)", subtitle_style))
    
    meta_table_data = [
        [
            Paragraph("<b>Participant:</b> E Sai Praneeth<br/><b>Role:</b> Sports Data Scientist & Analytics Engineer", meta_style),
            Paragraph("<b>Hackathon:</b> Rajasthan Royals SupeRR Selector S2<br/><b>Problem:</b> Identifying Players Under Pressure", meta_style),
            Paragraph("<b>Dataset:</b> 2022–2026 IPL & T20Is (207,678 Deliveries)<br/><b>Interactive App:</b> Streamlit 11-Module Suite", meta_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), card_bg),
        ('BOX', (0,0), (-1,-1), 1, border_subtle),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Executive Journey Narrative Box
    journey_intro = (
        "<b>The Mission:</b> Every T20 tournament has flat-track bullies who feast on gentle mid-innings bowling "
        "when victory is already assured, only to freeze when 18 runs are needed off the final 10 deliveries. "
        "Our journey was not merely to compute cricket averages, but to build an empirical, objective decision engine "
        "capable of identifying true ice-in-the-veins match-winners for the Rajasthan Royals franchise."
    )
    intro_table = Table([[Paragraph(journey_intro, quote_style)]], colWidths=[7.5*inch])
    intro_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('LINELEFT', (0,0), (-1,-1), 4, rr_pink),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#BFDBFE")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(intro_table)
    story.append(Spacer(1, 12))

    # STEP 1
    story.append(Paragraph("Step 1: Rejecting 'One-Size-Fits-All' Definitions of Pressure", h1_style))
    story.append(Paragraph(
        "When we first opened the dataset of 883 matches and 207,678 deliveries, our first instinct was: <i>What is pressure?</i> "
        "Many public models define pressure lazily as just 'overs 16 to 20' or 'run chases'. "
        "We realized that this simplistic threshold is completely blind to match reality. "
        "Defending 15 runs in the final over is maximum tension, but cruising at 80/0 needing 10 runs in over 17 has near-zero pressure. "
        "Similarly, batting in over 2 after losing 3 wickets for 9 runs is an existential crisis.",
        body_style
    ))
    story.append(Paragraph(
        "To capture genuine match tension, we formulated a <b>4-Pillar Multi-Context Pressure Architecture</b>:",
        body_style
    ))
    
    pillars_data = [
        [Paragraph("Pillar", table_header), Paragraph("Context Signal", table_header), Paragraph("Empirical Rationale & Weight", table_header)],
        [Paragraph("<b>1. Stage Leverage</b>", table_cell), Paragraph("Overs 16–20 (Death)", table_cell), Paragraph("Margin for error collapses; par economy accelerates to 10.56 RPO. (35% Weight)", table_cell)],
        [Paragraph("<b>2. Chase Knife-Edge</b>", table_cell), Paragraph("RRR > 9.0 or Wickets < 5", table_cell), Paragraph("Dot balls non-linearly spike wicket hazard rate by +42%. (30% Weight)", table_cell)],
        [Paragraph("<b>3. Batter Mortality</b>", table_cell), Paragraph("First 6 Balls of Innings", table_cell), Paragraph("Wicket probability is 3.1x higher before eye is in; absorbing crisis. (20% Weight)", table_cell)],
        [Paragraph("<b>4. Tournament Stakes</b>", table_cell), Paragraph("Playoffs & ICC Knockouts", table_cell), Paragraph("1.25x consequence multiplier for elimination games. (15% Weight)", table_cell)]
    ]
    ptab = Table(pillars_data, colWidths=[1.8*inch, 2.2*inch, 3.5*inch])
    ptab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), rr_navy),
        ('BOX', (0,0), (-1,-1), 0.5, border_subtle),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(ptab)
    story.append(Spacer(1, 10))

    if os.path.exists("figures/fig6_over_pressure_curve.png"):
        story.append(Image("figures/fig6_over_pressure_curve.png", width=7.2*inch, height=2.2*inch))
        story.append(Paragraph("<i>Figure 1: Empirical Leverage Curve across 20 overs demonstrating tension surge in overs 16–20 and chasing knife-edges.</i>", meta_style))
        story.append(Spacer(1, 10))

    # STEP 2
    story.append(Paragraph("Step 2: The Breakthrough — Uncovering the 'Formula 1 Paradox'", h1_style))
    story.append(Paragraph(
        "During our initial exploratory runs, we encountered a puzzling paradox: raw bowling statistics rated middle-overs "
        "spinners ahead of death-overs specialists. Jasprit Bumrah's raw economy was 7.32 RPO, whereas a defensive spinner bowling "
        "overs 7–10 had an economy of 6.70 RPO. Had we stopped there, our model would have concluded that the spinner is a better pressure bowler. "
        "This is the <b>Formula 1 Paradox</b>.",
        body_style
    ))
    
    f1_box = (
        "<b>💡 The Formula 1 Analogy:</b><br/>"
        "Bowling over 19 is like driving an F1 car at 300 km/h where the situational par economy is <b>10.56 RPO</b>. "
        "Bowling over 8 is driving in a school zone where par economy is <b>7.43 RPO</b>. "
        "Conceding 7.32 RPO at the death is extraordinary—it represents a <b>+1.99 Runs/Over Saving vs Situational Par</b>. "
        "Conceding 6.70 in a school zone is merely average. "
        "We realized we must never evaluate bowlers on raw economy, but on <b>Phase-Adjusted Par Savings (Phase ΔEcon)</b>."
    )
    f1_table = Table([[Paragraph(f1_box, body_style)]], colWidths=[7.5*inch])
    f1_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('LINELEFT', (0,0), (-1,-1), 4, accent_gold),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#FDE68A")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(f1_table)
    story.append(Spacer(1, 10))

    if os.path.exists("figures/fig2_bowling_containment.png"):
        story.append(Image("figures/fig2_bowling_containment.png", width=7.2*inch, height=2.3*inch))
        story.append(Paragraph("<i>Figure 2: Phase-Adjusted Economy Savings. Death-overs specialists (Bumrah, Narine, Afridi) surge when evaluated against situational par.</i>", meta_style))
        story.append(Spacer(1, 12))

    story.append(PageBreak())

    # STEP 3
    story.append(Paragraph("Step 3: The Clutch Discoveries — Uncapped Finishers vs Flat-Track Bullies", h1_style))
    story.append(Paragraph(
        "When we applied our Situational Run Value Added (RVA) and Strike Rate Acceleration (ΔSR) metrics to batters, "
        "the leaderboard revealed two stunning revelations that reputation-based scouting routinely misses:",
        body_style
    ))
    
    disc_data = [
        [Paragraph("Discovery", table_header), Paragraph("Data Evidence", table_header), Paragraph("Franchise Scouting Takeaway", table_header)],
        [
            Paragraph("<b>Naman Dhir (#1) & Shashank Singh (#2)</b>", table_cell),
            Paragraph("ΔSR: +17.2 & +14.8<br/>Boundary %: 30.1%<br/>Dot %: 27.9%", table_cell),
            Paragraph("True clutch accelerators. Unlike traditional anchors who eat dots before catching up, they hit boundaries from ball one without stalling.", table_cell)
        ],
        [
            Paragraph("<b>The Flat-Track Regressors</b>", table_cell),
            Paragraph("ΔSR: -5.0 to -18.2<br/>Dot % under pressure: > 45%", table_cell),
            Paragraph("Players whose career stats look inflated on flat pitches, but whose boundary hitting collapses when required run rates spike above 10.0.", table_cell)
        ]
    ]
    dtab = Table(disc_data, colWidths=[2.2*inch, 2.2*inch, 3.1*inch])
    dtab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), rr_navy),
        ('BOX', (0,0), (-1,-1), 0.5, border_subtle),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(dtab)
    story.append(Spacer(1, 10))

    if os.path.exists("figures/fig7_rise_vs_dip.png"):
        story.append(Image("figures/fig7_rise_vs_dip.png", width=7.2*inch, height=2.4*inch))
        story.append(Paragraph("<i>Figure 3: Clutch vs Regressors Quadrant Analysis separating true accelerators (top-right) from flat-track players (bottom-left).</i>", meta_style))
        story.append(Spacer(1, 12))

    # STEP 4
    story.append(Paragraph("Step 4: The Official Verified Top 10 Rankings", h1_style))
    story.append(Paragraph(
        "Combining our metrics into the <b>Pressure Reliability Index (PRI 0–100)</b>, here are the official rankings "
        "submitted in the Unstop dropdowns:",
        body_style
    ))

    top_data = [
        [Paragraph("Rank", table_header), Paragraph("Top 10 Batters (Clutch Finishers)", table_header), Paragraph("PRI", table_header), Paragraph("Top 10 Bowlers (Containment Specialists)", table_header), Paragraph("PRI", table_header)],
        [Paragraph("<b>1</b>", table_cell), Paragraph("<b>Naman Dhir</b> (ID: 37052)", table_cell), Paragraph("<b>94.2</b>", table_cell), Paragraph("<b>Mohammad Nawaz</b> (ID: 2490)", table_cell), Paragraph("<b>94.5</b>", table_cell)],
        [Paragraph("<b>2</b>", table_cell), Paragraph("<b>Shashank Singh</b> (ID: 2756)", table_cell), Paragraph("<b>93.8</b>", table_cell), Paragraph("<b>Abrar Ahmed</b> (ID: 5979)", table_cell), Paragraph("<b>93.7</b>", table_cell)],
        [Paragraph("<b>3</b>", table_cell), Paragraph("<b>Rishabh Pant</b> (ID: 4703)", table_cell), Paragraph("<b>92.5</b>", table_cell), Paragraph("<b>Sunil Narine</b> (ID: 781)", table_cell), Paragraph("<b>93.1</b>", table_cell)],
        [Paragraph("<b>4</b>", table_cell), Paragraph("<b>Suryakumar Yadav</b> (ID: 1699)", table_cell), Paragraph("<b>91.9</b>", table_cell), Paragraph("<b>Akeal Hosein</b> (ID: 2417)", table_cell), Paragraph("<b>92.4</b>", table_cell)],
        [Paragraph("<b>5</b>", table_cell), Paragraph("<b>Tim David</b> (ID: 6396)", table_cell), Paragraph("<b>90.4</b>", table_cell), Paragraph("<b>Mitchell Santner</b> (ID: 4101)", table_cell), Paragraph("<b>91.8</b>", table_cell)],
        [Paragraph("<b>6</b>", table_cell), Paragraph("<b>Ishan Kishan</b> (ID: 4117)", table_cell), Paragraph("<b>89.7</b>", table_cell), Paragraph("<b>Jasprit Bumrah</b> (ID: 2933)", table_cell), Paragraph("<b>91.2</b>", table_cell)],
        [Paragraph("<b>7</b>", table_cell), Paragraph("<b>Dinesh Karthik</b> (ID: 143)", table_cell), Paragraph("<b>88.8</b>", table_cell), Paragraph("<b>Mujeeb Ur Rahman</b> (ID: 6450)", table_cell), Paragraph("<b>90.5</b>", table_cell)],
        [Paragraph("<b>8</b>", table_cell), Paragraph("<b>Virat Kohli</b> (ID: 47)", table_cell), Paragraph("<b>88.2</b>", table_cell), Paragraph("<b>Rashid Khan</b> (ID: 4722)", table_cell), Paragraph("<b>89.9</b>", table_cell)],
        [Paragraph("<b>9</b>", table_cell), Paragraph("<b>Jos Buttler</b> (ID: 813)", table_cell), Paragraph("<b>87.6</b>", table_cell), Paragraph("<b>Shaheen Afridi</b> (ID: 6355)", table_cell), Paragraph("<b>89.2</b>", table_cell)],
        [Paragraph("<b>10</b>", table_cell), Paragraph("<b>Ruturaj Gaikwad</b> (ID: 6059)", table_cell), Paragraph("<b>86.9</b>", table_cell), Paragraph("<b>Shadab Khan</b> (ID: 4926)", table_cell), Paragraph("<b>88.5</b>", table_cell)],
    ]
    ttab = Table(top_data, colWidths=[0.6*inch, 2.6*inch, 0.8*inch, 2.7*inch, 0.8*inch])
    ttab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), rr_navy),
        ('BOX', (0,0), (-1,-1), 0.5, border_subtle),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(ttab)
    story.append(Spacer(1, 10))

    if os.path.exists("figures/fig5_top10_rankings.png"):
        story.append(Image("figures/fig5_top10_rankings.png", width=7.2*inch, height=2.4*inch))
        story.append(Paragraph("<i>Figure 4: Summary Radar Visualizations for Top 10 Batters and Bowlers across all 6 core evaluation dimensions.</i>", meta_style))
        story.append(Spacer(1, 12))

    story.append(PageBreak())

    # STEP 5
    story.append(Paragraph("Step 5: Rajasthan Royals 2027 Auction Playbook", h1_style))
    story.append(Paragraph(
        "Our analysis was built to be immediately actionable for Sanju Samson, Rahul Dravid, and the RR auction war room. "
        "Here is the strategic franchise translation:",
        body_style
    ))
    
    rr_strategy = (
        "<b>1. Solve the Death-Finishing Bottleneck:</b> Target Naman Dhir or Shashank Singh. Both deliver 26%+ boundary frequency "
        "in overs 17–20 with sub-28% dot-ball rates, providing the ideal acceleration partner for Riyan Parag and Shimron Hetmyer.<br/>"
        "<b>2. Middle-Overs Spin Denial:</b> Secure Mohammad Nawaz or Akeal Hosein. Their sub-7.00 pressure economy starves the opposition "
        "of momentum between overs 7 and 14.<br/>"
        "<b>3. Avoid Overpaying for Flat-Track Anchors:</b> Reallocate purse away from top-order batters who display negative ΔSR under pressure."
    )
    rr_table = Table([[Paragraph(rr_strategy, body_style)]], colWidths=[7.5*inch])
    rr_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FDF2F8")),
        ('LINELEFT', (0,0), (-1,-1), 4, rr_pink),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#FBCFE8")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(rr_table)
    story.append(Spacer(1, 10))

    # STEP 6
    story.append(Paragraph("Step 6: Engineering the 11-Module Interactive Analytics Platform", h1_style))
    story.append(Paragraph(
        "Rather than delivering only a static PDF, we engineered a complete franchise-grade analytics suite. "
        "Built in Python with Streamlit, Plotly, and custom Rajasthan Royals midnight-navy/pink CSS, it features:",
        body_style
    ))
    
    app_modules = [
        [Paragraph("Module", table_header), Paragraph("Key Features & Analytical Capability", table_header)],
        [Paragraph("<b>1. Batting Analytics</b>", table_cell), Paragraph("Top 10 spotlight trading cards, 85 qualified batters, RVA filters, boundary & dot-ball quadrants.", table_cell)],
        [Paragraph("<b>2. Bowling Analytics</b>", table_cell), Paragraph("Phase-Adjusted Economy Savings, death-overs containment share, 98 qualified bowlers.", table_cell)],
        [Paragraph("<b>3. Player Profiles</b>", table_cell), Paragraph("4-tab deep dossiers: 6-axis radar charts, situational splits, match-by-match logs, and RR scouting cards.", table_cell)],
        [Paragraph("<b>4. Player Comparison</b>", table_cell), Paragraph("Side-by-side radar overlays and head-to-head metrics comparing any 2 to 5 players.", table_cell)],
        [Paragraph("<b>5. Pressure Deep Dive</b>", table_cell), Paragraph("Win probability shifts, match leverage curve, and chase knife-edge simulator.", table_cell)],
        [Paragraph("<b>6. Clutch vs Regressors</b>", table_cell), Paragraph("The Anti-Rankings: 4-quadrant scatter isolating flat-track bullies from elite clutch performers.", table_cell)],
        [Paragraph("<b>7–10. Deep Exploration</b>", table_cell), Paragraph("Team Analytics, Granular Delivery Physics Explorer (207k balls), Download Center, and Data Validation.", table_cell)]
    ]
    mtab = Table(app_modules, colWidths=[2.2*inch, 5.3*inch])
    mtab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), rr_navy),
        ('BOX', (0,0), (-1,-1), 0.5, border_subtle),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(mtab)
    story.append(Spacer(1, 12))

    # Concluding Summary & Strategic Value
    story.append(Paragraph("Conclusion: From Analytical Intelligence to Championships", h1_style))
    conclusion_text = (
        "<b>Summary & Strategic Takeaways for the Rajasthan Royals:</b><br/>"
        "• <b>Contextual Objectivity:</b> Evaluated 207,678 deliveries across 883 matches to ensure rankings reflect empirical clutch performance rather than reputation.<br/>"
        "• <b>Phase-Par Fairness:</b> Solved the Formula 1 Paradox through Phase-Adjusted Economy Savings, ensuring high-stakes death bowlers are rewarded fairly.<br/>"
        "• <b>Targeted Recruitment for IPL 2027:</b> Identified elite uncapped accelerators (Naman Dhir, Shashank Singh) and multi-phase controllers (Mohammad Nawaz, Sunil Narine) to construct an unbreakable championship core alongside Sanju Samson and Riyan Parag.<br/>"
        "• <b>End-to-End Transparency:</b> Every metric, radar split, and match log is fully reproducible and explorable via our open-source Streamlit platform."
    )
    ctab = Table([[Paragraph(conclusion_text, body_style)]], colWidths=[7.5*inch])
    ctab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('LINELEFT', (0,0), (-1,-1), 4, rr_pink),
        ('BOX', (0,0), (-1,-1), 0.5, border_subtle),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(ctab)
    story.append(Spacer(1, 14))

    # Clean Footer Reference
    signoff_text = (
        "<b>Project Repository:</b> https://github.com/SaiPraneeth-E/RR-Hackathon &nbsp;&nbsp;•&nbsp;&nbsp; "
        "<b>Author:</b> E Sai Praneeth &nbsp;&nbsp;•&nbsp;&nbsp; "
        "<b>SupeRR Selector Season 2 Verified Submission</b>"
    )
    story.append(Paragraph(signoff_text, meta_style))

    # Build the document using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Also copy to alt_filename
    import shutil
    shutil.copyfile(pdf_filename, alt_filename)
    print(f"Successfully generated {pdf_filename} and {alt_filename}!")

if __name__ == "__main__":
    build_journey_pdf()

