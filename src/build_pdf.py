import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdf_filename = "METHODOLOGY_REPORT_FINAL.pdf"
doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    leftMargin=0.45 * inch,
    rightMargin=0.45 * inch,
    topMargin=0.45 * inch,
    bottomMargin=0.45 * inch
)

styles = getSampleStyleSheet()

primary_color = colors.HexColor("#1A5276")
secondary_color = colors.HexColor("#196F3D")
dark_neutral = colors.HexColor("#2C3E50")
light_bg = colors.HexColor("#F8F9F9")

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=16,
    leading=20,
    textColor=primary_color,
    alignment=1,
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=9,
    leading=12,
    textColor=colors.HexColor("#555555"),
    alignment=1,
    spaceAfter=8
)

h1_style = ParagraphStyle(
    'SectionH1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=15,
    textColor=primary_color,
    spaceBefore=10,
    spaceAfter=4
)

h2_style = ParagraphStyle(
    'SectionH2',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=12,
    textColor=dark_neutral,
    spaceBefore=6,
    spaceAfter=3
)

body_style = ParagraphStyle(
    'DocBody',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8,
    leading=11,
    textColor=colors.HexColor("#222222"),
    spaceAfter=5
)

table_header_style = ParagraphStyle(
    'TableHeader',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7,
    leading=8.5,
    textColor=colors.white,
    alignment=1
)

table_cell_style = ParagraphStyle(
    'TableCell',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7,
    leading=8.5,
    textColor=colors.HexColor("#111111"),
    alignment=1
)

table_cell_left = ParagraphStyle(
    'TableCellLeft',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7,
    leading=8.5,
    textColor=colors.HexColor("#111111"),
    alignment=0
)

caption_style = ParagraphStyle(
    'Caption',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=7,
    leading=8.5,
    textColor=colors.HexColor("#666666"),
    alignment=1,
    spaceAfter=6
)

story = []

# Title Banner
story.append(Paragraph("SupeRR Selector Season 2: Round 1 Challenge", title_style))
story.append(Paragraph("Identifying the Most Reliable Players Under Pressure in T20 Cricket", ParagraphStyle('Sub', parent=title_style, fontSize=13, leading=16, textColor=dark_neutral)))
story.append(Paragraph("Comprehensive Methodology Report & Top 10 Player Rankings | Corpus: 883 Matches, 200,999 Deliveries (2022–2026)", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceBefore=1, spaceAfter=6))

# 1. Executive Summary
story.append(Paragraph("1. Executive Summary: The Search for True Clutch Performers", h1_style))
story.append(Paragraph(
    "In high-stakes Twenty20 cricket, traditional career averages and overall strike rates often tell dangerous lies. A batter who scores "
    "an effortless 50 in a blowout looks great on paper. A bowler who feigns dominance by picking up lower-order wickets in the 8th over against an associate "
    "nation pads their career economy rate. But what happens when the game is on the line? When a team needs 42 off 18 balls with four wickets down? "
    "To solve Round 1 of the SupeRR Selector Season 2, we built the <b>Pressure Reliability Index (PRI)</b>—a delivery-level data science system "
    "evaluating 65,741 high-pressure deliveries across five years of IPL and T20I cricket. By measuring each player's execution against situational "
    "win-expectancy par and their own career baselines, PRI separates genuine match-winners from those whose performances dip under tension.",
    body_style
))

# Top 10 Batters Table
story.append(Paragraph("Official Top 10 Batters Under Pressure (Selected on Unstop)", h2_style))
bat_rows = [
    ["Rank", "Player Name", "Player ID", "Balls_P", "SR_P", "Base SR", "ΔSR", "Avg_P", "Dot %", "Bnd %", "Win Imp %", "Total RVA", "PRI Score"],
    ["1", "Naman Dhir", "37052", "229", "199.56", "168.71", "+30.86", "41.55", "27.9%", "30.1%", "78.9%", "+169.1", "100.00"],
    ["2", "Shashank Singh", "2756", "350", "180.29", "161.61", "+18.68", "45.07", "29.1%", "24.9%", "70.8%", "+184.6", "81.86"],
    ["3", "Rishabh Pant", "4703", "418", "170.10", "143.30", "+26.80", "30.91", "38.0%", "24.9%", "72.4%", "+145.6", "71.34"],
    ["4", "Suryakumar Yadav", "1699", "816", "177.70", "167.21", "+10.48", "36.25", "34.6%", "26.5%", "76.0%", "+410.2", "71.17"],
    ["5", "Tim David", "6396", "701", "191.87", "180.00", "+11.87", "32.02", "37.5%", "27.5%", "69.2%", "+343.9", "70.58"],
    ["6", "Ishan Kishan", "4117", "209", "174.64", "146.98", "+27.66", "28.08", "34.0%", "25.8%", "64.7%", "+74.7", "67.68"],
    ["7", "Dinesh Karthik", "143", "486", "184.36", "168.08", "+16.28", "28.00", "35.4%", "28.0%", "61.9%", "+170.3", "66.64"],
    ["8", "Virat Kohli", "47", "275", "171.64", "145.35", "+26.28", "36.31", "27.6%", "21.5%", "61.1%", "+90.0", "66.48"],
    ["9", "Jos Buttler", "813", "363", "182.37", "155.89", "+26.48", "26.48", "29.8%", "25.6%", "63.3%", "+145.1", "66.17"],
    ["10", "Ruturaj Gaikwad", "6059", "202", "173.76", "139.64", "+34.13", "27.00", "33.2%", "23.8%", "66.7%", "+61.7", "65.73"]
]

flow_bat = []
for i, r in enumerate(bat_rows):
    row_f = []
    for j, val in enumerate(r):
        if i == 0:
            row_f.append(Paragraph(val, table_header_style))
        else:
            style = table_cell_left if j == 1 else table_cell_style
            row_f.append(Paragraph(val, style))
    flow_bat.append(row_f)

t_bat = Table(flow_bat, colWidths=[24, 82, 38, 34, 38, 38, 36, 34, 34, 34, 42, 44, 42])
t_bat.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), primary_color),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ('TOPPADDING', (0,0), (-1,-1), 1.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D5D8DC"))
]))
story.append(t_bat)
story.append(Spacer(1, 4))

# Top 10 Bowlers Table
story.append(Paragraph("Official Top 10 Bowlers Under Pressure (Selected on Unstop)", h2_style))
bowl_rows = [
    ["Rank", "Player Name", "Player ID", "Balls_P", "Econ_P", "Exp Econ", "Phase ΔEcon", "SR_P", "Death %", "Dot %", "Win Imp %", "Total BVA", "PRI Score"],
    ["1", "Mohammad Nawaz", "2490", "262", "5.66", "7.73", "+2.07", "10.48", "16.8%", "42.4%", "76.0%", "+151.3", "100.00"],
    ["2", "Abrar Ahmed", "5979", "227", "6.00", "8.48", "+2.48", "12.61", "41.0%", "50.2%", "65.2%", "+119.6", "97.02"],
    ["3", "Sunil Narine", "781", "480", "6.23", "8.42", "+2.19", "15.48", "39.0%", "39.0%", "77.3%", "+212.0", "90.05"],
    ["4", "Akeal Hosein", "2417", "234", "6.79", "8.40", "+1.61", "14.62", "30.8%", "37.6%", "76.9%", "+77.2", "81.14"],
    ["5", "Mitchell Santner", "4101", "581", "6.84", "8.37", "+1.54", "15.70", "28.2%", "38.7%", "70.6%", "+176.9", "79.61"],
    ["6", "Jasprit Bumrah", "2933", "652", "7.32", "9.31", "+1.99", "14.82", "73.9%", "37.7%", "68.9%", "+248.2", "79.12"],
    ["7", "Mujeeb Ur Rahman", "6450", "209", "6.72", "8.30", "+1.58", "14.93", "34.4%", "41.1%", "75.0%", "+64.4", "79.05"],
    ["8", "Rashid Khan", "4722", "1036", "7.23", "8.39", "+1.16", "13.11", "43.9%", "39.4%", "68.5%", "+263.7", "76.11"],
    ["9", "Shaheen Afridi", "6355", "302", "8.11", "9.76", "+1.65", "10.41", "79.1%", "38.7%", "68.6%", "+117.6", "75.70"],
    ["10", "Shadab Khan", "4926", "273", "7.05", "8.12", "+1.07", "13.65", "20.9%", "36.3%", "66.7%", "+72.9", "72.76"]
]

flow_bowl = []
for i, r in enumerate(bowl_rows):
    row_f = []
    for j, val in enumerate(r):
        if i == 0:
            row_f.append(Paragraph(val, table_header_style))
        else:
            style = table_cell_left if j == 1 else table_cell_style
            row_f.append(Paragraph(val, style))
    flow_bowl.append(row_f)

t_bowl = Table(flow_bowl, colWidths=[24, 78, 36, 32, 32, 38, 42, 32, 36, 32, 40, 44, 42])
t_bowl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), secondary_color),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ('TOPPADDING', (0,0), (-1,-1), 1.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D5D8DC"))
]))
story.append(t_bowl)
story.append(Spacer(1, 6))

if os.path.exists("figures/fig5_top10_rankings.png"):
    story.append(Image("figures/fig5_top10_rankings.png", width=7.2*inch, height=3.0*inch))
    story.append(Paragraph("Figure 1: Official Top 10 Batters and Bowlers Under Pressure (PRI Score Comparison)", caption_style))

# 2. What Counts as Pressure?
story.append(Paragraph("2. What Counts as Pressure? The Human and Mathematical Reality", h1_style))
story.append(Paragraph(
    "Cricket pressure is driven by win expectancy swings and temporal urgency. Our Four-Pillar Pressure Framework defines:<br/>"
    "• <b>Pillar 1 (The Chase)</b>: Overs 15–20 with RRR between 6.0 and 22.0, target <= 80 runs, and wickets in hand <= 8; plus middle-overs climbs "
    "(overs 7–14, RRR >= 10.0, wickets <= 7). Coasting chases (RRR < 5 with 8+ wickets) and hopeless blowouts (RRR > 24) are filtered out.<br/>"
    "• <b>Pillar 2 (Setting Targets)</b>: Overs 16–20 (Death Overs) where league par scoring leaps to 10.56 rpo, and early top-order collapses (loss of >= 3 wickets inside overs 1–10).<br/>"
    "• <b>Pillar 3 (Super Overs)</b>: All deliveries in innings 3 and 4 (100% clutch).<br/>"
    "• <b>Pillar 4 (Stakes Multipliers)</b>: 1.25x for playoff/knockout fixtures; 1.15x for IPL matches.",
    body_style
))

if os.path.exists("figures/fig3_macro_validation.png"):
    story.append(Image("figures/fig3_macro_validation.png", width=7.2*inch, height=2.0*inch))
    story.append(Paragraph("Figure 2: Empirical Macro Validation: High Pressure vs Ordinary Situations (N = 200,999 Balls)", caption_style))

if os.path.exists("figures/fig6_over_pressure_curve.png"):
    story.append(Image("figures/fig6_over_pressure_curve.png", width=7.0*inch, height=3.2*inch))
    story.append(Paragraph("Figure 3: The 20-Over Pressure Escalation Curve: Run Rate & Wicket Mortality Escalation by Over", caption_style))

if os.path.exists("figures/fig4_win_probability_matrix.png"):
    story.append(Image("figures/fig4_win_probability_matrix.png", width=4.8*inch, height=3.2*inch))
    story.append(Paragraph("Figure 4: Empirical Chase Win Probability in Death Overs (RRR vs Wickets in Hand Knife-Edge)", caption_style))

# 3. How Performance is Measured
story.append(Paragraph("3. Performance Measurement: Leveling the Playing Field", h1_style))
story.append(Paragraph(
    "<b>The Formula 1 Analogy (Solving Phase Confounding):</b><br/>"
    "Imagine judging a driver's speed in school traffic (20 mph limit) versus on an open F1 track. Standard bowling economy commits this exact error! "
    "League death economy is 9.55–11.5 rpo. The 8th over is a school zone (7.43 rpo). If Jasprit Bumrah bowls overs 18 and 20 at 7.32 rpo, he is saving "
    "nearly 2 full runs every over (+1.99 Phase ΔEcon) compared to par! Our Phase-Adjusted metric levels the playing field so death bowlers are evaluated fairly against the exact difficulty of the overs they bowled.<br/><br/>"
    "<b>The 'Bonus Runs' System (RVA & BVA):</b><br/>"
    "Every delivery has an expected price tag. If an average batter in the 18th over scores 1.55 runs, and Tim David hits a six, he banks +4.45 Run Value Added (RVA). "
    "A dismissal costs 3.5 runs in lost equity. For bowlers, bowling a dot in a death chase banks +1.55 BVA; a dot plus a wicket banks +5.05 BVA. "
    "Summing these profits gives Total RVA and Total BVA.",
    body_style
))

if os.path.exists("figures/fig1_batting_pressure_landscape.png"):
    story.append(Image("figures/fig1_batting_pressure_landscape.png", width=6.8*inch, height=4.0*inch))
    story.append(Paragraph("Figure 5: Batting Pressure Landscape: High-Pressure SR vs Baseline Parity (Top-Right = Accelerators)", caption_style))

if os.path.exists("figures/fig2_bowling_containment.png"):
    story.append(Image("figures/fig2_bowling_containment.png", width=6.8*inch, height=4.0*inch))
    story.append(Paragraph("Figure 6: Bowling Run Suppression: Phase-Adjusted Economy Savings vs Wicket Strike Rate", caption_style))

# 4. Humanizing Stories & Deep Dives
story.append(Paragraph("4. Humanizing the Top 10: Stories of Nerves, Skill, and Ice", h1_style))
story.append(Paragraph(
    "<b>Batting Highlights:</b><br/>"
    "• <b>Naman Dhir (#1 Batter | PRI: 100.00)</b>: Dhir attacks from ball one, producing an astonishing 199.56 pressure strike rate (+30.86 ΔSR) and winning 78.9% of his match battles.<br/>"
    "• <b>Shashank Singh (#2 Batter | PRI: 81.86)</b>: Punjab's ice-cool crisis merchant. In impossible chases, Shashank averaged 45.07 at a 180.29 SR, combining clinical boundary targeting with zero panic.<br/>"
    "• <b>Suryakumar Yadav (#4 Batter | PRI: 71.17)</b>: Facing an unmatched 816 pressure balls, SKY amassed +410.2 Total RVA (highest in cricket) with a 76.0% win impact rate, scooping 145 km/h yorkers over fine leg while falling on one knee.<br/>"
    "• <b>Tim David (#5 Batter | PRI: 70.58)</b>: Striking at 191.87 under pressure across 701 balls (+343.9 RVA), David is modern cricket's most fearsome death-overs finisher.<br/><br/>"
    "<b>Bowling Highlights:</b><br/>"
    "• <b>Mohammad Nawaz (#1 Bowler | PRI: 100.00) & Abrar Ahmed (#2 Bowler | PRI: 97.02)</b>: Pakistan's suffocating spin duo. Nawaz conceded just 5.66 rpo (+2.07 runs saved/over), while Abrar delivered an astounding 50.2% dot ball rate under pressure (+2.48 Phase ΔEcon).<br/>"
    "• <b>Sunil Narine (#3 Bowler | PRI: 90.05)</b>: The emotionless assassin. In 480 clutch IPL balls, Narine conceded barely 6.23 rpo (+2.19 Phase ΔEcon) and won his matchup in 77.3% of matches.<br/>"
    "• <b>Jasprit Bumrah (#6 Bowler | PRI: 79.12)</b>: The greatest death bowler alive. 73.9% of his pressure deliveries were bowled in overs 16–20. Bumrah conceded only 7.32 rpo against a death par of 9.31 (+1.99 runs saved/over) with +248.2 Total BVA.",
    body_style
))

# 5. The Other Side of the Coin: Who Chokes?
story.append(Paragraph("5. The Other Side of the Coin: Who Chokes Under Pressure?", h1_style))
story.append(Paragraph(
    "The data clearly identifies players who retreat into a shell or blow out when the heat rises:<br/>"
    "• <b>Batters Who Stall (Negative ΔSR)</b>: Curtis Campher (SR drops to 115.61, -5.04 ΔSR, -46.3 RVA), Washington Sundar (SR drops to 136.73, -3.80 ΔSR, -50.8 RVA), Deepak Hooda (SR 130.71, -2.87 ΔSR), Jimmy Neesham (SR 132.46, -2.78 ΔSR), and Wanindu Hasaranga (pressure average collapses to 9.17, -137.9 RVA).<br/>"
    "• <b>Bowlers Who Bleed Runs (Negative Phase ΔEcon)</b>: Andre Russell (concedes 11.69 rpo under pressure, -2.29 Phase ΔEcon, -128.8 BVA), Nitish Reddy (10.52 rpo, -1.60 Phase ΔEcon), Tushar Deshpande (11.43 rpo, -1.39 Phase ΔEcon, -87.8 BVA), and Mukesh Kumar (11.15 rpo, -1.33 Phase ΔEcon, -135.9 BVA).",
    body_style
))

if os.path.exists("figures/fig7_rise_vs_dip.png"):
    story.append(Image("figures/fig7_rise_vs_dip.png", width=6.8*inch, height=3.2*inch))
    story.append(Paragraph("Figure 7: The Psychological Divide: Comparing Clutch Risers (Accelerators) vs Pressure Regressors (Stallers)", caption_style))

# 6. Strategic Recommendations
story.append(Paragraph("6. Strategic Recommendations for Rajasthan Royals", h1_style))
story.append(Paragraph(
    "1. <b>Target Undervalued Clutch Gems</b>: Naman Dhir and Shashank Singh provide world-class clutch execution at a fraction of superstar auction costs.<br/>"
    "2. <b>Protect High-Variance Bowlers</b>: Bowlers who blow out at the death (Russell, Deshpande, Mukesh) must be front-loaded in overs 1–14; overs 17–20 must be reserved exclusively for elite run suppressors (Bumrah, Shaheen, Narine).<br/>"
    "3. <b>Pair Composure with Explosion</b>: In tight chases, pairing an anchor who cuts dot balls (Kohli, Gaikwad) with an explosive boundary striker (David, Shashank) maximizes win expectancy by preventing both collapses and rate asphyxiation.",
    body_style
))

doc.build(story)
print("METHODOLOGY_REPORT_FINAL.pdf successfully generated and saved!")
