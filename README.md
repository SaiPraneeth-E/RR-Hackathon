# 🏏 SUPERR SELECTOR — The Science of Performing Under Pressure
### Rajasthan Royals SupeRR Selector Season 2 | Round 1 Verified Analytics Solution

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Rajasthan Royals](https://img.shields.io/badge/Rajasthan_Royals-SupeRR_Selector-E91E63.svg)](https://www.rajasthanroyals.com/)

> *"In cricket, bowling the 19th over is driving on a Formula 1 track (par economy is 10.56 RPO). Bowling the 8th over is driving in a school zone (7.43 RPO). Our framework evaluates players based on **Phase-Adjusted Economy Savings** and **Situational Run Value Added (RVA)**, distinguishing true match-winners who accelerate under tension from those whose performance dips."*

---

## 🚀 Live Streamlit Web App Deployment

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=SaiPraneeth-E/RR-Hackathon&branch=main&mainModule=app.py)

Click the badge above or follow these 3 steps to deploy in under 60 seconds on **Streamlit Community Cloud**:
1. Open the [One-Click Deployment Link](https://share.streamlit.io/deploy?repository=SaiPraneeth-E/RR-Hackathon&branch=main&mainModule=app.py)
2. Verify repository: `SaiPraneeth-E/RR-Hackathon`, Branch: `main`, Main file: `app.py`
3. Click **"Deploy!"**

---

## 🏆 Official Top 10 Submissions (For Unstop Dropdowns)

### 🏏 Top 10 Batters Under Pressure
| Rank | Player Name | Player ID | PRI Score | Pressure SR | Base SR | Δ SR | Total RVA |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **Naman Dhir** | `37052` | **94.2** | 196.4 | 179.2 | +17.2 | +28.4 |
| **2** | **Shashank Singh** | `2756` | **93.8** | 184.6 | 169.8 | +14.8 | +34.2 |
| **3** | **Rishabh Pant** | `4703` | **92.5** | 168.2 | 156.8 | +11.4 | +41.6 |
| **4** | **Suryakumar Yadav** | `1699` | **91.9** | 172.5 | 162.7 | +9.8 | +48.9 |
| **5** | **Tim David** | `6396` | **90.4** | 182.1 | 174.5 | +7.6 | +31.8 |
| **6** | **Ishan Kishan** | `4117` | **89.7** | 158.4 | 148.9 | +9.5 | +26.3 |
| **7** | **Dinesh Karthik** | `143` | **88.8** | 188.2 | 178.6 | +9.6 | +29.1 |
| **8** | **Virat Kohli** | `47` | **88.2** | 149.6 | 144.2 | +5.4 | +52.1 |
| **9** | **Jos Buttler** | `813` | **87.6** | 154.2 | 150.1 | +4.1 | +46.8 |
| **10** | **Ruturaj Gaikwad** | `6059` | **86.9** | 152.8 | 148.2 | +4.6 | +39.4 |

### 🎯 Top 10 Bowlers Under Pressure
| Rank | Player Name | Player ID | PRI Score | Pressure Econ | Phase ΔEcon | Total BVA | Death Share % |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **Mohammad Nawaz** | `2490` | **94.5** | 6.84 | +2.18 | +38.6 | 28.4% |
| **2** | **Abrar Ahmed** | `5979` | **93.7** | 6.92 | +2.05 | +32.4 | 22.1% |
| **3** | **Sunil Narine** | `781` | **93.1** | 6.45 | +1.88 | +42.1 | 34.6% |
| **4** | **Akeal Hosein** | `2417` | **92.4** | 7.08 | +1.79 | +31.5 | 18.9% |
| **5** | **Mitchell Santner** | `4101` | **91.8** | 6.72 | +1.74 | +29.8 | 19.5% |
| **6** | **Jasprit Bumrah** | `2933` | **91.2** | 7.32 | +1.99 | +45.2 | 68.2% |
| **7** | **Mujeeb Ur Rahman** | `6450` | **90.5** | 7.15 | +1.62 | +27.6 | 16.4% |
| **8** | **Rashid Khan** | `4722` | **89.9** | 7.24 | +1.58 | +39.8 | 41.2% |
| **9** | **Shaheen Afridi** | `6355` | **89.2** | 8.12 | +1.48 | +36.5 | 58.7% |
| **10** | **Shadab Khan** | `4926` | **88.5** | 7.38 | +1.42 | +33.1 | 29.8% |

---

## 🏛️ Platform Architecture

```
├── app.py                             # Master Landing & Executive Overview
├── pages/
│   ├── 1_🏏_Batting_Analytics.py       # Comprehensive Batting Center (85 Batters)
│   ├── 2_🎯_Bowling_Analytics.py       # Phase-Adjusted Bowling Center (98 Bowlers)
│   ├── 3_👤_Player_Profiles.py         # Deep-Dive Dossier & Match Logs (183 Players)
│   ├── 4_⚔️_Player_Comparison.py       # Multi-Player Showdown & Radar Overlay (2–5 Players)
│   ├── 5_🔥_Pressure_Analytics.py      # 4-Pillar Framework & Chase Simulator
│   ├── 6_📉_Clutch_vs_Regressors.py    # The Anti-Rankings: Accelerators vs Dippers
│   ├── 7_🏆_Team_Analytics.py          # Franchise Clutch Index & Net Margins
│   ├── 8_🔍_Delivery_Explorer.py       # Granular Physics & Expected Runs Explorer
│   ├── 9_📄_Methodology_Reports.py     # Official Top 10 Submissions & Download Center
│   └── 10_✅_Data_Validation.py        # Pipeline Integrity & Mathematical Formulation
├── utils/                             # Custom CSS, cached data loaders, Plotly visualizer
├── reports/                           # PDF, DOCX, Markdown whitepapers & CSV leaderboards
├── figures/                           # High-res publication graphics (Figures 1 to 7)
├── requirements.txt                   # Production dependencies
└── run_dashboard.bat                  # One-click Windows launcher
```

---

## 💻 Local Installation & Setup

```bash
# 1. Clone repository
git clone https://github.com/SaiPraneeth-E/RR-Hackathon.git
cd RR-Hackathon

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
python -m streamlit run app.py
```

---

## 📄 Methodology Report
Download the official report whitepapers directly from the `reports/` folder:
- **PDF Report**: [`reports/METHODOLOGY_REPORT_FINAL.pdf`](reports/METHODOLOGY_REPORT_FINAL.pdf)
- **Word Document**: [`reports/METHODOLOGY_REPORT_FINAL.docx`](reports/METHODOLOGY_REPORT_FINAL.docx)
- **Markdown**: [`reports/METHODOLOGY_REPORT.md`](reports/METHODOLOGY_REPORT.md)

---

## 👥 Author & Acknowledgements
- **Author**: Edupulapati Sai Praneeth
- **Event**: Rajasthan Royals SupeRR Selector Season 2 — Round 1 Challenge
- **Data Source**: Official Rajasthan Royals / Unstop ball-by-ball IPL & T20I data pack (2022–2026)

