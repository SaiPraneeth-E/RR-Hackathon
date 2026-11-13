---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #0B132B
color: #F8FAFC
style: |
  section {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    padding: 40px;
  }
  h1, h2 {
    color: #FFFFFF;
  }
  h3 {
    color: #E91E63;
  }
  strong {
    color: #38BDF8;
  }
  .highlight-gold {
    color: #F59E0B;
  }
  .highlight-pink {
    color: #E91E63;
  }
  table {
    font-size: 15px;
    border-collapse: collapse;
    width: 100%;
    margin-top: 15px;
  }
  th {
    background-color: #1E293B;
    color: #38BDF8;
    padding: 8px 12px;
    border: 1px solid rgba(255,255,255,0.1);
  }
  td {
    padding: 8px 12px;
    border: 1px solid rgba(255,255,255,0.06);
    background-color: rgba(30, 41, 59, 0.4);
  }
---

# 🏏 SUPERR SELECTOR
### The Science of Performing Under Pressure in T20 Cricket
**Rajasthan Royals SupeRR Selector Season 2 — Round 1 Challenge**

*Edupulapati Sai Praneeth | Complete Analytics & Engineering Solution*

---

## 🎯 The Core Problem: The Pressure Paradox

*Some players thrive when the game is on the line. Others look dominant only when there is zero pressure.*

### The Core Challenge
- Can data distinguish true match-winners who consistently rise to the occasion from those whose performances dip under tension?
- How do we define pressure objectively across both batting and bowling?
- How do we eliminate **phase bias** (e.g. death overs vs middle overs)?

### Our Moneyball Philosophy
> **"Performance under pressure is not raw accumulation. It is the ability to outperform contextual expectations when the stakes peak."**

---

## 🏛️ The 4-Pillar Pressure Framework

We evaluated **200,999 deliveries across 883 matches (2022–2026)** using 4 mathematical conditions:

1. **Pillar 1: Over Leverage (Death Overs 16–20)**
   - Tournament par economy jumps to **10.56 RPO**; margin for error contracts to millimeters.
   - Represents **46.2%** of all high-pressure deliveries.
2. **Pillar 2: Chase Knife-Edge (RRR & Wickets)**
   - Activated when Required Run Rate $> 9.0$ RPO or wickets in hand fall below 5.
   - Compounding tension where every dot ball increases wicket hazard.
3. **Pillar 3: Wicket Mortality (First 6 Balls Crisis)**
   - Wicket mortality is **3.1x higher** during a batter's first 6 balls at the crease.
4. **Pillar 4: Match Stakes (Knockout Multiplier)**
   - A **1.25x context multiplier** for playoffs, finals, and ICC tournament eliminations.

---

## 📊 Macro Validation: Does the Model Separate Pressure?

Across 200,999 balls, high-pressure deliveries exhibit fundamentally distinct physical dynamics:

| Metric | High Pressure | Ordinary Play | Differential (Δ) | Statistical Impact |
|:---|:---:|:---:|:---:|:---|
| **Scoring Rate** | **8.84 RPO** | 7.82 RPO | **+13.0%** | Batsmen forced to attack |
| **Wicket Frequency** | **1 in 13.9 balls** | 1 in 19.8 balls | **+42.4% Hazard** | Extreme mortality spike |
| **Boundary %** | **16.7%** | 14.2% | **+17.6%** | Elevated aggression |
| **Dot Ball %** | **34.8%** | 37.1% | **-6.2%** | High rotational urgency |

> **Conclusion**: The model captures genuine high-stress environments rather than arbitrary match subsets.

---

## 🏎️ The Breakthrough: The "Formula 1 vs School Zone" Paradox

### Why Traditional Economy Fails
- A raw economy of 8.00 in the Powerplay is poor (par: ~7.4 RPO).
- A raw economy of 8.00 at the Death is world-class (par: 10.56 RPO).

### Jasprit Bumrah's True Impact
- Bumrah's raw pressure economy is 7.32 RPO.
- **68.2% of his pressure deliveries occur in overs 16–20.**
- Against the death-overs par of 10.56, Bumrah saves **+1.99 runs per over vs par**!

$$\text{Phase }\Delta\text{Econ} = \frac{\sum \mathbb{E}[\text{Runs}_i] - \sum \text{Runs}_i}{\text{Balls}_p / 6}$$

---

## 🏏 Official Top 10 Batters Under Pressure (Selected on Unstop)

| Rank | Player Name | ID | PRI | Press SR | Base SR | Δ SR | Total RVA | Tactical Profile |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **1** | **Naman Dhir** | `37052` | **94.2** | 196.4 | 179.2 | **+17.2** | +28.4 | Death Finisher & Disruptor |
| **2** | **Shashank Singh** | `2756` | **93.8** | 184.6 | 169.8 | **+14.8** | +34.2 | Clutch Chase Accelerator |
| **3** | **Rishabh Pant** | `4703` | **92.5** | 168.2 | 156.8 | **+11.4** | +41.6 | High-Leverage Counter-Attacker |
| **4** | **Suryakumar Yadav** | `1699` | **91.9** | 172.5 | 162.7 | **+9.8** | +48.9 | 360° Field Manipulator |
| **5** | **Tim David** | `6396` | **90.4** | 182.1 | 174.5 | **+7.6** | +31.8 | Pure Boundary Closer |
| **6** | **Ishan Kishan** | `4117` | **89.7** | 158.4 | 148.9 | **+9.5** | +26.3 | Crisis First-Phase Attacker |
| **7** | **Dinesh Karthik** | `143` | **88.8** | 188.2 | 178.6 | **+9.6** | +29.1 | Veteran Tactical Closer |
| **8** | **Virat Kohli** | `47` | **88.2** | 149.6 | 144.2 | **+5.4** | **+52.1** | Volume Anchor & Target Master |
| **9** | **Jos Buttler** | `813` | **87.6** | 154.2 | 150.1 | **+4.1** | +46.8 | High-Leverage Match Winner |
| **10** | **Ruturaj Gaikwad** | `6059` | **86.9** | 152.8 | 148.2 | **+4.6** | +39.4 | Controlled Accumulator |

---

## 🎯 Official Top 10 Bowlers Under Pressure (Selected on Unstop)

| Rank | Player Name | ID | PRI | Press Econ | Phase ΔEcon | Total BVA | Death % | Tactical Profile |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **1** | **Mohammad Nawaz** | `2490` | **94.5** | 6.84 | **+2.18** | +38.6 | 28.4% | Matchup Specialist & Wicket Taker |
| **2** | **Abrar Ahmed** | `5979` | **93.7** | 6.92 | **+2.05** | +32.4 | 22.1% | Mystery Spin Crisis Strangler |
| **3** | **Sunil Narine** | `781` | **93.1** | 6.45 | **+1.88** | +42.1 | 34.6% | Multi-Phase Boundary Denial |
| **4** | **Akeal Hosein** | `2417` | **92.4** | 7.08 | **+1.79** | +31.5 | 18.9% | Early-Leverage Constrictor |
| **5** | **Mitchell Santner** | `4101` | **91.8** | 6.72 | **+1.74** | +29.8 | 19.5% | Control & Economy Bowler |
| **6** | **Jasprit Bumrah** | `2933` | **91.2** | 7.32 | **+1.99** | **+45.2** | **68.2%** | Generational Death Master |
| **7** | **Mujeeb Ur Rahman** | `6450` | **90.5** | 7.15 | **+1.62** | +27.6 | 16.4% | High-Accuracy Containment |
| **8** | **Rashid Khan** | `4722` | **89.9** | 7.24 | **+1.58** | +39.8 | 41.2% | Clutch Enforcer & Wicket Hunter |
| **9** | **Shaheen Afridi** | `6355` | **89.2** | 8.12 | **+1.48** | +36.5 | 58.7% | High-Stakes Pacer |
| **10** | **Shadab Khan** | `4926` | **88.5** | 7.38 | **+1.42** | +33.1 | 29.8% | Aggressive Middle Spin Enforcer |

---

## 📉 The Anti-Rankings: Clutch vs Chokers

The model separates genuine accelerators from flat-track bullies who collapse under pressure:

### 🚀 Top Pressure Accelerators (Highest +ΔSR)
- **Naman Dhir**: **+17.2** SR above baseline (196.4 vs 179.2)
- **Shashank Singh**: **+14.8** SR above baseline (184.6 vs 169.8)
- **Rishabh Pant**: **+11.4** SR above baseline (168.2 vs 156.8)

### ⚠️ Top Pressure Dippers (Steepest Performance Dip)
- **Curtis Campher**: **-5.04** ΔSR (Struggles against set fields)
- **Washington Sundar**: **-3.80** ΔSR (Lacks power boundary options)
- **Deepak Hooda**: **-2.87** ΔSR (High dot ball accumulation)
- **Andre Russell (Bowling)**: **-2.29** Phase ΔEcon (Yields 12+ RPO at death vs 10.56 par)

---

## 💻 The Platform: SupeRR Selector Analytics Suite

We built an enterprise-grade Streamlit Analytics Dashboard:

1. **Broadcast Live Ticker**: Real-time tournament intel marquee.
2. **6-Axis Polar Radar**: Player capabilities vs cohort medians.
3. **Player Comparison Lab**: Head-to-head showdowns for 2–5 players.
4. **Delivery-Level Physics**: Expected runs ($\mathbb{E}[\text{Runs}]$) and live RVA/BVA across 200,999 deliveries.
5. **Turnkey Deployment**: One-click cloud deploy on Streamlit Community Cloud + local daemon.

---

## 🏆 Franchise Moneyball Strategy for Rajasthan Royals

1. **Finisher Valuation**: Uncapped finishers with positive $\Delta$SR (like Naman Dhir and Shashank Singh) deliver more win probability surplus per crore than traditional top-order anchors.
2. **Death Bowling Allocation**: Protect bowlers with positive Phase $\Delta$Econ (Bumrah, Sandeep Sharma, Nawaz) strictly for overs 17, 19, and 20.
3. **Anti-Fragile Team Composition**: Pair high-volume anchors (Kohli, Buttler) with high-acceleration disruptors (Pant, David) to minimize collapse risk while maximizing death-overs ceiling.

> **Halla Bol! Ready for Round 2.**

