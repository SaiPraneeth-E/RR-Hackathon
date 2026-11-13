import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

doc = Document()

# Set page margins
sections = doc.sections
for section in sections:
    section.top_margin = Inches(0.65)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.65)
    section.right_margin = Inches(0.65)

# Styling helper functions
def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_custom_heading(text, level=1):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    r = h.add_run(text)
    r.font.name = "Arial"
    r.font.bold = True
    if level == 1:
        r.font.size = Pt(14)
        r.font.color.rgb = RGBColor(26, 82, 118) # Dark Navy
    elif level == 2:
        r.font.size = Pt(11.5)
        r.font.color.rgb = RGBColor(39, 110, 144)
    else:
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(44, 62, 80)
    return h

def add_body_paragraph(text, italic=False, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(9.5)
        r_pre.font.bold = True
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(9.5)
    r.font.italic = italic
    r.font.color.rgb = RGBColor(34, 34, 34)
    return p

def add_caption(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(8.5)
    r.font.italic = True
    r.font.color.rgb = RGBColor(100, 100, 100)

# Title & Meta
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(2)
run_title = p_title.add_run("SupeRR Selector Season 2: Round 1 Challenge\nIdentifying the Most Reliable Players Under Pressure in T20 Cricket")
run_title.font.name = "Arial"
run_title.font.size = Pt(17)
run_title.font.bold = True
run_title.font.color.rgb = RGBColor(26, 82, 118)

p_meta = doc.add_paragraph()
p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_meta.paragraph_format.space_after = Pt(12)
run_meta = p_meta.add_run("Comprehensive Data-Driven Methodology Report & Top 10 Player Rankings\nCorpus: 883 Matches | 200,999 Deliveries | IPL & T20 Internationals (2022–2026)")
run_meta.font.name = "Arial"
run_meta.font.size = Pt(9.5)
run_meta.font.italic = True
run_meta.font.color.rgb = RGBColor(85, 85, 85)

# 1. Executive Summary
add_custom_heading("1. Executive Summary: The Search for True Clutch Performers", level=1)
add_body_paragraph(
    "In high-stakes Twenty20 cricket, traditional career averages and overall strike rates often tell dangerous lies. A batter who scores "
    "an effortless 50 in a blowout when the match is already decided looks great on paper. A bowler who feigns dominance by picking up lower-order "
    "wickets in the 8th over against an associate nation pads their career economy rate. But what happens when the game is on the line? When a team "
    "needs 42 off 18 balls with four wickets down? Or when a bowler must defend 11 in the 20th over against elite power-hitters?"
)
add_body_paragraph(
    "To solve Round 1 of the SupeRR Selector Season 2, we built the Pressure Reliability Index (PRI)—a delivery-level data science system "
    "evaluating 65,741 high-pressure deliveries across five years of IPL and T20I cricket. By measuring each player's execution against situational "
    "win-expectancy par and their own career baselines, PRI separates genuine match-winners from those whose performances dip under tension."
)

# Top 10 Batters Table
add_custom_heading("Official Top 10 Batters Under Pressure (Selected on Unstop)", level=2)
bat_data = [
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

table_bat = doc.add_table(rows=len(bat_data), cols=len(bat_data[0]))
table_bat.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, row in enumerate(bat_data):
    for j, val in enumerate(row):
        cell = table_bat.cell(i, j)
        cell.text = str(val)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j != 1 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.runs[0]
        r.font.name = "Arial"
        r.font.size = Pt(8)
        if i == 0:
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            set_cell_background(cell, "1A5276")
        else:
            if i % 2 == 1:
                set_cell_background(cell, "F2F4F4")
            if j in [0, 1]:
                r.font.bold = True
            if j == 6 and "+" in str(val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(25, 111, 61)
        set_cell_margins(cell, top=50, bottom=50, left=50, right=50)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Top 10 Bowlers Table
add_custom_heading("Official Top 10 Bowlers Under Pressure (Selected on Unstop)", level=2)
bowl_data = [
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

table_bowl = doc.add_table(rows=len(bowl_data), cols=len(bowl_data[0]))
table_bowl.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, row in enumerate(bowl_data):
    for j, val in enumerate(row):
        cell = table_bowl.cell(i, j)
        cell.text = str(val)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j != 1 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.runs[0]
        r.font.name = "Arial"
        r.font.size = Pt(8)
        if i == 0:
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            set_cell_background(cell, "196F3D")
        else:
            if i % 2 == 1:
                set_cell_background(cell, "F2F4F4")
            if j in [0, 1]:
                r.font.bold = True
            if j == 6 and "+" in str(val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(25, 111, 61)
        set_cell_margins(cell, top=50, bottom=50, left=40, right=40)

doc.add_paragraph().paragraph_format.space_after = Pt(10)

if os.path.exists("figures/fig5_top10_rankings.png"):
    doc.add_picture("figures/fig5_top10_rankings.png", width=Inches(6.8))
    add_caption("Figure 1: Official Top 10 Batters and Top 10 Bowlers Under Pressure (PRI Score Comparison)")

# 2. What Counts as Pressure?
add_custom_heading("2. What Counts as Pressure? The Human and Mathematical Reality", level=1)
add_body_paragraph(
    "Ask any international cricketer what pressure feels like, and they will describe two distinct psychological states:\n"
    "1. The Chaser's Dilemma (Innings 2): The scoreboard is ticking down like a time bomb. Every dot ball feels like an explosion. "
    "When the required run rate climbs above 11 an over, a single boundary changes the entire mood of the stadium, while a wicket brings cold despair.\n"
    "2. The Defender's Burden (Innings 1 & Death Bowling): The batter has nothing to lose and is swinging at everything. The bowler knows a millimeter "
    "of error results in a six over third man or extra cover. In the 19th over, bowling a dot ball is the hardest feat in world sport."
)
add_body_paragraph(
    "Our model translates these exact human realities into a Four-Pillar Pressure Framework:\n"
    "• Pillar 1 (Critical Chase): Overs 15–20 with RRR between 6.0 and 22.0, target <= 80 runs, and wickets in hand <= 8; plus middle-overs climbs "
    "(overs 7–14, RRR >= 10.0, wickets <= 7). Coasting chases (RRR < 5 with 8+ wickets) and hopeless blowouts (RRR > 24 with tailenders) are filtered out.\n"
    "• Pillar 2 (Setting Targets): Overs 16–20 (Death Overs) where par run rate leaps to 10.56 rpo, and early top-order collapses (loss of >= 3 wickets inside overs 1–10).\n"
    "• Pillar 3 (Super Overs): All deliveries in innings 3 and 4 (100% clutch).\n"
    "• Pillar 4 (Stakes Multipliers): 1.25x for playoff/knockout fixtures; 1.15x for IPL matches."
)

if os.path.exists("figures/fig3_macro_validation.png"):
    doc.add_picture("figures/fig3_macro_validation.png", width=Inches(6.8))
    add_caption("Figure 2: Empirical Macro Validation: High Pressure vs Ordinary Situations (N = 200,999 Balls)")

if os.path.exists("figures/fig6_over_pressure_curve.png"):
    doc.add_picture("figures/fig6_over_pressure_curve.png", width=Inches(6.8))
    add_caption("Figure 3: The 20-Over Pressure Escalation Curve: Run Rate & Wicket Mortality Escalation by Over")

if os.path.exists("figures/fig4_win_probability_matrix.png"):
    doc.add_picture("figures/fig4_win_probability_matrix.png", width=Inches(5.2))
    add_caption("Figure 4: Empirical Chase Win Probability in Death Overs (RRR vs Wickets in Hand Knife-Edge)")

# 3. How Performance is Measured
add_custom_heading("3. Performance Measurement: Leveling the Playing Field", level=1)
add_body_paragraph(
    "Why can't you just look at a bowler's career economy rate to judge their pressure skill?",
    bold_prefix="The Formula 1 Analogy: "
)
add_body_paragraph(
    "Imagine comparing two drivers. Driver A drives in heavy school traffic with a 20 mph speed limit. Driver B drives on an open Formula 1 track. "
    "If Driver A averages 18 mph and Driver B averages 60 mph, does that mean Driver A is a better driver? Of course not! In cricket, the 19th over is a "
    "Formula 1 track. League death economy is 9.55 to 11.5 rpo. The 8th over is a school zone (7.43 rpo). If Jasprit Bumrah bowls overs 18 and 20 at "
    "7.32 rpo, he is saving nearly 2 full runs every over (+1.99 Phase ΔEcon) compared to par! Our Phase-Adjusted metric levels the playing field so "
    "death-overs gladiators are evaluated fairly against the exact difficulty of the overs they bowled."
)
add_body_paragraph(
    "Instead of counting raw runs, we evaluate every single ball against historical expectations. If an average batter in the 18th over scores 1.55 runs, "
    "and Tim David hits a six, he banks +4.45 Run Value Added (RVA). If a batter gets out, that dismissal costs their team roughly 3.5 runs in lost equity. "
    "Similarly, if Sunil Narine bowls a dot ball in a death chase, he banks +1.55 Bowling Value Added (BVA). Summing these delivery-level profits over "
    "five years gives Total RVA and Total BVA—the true net runs a player contributed above replacement.",
    bold_prefix="The 'Bonus Runs' System: "
)

if os.path.exists("figures/fig1_batting_pressure_landscape.png"):
    doc.add_picture("figures/fig1_batting_pressure_landscape.png", width=Inches(6.8))
    add_caption("Figure 5: Batting Pressure Landscape: High-Pressure SR vs Career Baseline Parity (Top-Right = Accelerators)")

if os.path.exists("figures/fig2_bowling_containment.png"):
    doc.add_picture("figures/fig2_bowling_containment.png", width=Inches(6.8))
    add_caption("Figure 6: Bowling Run Suppression: Phase-Adjusted Economy Savings vs Wicket Strike Rate")

# 4. Humanizing Stories & Deep Dives
add_custom_heading("4. Humanizing the Top 10: Stories of Nerves, Skill, and Ice", level=1)
add_body_paragraph(
    "• Naman Dhir (#1 Batter | PRI: 100.00): Dhir does not wait to 'get his eye in.' While other batters take 6–8 balls to adjust, Dhir attacks from ball one, "
    "producing an astonishing 199.56 pressure strike rate (+30.86 ΔSR) and winning 78.9% of his match battles.\n"
    "• Shashank Singh (#2 Batter | PRI: 81.86): Punjab Kings' unflappable crisis merchant. In impossible chases, Shashank averaged 45.07 at a 180.29 SR, "
    "combining ice-cool shot selection with ruthless boundary targeting.\n"
    "• Suryakumar Yadav (#4 Batter | PRI: 71.17): The volume colossus of T20 cricket. Facing an unmatched 816 pressure balls, SKY amassed +410.2 Total RVA "
    "(highest in cricket) with a 76.0% win impact rate, scooping 145 km/h yorkers over fine leg while falling on one knee.\n"
    "• Tim David (#5 Batter | PRI: 70.58): Modern cricket's most fearsome closer, striking at 191.87 under pressure across 701 balls (+343.9 RVA).\n"
    "• Mohammad Nawaz (#1 Bowler | PRI: 100.00) & Abrar Ahmed (#2 Bowler | PRI: 97.02): Pakistan's suffocating spin duo. Nawaz conceded just 5.66 rpo "
    "(+2.07 runs saved/over), while Abrar delivered an astounding 50.2% dot ball rate under pressure (+2.48 Phase ΔEcon).\n"
    "• Sunil Narine (#3 Bowler | PRI: 90.05): The emotionless assassin. In 480 clutch IPL balls against elite hitters, Narine conceded barely 6.23 rpo "
    "(+2.19 Phase ΔEcon) and won his individual matchup in 77.3% of matches.\n"
    "• Jasprit Bumrah (#6 Bowler | PRI: 79.12): The greatest death bowler alive. 73.9% of his pressure deliveries were bowled in overs 16–20. Where death par "
    "is 9.31–11.5 rpo, Bumrah conceded only 7.32 rpo (+1.99 runs saved/over) with +248.2 Total BVA."
)

# 5. The Other Side of the Coin: Who Chokes?
add_custom_heading("5. The Other Side of the Coin: Who Chokes Under Pressure?", level=1)
add_body_paragraph(
    "To prove our system is balanced, the data clearly identifies players who retreat into a shell or blow out when the heat rises:\n\n"
    "• Batters Who Stall (Negative ΔSR): Curtis Campher (SR drops to 115.61, -5.04 ΔSR, -46.3 RVA), Washington Sundar (SR drops to 136.73, -3.80 ΔSR, "
    "-50.8 RVA), Deepak Hooda (SR 130.71, -2.87 ΔSR), Jimmy Neesham (SR 132.46, -2.78 ΔSR), and Wanindu Hasaranga (pressure average collapses to 9.17, -137.9 RVA).\n"
    "• Bowlers Who Bleed Runs (Negative Phase ΔEcon): Andre Russell (concedes 11.69 rpo under pressure, -2.29 Phase ΔEcon, -128.8 BVA), Nitish Reddy (10.52 rpo, "
    "-1.60 Phase ΔEcon), Tushar Deshpande (11.43 rpo, -1.39 Phase ΔEcon, -87.8 BVA), and Mukesh Kumar (11.15 rpo, -1.33 Phase ΔEcon, -135.9 BVA)."
)

if os.path.exists("figures/fig7_rise_vs_dip.png"):
    doc.add_picture("figures/fig7_rise_vs_dip.png", width=Inches(6.8))
    add_caption("Figure 7: The Psychological Divide: Comparing Clutch Risers (Accelerators) vs Pressure Regressors (Stallers)")

# 6. Strategic Takeaways
add_custom_heading("6. Strategic Recommendations for Rajasthan Royals", level=1)
add_body_paragraph(
    "1. Target Undervalued Clutch Gems: Naman Dhir and Shashank Singh provide world-class clutch execution at a fraction of superstar auction costs.\n"
    "2. Protect High-Variance Bowlers: Bowlers who blow out at the death (Russell, Deshpande, Mukesh) must be front-loaded in overs 1–14; overs 17–20 "
    "must be reserved exclusively for elite run suppressors (Bumrah, Shaheen, Narine).\n"
    "3. Pair Composure with Explosion: In tight chases, pairing an anchor who cuts dot balls (Kohli, Gaikwad) with an explosive boundary striker "
    "(David, Shashank) maximizes win expectancy by preventing both collapses and rate asphyxiation."
)

doc.save("METHODOLOGY_REPORT_FINAL.docx")
print("METHODOLOGY_REPORT_FINAL.docx successfully updated and saved!")
