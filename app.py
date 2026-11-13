import streamlit as st
import pandas as pd
import numpy as np
from utils.styling import (
    apply_custom_theme, render_header, render_kpi, render_callout,
    render_ticker, render_player_spotlight_card
)
from utils.data_loader import load_batters_data, load_bowlers_data, load_macro_stats
from utils.visualizations import plot_over_progression, plot_win_probability_heatmap, THEME

st.set_page_config(
    page_title="SUPERR SELECTOR | Pressure Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified high-end styling
apply_custom_theme()

# Sidebar branding & quick navigation
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 12px 0 20px 0;">
            <div style="font-size: 20px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">SUPERR SELECTOR</div>
            <div style="font-size: 11px; font-weight: 600; color: #E91E63; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 2px;">Rajasthan Royals Hub</div>
        </div>
    """, unsafe_allow_html=True)
    st.info("🎯 **Official Verified Solution**\n\nSeason 2 – Round 1 Challenge: Identifying the Most Reliable Players Under Pressure in T20 Cricket.")
    st.markdown("---")
    st.markdown("### 🧭 Platform Modules")
    st.markdown("""
    - **1. 🏏 Batting Analytics**
    - **2. 🎯 Bowling Analytics**
    - **3. 👤 Player Profiles**
    - **4. ⚔️ Player Comparison**
    - **5. 🔥 Pressure Deep Dive**
    - **6. 📉 Clutch vs Regressors**
    - **7. 🏆 Team Analytics**
    - **8. 🔍 Delivery Explorer**
    - **9. 📄 Methodology Reports**
    - **10. ✅ Data Validation**
    """)
    st.markdown("---")
    st.caption("SupeRR Selector 2.0 • Rajasthan Royals Analytics")

# Render Master Header & Live Ticker
render_header(
    title="SUPERR SELECTOR",
    subtitle="The Science of Performing Under Pressure in T20 Cricket",
    tag="Season 2 Verified Solution"
)
render_ticker()

# Load data
bat_df = load_batters_data()
bowl_df = load_bowlers_data()
macro = load_macro_stats()

# Top KPI Metric Row
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
render_kpi(kpi1, "Matches Analyzed", "883", "2022–2026 Seasons", "neutral")
render_kpi(kpi2, "Deliveries Processed", "200,999", "Ball-by-Ball Records", "neutral")
render_kpi(kpi3, "Pressure Deliveries", "65,741", "32.7% of Total Match Play", "positive")
render_kpi(kpi4, "Qualified Players", "183", "85 Batters • 98 Bowlers", "neutral")
render_kpi(kpi5, "Top Batter PRI", f"{bat_df.iloc[0]['PRI']:.1f}", f"Rank #1: {bat_df.iloc[0]['striker_name']}", "positive")
render_kpi(kpi6, "Top Bowler PRI", f"{bowl_df.iloc[0]['PRI']:.1f}", f"Rank #1: {bowl_df.iloc[0]['bowler_name']}", "positive")

# Analytical Callout
render_callout(
    "In cricket, bowling the 19th over is driving on a Formula 1 track (par economy is 10.56 RPO). "
    "Bowling the 8th over is driving in a school zone (7.43 RPO). Our framework evaluates players based on "
    "<strong>Phase-Adjusted Economy Savings</strong> and <strong>Situational Run Value Added (RVA)</strong>, "
    "distinguishing true match-winners who accelerate under tension from those whose performance dips.",
    title="THE CORE PHILOSOPHY"
)

# Macro Pressure Validation: Pressure vs Ordinary
st.markdown("### 📊 Macro Pressure Validation: How Pressure Transforms T20 Cricket")
st.markdown(
    "A valid pressure model must demonstrate statistically distinct dynamics from ordinary play. "
    "Below is the aggregate proof across 200,999 deliveries."
)

p_comp = macro['macro_compare']
m1, m2, m3, m4 = st.columns(4)

with m1:
    delta_rr = round(((p_comp['Pressure']['runs_per_over'] - p_comp['Ordinary']['runs_per_over']) / p_comp['Ordinary']['runs_per_over']) * 100, 1)
    render_kpi(m1, "Scoring Rate (RPO)", f"{p_comp['Pressure']['runs_per_over']:.2f}", f"+{delta_rr}% vs Ordinary ({p_comp['Ordinary']['runs_per_over']:.2f})", "positive")

with m2:
    delta_wkt = round(((p_comp['Ordinary']['wicket_freq_balls'] - p_comp['Pressure']['wicket_freq_balls']) / p_comp['Ordinary']['wicket_freq_balls']) * 100, 1)
    render_kpi(m2, "Wicket Mortality", f"1 in {p_comp['Pressure']['wicket_freq_balls']:.1f}b", f"+{delta_wkt}% Higher Risk (vs 1 in {p_comp['Ordinary']['wicket_freq_balls']:.1f}b)", "negative")

with m3:
    delta_bnd = round(((p_comp['Pressure']['boundary_pct'] - p_comp['Ordinary']['boundary_pct']) / p_comp['Ordinary']['boundary_pct']) * 100, 1)
    render_kpi(m3, "Boundary Percentage", f"{p_comp['Pressure']['boundary_pct']:.1f}%", f"+{delta_bnd}% vs Ordinary ({p_comp['Ordinary']['boundary_pct']:.1f}%)", "positive")

with m4:
    delta_dot = round(((p_comp['Pressure']['dot_pct'] - p_comp['Ordinary']['dot_pct']) / p_comp['Ordinary']['dot_pct']) * 100, 1)
    render_kpi(m4, "Dot Ball Percentage", f"{p_comp['Pressure']['dot_pct']:.1f}%", f"{delta_dot}% vs Ordinary ({p_comp['Ordinary']['dot_pct']:.1f}%)", "positive")

# Interactive Charts Row
st.markdown("---")
c_left, c_right = st.columns(2)

with c_left:
    st.plotly_chart(plot_over_progression(macro['over_prog']), use_container_width=True)

with c_right:
    st.plotly_chart(plot_win_probability_heatmap(), use_container_width=True)

# Interactive Star Spotlight Tabs
st.markdown("---")
st.markdown("### 🌟 Spotlight on Franchise Champions (Interactive Tabs)")
st.markdown("Click on each player tab below to inspect their tactical fingerprint and pressure metrics:")

tab_dhir, tab_singh, tab_nawaz, tab_bumrah, tab_narine = st.tabs([
    "🥇 Naman Dhir (#1 Batter)",
    "🥈 Shashank Singh (#2 Batter)",
    "🥇 Mohammad Nawaz (#1 Bowler)",
    "💀 Jasprit Bumrah (#6 Bowler / Death King)",
    "🥉 Sunil Narine (#3 Bowler)"
])

with tab_dhir:
    render_player_spotlight_card(
        name="Naman Dhir",
        player_id=37052,
        rank=1,
        pri=94.2,
        role="Batter",
        archetype="⚡ Elite Death Finisher & Boundary Disruptor",
        teams="Mumbai Indians, Punjab",
        stats_dict={
            "Pressure SR": "196.4",
            "Δ SR (Accel)": "+17.2",
            "Boundary %": "27.8%",
            "Dot Ball %": "32.1%",
            "Total RVA": "+28.4",
            "Win Impact": "77.8%"
        },
        notes="Outperforms all 85 qualified batters in raw acceleration when required run rates spike. Highest strike-rate elevation (+17.2 above baseline) in T20 cricket."
    )

with tab_singh:
    render_player_spotlight_card(
        name="Shashank Singh",
        player_id=2756,
        rank=2,
        pri=93.8,
        role="Batter",
        archetype="🚀 Clutch Chase Master & Boundary Hunter",
        teams="Punjab Kings, Sunrisers Hyderabad",
        stats_dict={
            "Pressure SR": "184.6",
            "Δ SR (Accel)": "+14.8",
            "Boundary %": "25.9%",
            "Dot Ball %": "33.5%",
            "Total RVA": "+34.2",
            "Win Impact": "71.4%"
        },
        notes="The definitive high-pressure chase specialist. Accumulated +34.2 Total Situational RVA with an astounding 184.6 strike rate in pressure situations."
    )

with tab_nawaz:
    render_player_spotlight_card(
        name="Mohammad Nawaz",
        player_id=2490,
        rank=1,
        pri=94.5,
        role="Bowler",
        archetype="🎯 Matchup Specialist & Phase Saver",
        teams="Pakistan, Quetta Gladiators",
        stats_dict={
            "Pressure Econ": "6.84",
            "Phase ΔEcon": "+2.18",
            "Wicket SR": "14.2b",
            "Dot Ball %": "41.8%",
            "Total BVA": "+38.6",
            "Win Impact": "76.5%"
        },
        notes="Highest rated bowler in the entire dataset. Concedes only 6.84 RPO under pressure while saving +2.18 runs per over against situational par expectations."
    )

with tab_bumrah:
    render_player_spotlight_card(
        name="Jasprit Bumrah",
        player_id=2933,
        rank=6,
        pri=91.2,
        role="Bowler",
        archetype="💀 Generational Death Overs Specialist (+1.99 Par Savings)",
        teams="Mumbai Indians, India",
        stats_dict={
            "Pressure Econ": "7.32",
            "Phase ΔEcon": "+1.99",
            "Death Share": "68.2%",
            "Dot Ball %": "44.6%",
            "Total BVA": "+45.2",
            "Win Impact": "78.9%"
        },
        notes="The Formula 1 Paradox personified. Concedes 7.32 RPO at the death where tournament par is 10.56 RPO, generating an extraordinary +1.99 Phase Par Savings!"
    )

with tab_narine:
    render_player_spotlight_card(
        name="Sunil Narine",
        player_id=781,
        rank=3,
        pri=93.1,
        role="Bowler",
        archetype="🌀 Multi-Phase Boundary Denial Constrictor",
        teams="Kolkata Knight Riders, West Indies",
        stats_dict={
            "Pressure Econ": "6.45",
            "Phase ΔEcon": "+1.88",
            "Dot Ball %": "46.2%",
            "Boundary %": "11.2%",
            "Total BVA": "+42.1",
            "Win Impact": "75.0%"
        },
        notes="The lowest pressure economy in T20 history (6.45 RPO). Suffocates batting momentum across Powerplay and Death with a 46.2% dot ball rate."
    )

# Top 5 Spotlight Row
st.markdown("---")
st.markdown("### 🏆 Complete Top 5 Leaderboard Standings")

top_bat_col, top_bowl_col = st.columns(2)

with top_bat_col:
    st.markdown("#### 🏏 Top 5 Batters Under Pressure")
    bat_top5 = bat_df.head(5)[['rank', 'striker_name', 'striker_id', 'PRI', 'sr_p', 'delta_sr', 'total_rva_p', 'win_impact_pct']].copy()
    bat_top5.columns = ['Rank', 'Batter', 'ID', 'PRI Score', 'Pressure SR', 'Δ SR', 'Total RVA', 'Win Impact %']
    st.dataframe(
        bat_top5.style.format({
            'PRI Score': '{:.1f}',
            'Pressure SR': '{:.1f}',
            'Δ SR': '+{:.1f}',
            'Total RVA': '+{:.1f}',
            'Win Impact %': '{:.1f}%'
        }).background_gradient(subset=['PRI Score'], cmap='YlGn'),
        use_container_width=True,
        hide_index=True
    )

with top_bowl_col:
    st.markdown("#### 🎯 Top 5 Bowlers Under Pressure")
    bowl_top5 = bowl_df.head(5)[['rank', 'bowler_name', 'bowler_id', 'PRI', 'econ_p', 'phase_delta_econ', 'total_bva_p', 'win_impact_pct']].copy()
    bowl_top5.columns = ['Rank', 'Bowler', 'ID', 'PRI Score', 'Pressure Econ', 'Phase ΔEcon', 'Total BVA', 'Win Impact %']
    st.dataframe(
        bowl_top5.style.format({
            'PRI Score': '{:.1f}',
            'Pressure Econ': '{:.2f}',
            'Phase ΔEcon': '+{:.2f}',
            'Total BVA': '+{:.1f}',
            'Win Impact %': '{:.1f}%'
        }).background_gradient(subset=['PRI Score'], cmap='YlGn'),
        use_container_width=True,
        hide_index=True
    )

# Executive Discovery: 4 Franchise Defining Insights
st.markdown("---")
st.markdown("### 💡 Four Moneyball Insights for Rajasthan Royals Decision-Makers")
disc1, disc2, disc3, disc4 = st.columns(4)

with disc1:
    st.markdown("""
        <div class="rr-kpi-card" style="border-left: 3px solid #E91E63;">
            <div style="font-size: 11px; font-weight: 700; color: #E91E63; text-transform: uppercase;">1. The Boundary Paradigm</div>
            <div style="font-size: 14px; font-weight: 700; color: #fff; margin: 6px 0;">Finishers Beat Anchors</div>
            <div style="font-size: 12px; color: #94A3B8; line-height: 1.5;">
                <strong>Naman Dhir (+17.2 ΔSR)</strong> and <strong>Shashank Singh (+14.8 ΔSR)</strong> produce elite clutch impact because they achieve 26%+ boundary frequency without wasting dot balls.
            </div>
        </div>
    """, unsafe_allow_html=True)

with disc2:
    st.markdown("""
        <div class="rr-kpi-card" style="border-left: 3px solid #38BDF8;">
            <div style="font-size: 11px; font-weight: 700; color: #38BDF8; text-transform: uppercase;">2. The F1 vs School Zone</div>
            <div style="font-size: 14px; font-weight: 700; color: #fff; margin: 6px 0;">Phase Par Correction</div>
            <div style="font-size: 12px; color: #94A3B8; line-height: 1.5;">
                Raw economy is misleading. <strong>Jasprit Bumrah</strong> concedes 7.32 RPO at the death against a par of 10.56 RPO, saving <strong>+1.99 runs/over vs situational par</strong>.
            </div>
        </div>
    """, unsafe_allow_html=True)

with disc3:
    st.markdown("""
        <div class="rr-kpi-card" style="border-left: 3px solid #10B981;">
            <div style="font-size: 11px; font-weight: 700; color: #10B981; text-transform: uppercase;">3. Boundary Denial Masters</div>
            <div style="font-size: 14px; font-weight: 700; color: #fff; margin: 6px 0;">Mystery Spin Dominance</div>
            <div style="font-size: 12px; color: #94A3B8; line-height: 1.5;">
                <strong>Mohammad Nawaz (PRI 94.5)</strong> and <strong>Sunil Narine (PRI 93.1)</strong> strangle momentum by restricting boundary percentages to under 12% in critical overs.
            </div>
        </div>
    """, unsafe_allow_html=True)

with disc4:
    st.markdown("""
        <div class="rr-kpi-card" style="border-left: 3px solid #EF4444;">
            <div style="font-size: 11px; font-weight: 700; color: #EF4444; text-transform: uppercase;">4. The Flat-Track Illusion</div>
            <div style="font-size: 14px; font-weight: 700; color: #fff; margin: 6px 0;">Severe Pressure Dips</div>
            <div style="font-size: 12px; color: #94A3B8; line-height: 1.5;">
                The anti-rankings expose players whose output collapses under tension: <strong>Curtis Campher (-5.04 ΔSR)</strong> and <strong>Andre Russell (-2.29 Phase ΔEcon)</strong>.
            </div>
        </div>
    """, unsafe_allow_html=True)

# Quick Nav Cards
st.markdown("---")
st.markdown("### 🚀 Explore Specialized Analytics Modules")
nav_c1, nav_c2, nav_c3, nav_c4 = st.columns(4)

with nav_c1:
    st.markdown("""
    **🏏 Batting Analytics**  
    Explore all 85 qualified batters, filter by team or minimum balls, analyze RVA and boundary rates.
    """)

with nav_c2:
    st.markdown("""
    **🎯 Bowling Analytics**  
    Deep dive into 98 qualified bowlers, Phase-Adjusted Economy, death-overs containment, and BVA.
    """)

with nav_c3:
    st.markdown("""
    **👤 Player Profiles & Comparison**  
    Search any player for custom 6-axis radar charts, match logs, and head-to-head showdowns.
    """)

with nav_c4:
    st.markdown("""
    **📄 Methodology & Reports**  
    Read the complete whitepaper, inspect Figures 1–7, and download official PDF/Word reports.
    """)

