# SupeRR Selector Season 2: Share Your Journey & Video Script
### Optional 30–60 Second Video Script & Process Narrative

> *"Some players thrive when the game is on the line. Others struggle to deliver. Here is the story of how data separated the true match-winners from the flat-track bullies."*

---

## 1. 60-Second Video Script (Word-for-Word)

**Target Duration**: 45–60 Seconds  
**Tone**: Confident, passionate, analytical, humanized  
**Visual Setting**: Talking to camera with the interactive **SupeRR Selector Dashboard** or **Figure 2 / Figure 7** on the screen behind or beside you.

---

### [0:00 – 0:10] The Hook
*(Looking directly into the camera with enthusiasm)*  
> "When Rajasthan Royals launched the SupeRR Selector challenge, our team asked one fundamental question: **Can data distinguish a player who thrives under tension from one who looks great only when there's zero pressure?**"

### [0:10 – 0:25] The Core Approach & The "Aha!" Moment
*(Cut to or point at the screen showing the 4-Pillar Pressure Framework / Match Leverage Curve)*  
> "We analyzed over 200,000 deliveries across four years of IPL and T20Is using a 4-pillar pressure engine. But our biggest breakthrough was what we call the **'Formula 1 Paradox'**.  
> Bowling over 19 is like driving an F1 car at 300 km/h where par economy is 10.6. Bowling over 8 is driving in a school zone at 7.4. If you evaluate Jasprit Bumrah on raw economy, you miss the magic. He saves **two full runs per over against death-over expectations!**"

### [0:25 – 0:45] The Surprising Findings
*(Point to the Clutch vs Regressors Quadrant / Naman Dhir & Shashank Singh)*  
> "That insight unlocked everything. It revealed why uncapped finishers like **Naman Dhir** and **Shashank Singh** had higher pressure acceleration than traditional superstars—they hit boundaries without stalling dot balls. And it exposed who dips when stakes peak."

### [0:45 – 0:60] The Conclusion & Sign-Off
*(Smile, looking back at the camera)*  
> "We built an end-to-end interactive analytics platform to explore every delivery, every match log, and every pressure split. This isn't just theory—it's franchise Moneyball for winning championships.  
> Thank you, Rajasthan Royals, for an incredible challenge. Halla Bol!"

---

## 2. Behind the Scenes: The Process Story

### Phase 1: Rejecting "One-Size-Fits-All" Pressure
Many public models define pressure arbitrarily (e.g. only overs 16–20 or only run chases). We realized that pressure is multidimensional:
- **Over Leverage**: The math of death overs forces batters to hit out and bowlers to execute yorkers under severe margin for error.
- **Chase Knife-Edge**: A required run rate escalating above 9.0 RPO creates compounding tension where every dot ball increases the wicket hazard rate by 42%.
- **Wicket Mortality**: A batter facing their first 6 balls during a top-order collapse faces intense existential tension.
- **Match Stakes**: Knockouts, playoffs, and World Cups carry disproportionate consequence.

### Phase 2: Solving Phase Confounding (The True Game Changer)
In raw statistics:
- Spinners bowling middle overs had lower economy than elite pacers bowling death overs.
- To solve this, we engineered **Phase-Adjusted Economy Savings ($\text{Phase }\Delta\text{Econ}$)**.
- Each delivery was benchmarked against the situational expectation $\mathbb{E}[\text{Runs} \mid \text{Phase}, \text{Innings}, \text{Wickets Lost}]$.
- Suddenly, Jasprit Bumrah, Sunil Narine, and Mohammad Nawaz surged to the top of the leaderboard because of how many runs they saved *relative to contextual par*.

### Phase 3: Bringing the Data to Life
We didn't want this to live only in code or a static report. We built:
1. A **5-page publication-quality Methodology Report** (PDF and Word).
2. A full **Streamlit Cricket Analytics Dashboard** with 11 interactive modules, 6-axis radar charts, multi-player comparison, and granular delivery physics.
3. An offline-ready **HTML Analytics Hub**.

---

## 3. Recommended Screenshots to Share

If you wish to upload photographs or screenshots alongside your submission, the following 4 files from the `figures/` folder provide the strongest visual impact:

1. **`figures/fig5_top10_rankings.png`**: The complete summary of Top 10 Batters and Top 10 Bowlers with PRI scores and radar charts.
2. **`figures/fig2_bowling_containment.png`**: The Phase-Adjusted Economy Savings chart illustrating the Formula 1 paradox.
3. **`figures/fig6_over_pressure_curve.png`**: The 20-over match leverage curve showing pressure escalation.
4. **`figures/fig7_rise_vs_dip.png`**: The 4-quadrant scatter plot separating elite accelerators from regressors.
