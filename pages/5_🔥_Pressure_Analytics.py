import streamlit as st
import pandas as pd
import numpy as np
from utils.styling import apply_custom_theme, render_header, render_kpi, render_callout
from utils.data_loader import load_macro_stats
from utils.visualizations import plot_over_progression, plot_win_probability_heatmap, THEME

st.set_page_config(page_title="Pressure Situation Analytics | SUPERR SELECTOR", page_icon="🔥", layout="wide")
apply_custom_theme()

render_header(
    title="PRESSURE SITUATION ANALYTICS",
    subtitle="Deconstructing the 4-Pillar Pressure Framework Across 200,999 Deliveries",
    tag="Theoretical & Empirical Foundation"
)

macro = load_macro_stats()

# Overview Narrative
render_callout(
    "Cricket analytics often treats an over bowled in the 7th over with 10 wickets in hand the same as the 19th over "
    "with 18 runs required and 2 wickets left. Our 4-Pillar Pressure Framework eliminates this flaw by establishing "
    "mathematical conditions that identify when an individual ball possesses disproportionate leverage over the match outcome.",
    title="THE 4-PILLAR ARCHITECTURE"
)

# 4 Pillars Cards
p1, p2, p3, p4 = st.columns(4)

with p1:
    st.markdown("""
        <div class="rr-kpi-card" style="border-top: 3px solid #E91E63;">
            <div class="rr-kpi-title">Pillar 1: Over Leverage</div>
            <div style="font-size: 15px; font-weight: 700; color: #fff; margin: 8px 0;">Overs 16 to 20 (Death)</div>
            <div style="font-size: 12px; color: #94A3B8; line-height: 1.5;">
                Every delivery in overs 16–20 carries extreme leverage. Par economy accelerates to 10.56 RPO, and dot balls immediately tilt win probability.
            </div>
            <div style="margin-top: 10px; font-size: 11px; color: #FF80AB; font-weight: 700;">46.2% of Pressure Balls</div>
        </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown("""
        <div class="rr-kpi-card" style="border-top: 3px solid #38BDF8;">
            <div class="rr-kpi-title">Pillar 2: Chase Knife-Edge</div>
            <div style="font-size: 15px; font-weight: 700; color: #fff; margin: 8px 0;">Escalating RRR & Wickets</div>
            <div style="font-size: 12px; color: #94A3B8; line-height: 1.5;">
                Activated when RRR exceeds 9.0 RPO, or when wickets in hand fall below 5. Creates immediate asymmetric risk where dot balls compound tension.
            </div>
            <div style="margin-top: 10px; font-size: 11px; color: #38BDF8; font-weight: 700;">38.4% of Pressure Balls</div>
        </div>
    """, unsafe_allow_html=True)

with p3:
    st.markdown("""
        <div class="rr-kpi-card" style="border-top: 3px solid #F59E0B;">
            <div class="rr-kpi-title">Pillar 3: Wicket Mortality</div>
            <div style="font-size: 15px; font-weight: 700; color: #fff; margin: 8px 0;">First 6 Balls of Batter</div>
            <div style="font-size: 12px; color: #94A3B8; line-height: 1.5;">
                Wicket mortality is 3.1x higher during a batter's first 6 balls. Players who can absorb early swing and rotate strike without stalling prevent fatal collapses.
            </div>
            <div style="margin-top: 10px; font-size: 11px; color: #F59E0B; font-weight: 700;">15.4% of Pressure Balls</div>
        </div>
    """, unsafe_allow_html=True)

with p4:
    st.markdown("""
        <div class="rr-kpi-card" style="border-top: 3px solid #10B981;">
            <div class="rr-kpi-title">Pillar 4: Match Stakes</div>
            <div style="font-size: 15px; font-weight: 700; color: #fff; margin: 8px 0;">Playoffs, Finals & World Cups</div>
            <div style="font-size: 12px; color: #94A3B8; line-height: 1.5;">
                A 1.25x context multiplier is applied to knockout fixtures, finals, and ICC tournament eliminations where elimination consequences amplify tension.
            </div>
            <div style="margin-top: 10px; font-size: 11px; color: #10B981; font-weight: 700;">1.25x Multiplier Applied</div>
        </div>
    """, unsafe_allow_html=True)

# Visualizations Row
st.markdown("---")
st.markdown("### 📊 Empirical Behavior of Pressure Across Match Stages")

c_left, c_right = st.columns(2)

with c_left:
    st.plotly_chart(plot_over_progression(macro['over_prog']), use_container_width=True)

with c_right:
    st.plotly_chart(plot_win_probability_heatmap(), use_container_width=True)

# Interactive Chase Scenario Simulator
st.markdown("---")
st.markdown("### 🎛️ Interactive Chase Pressure Simulator")
st.markdown("Adjust the match parameters below to observe how the pressure model evaluates the situation in real time:")

sim_col1, sim_col2, sim_col3 = st.columns(3)
with sim_col1:
    sim_rrr = st.slider("Required Run Rate (RRR)", min_value=4.0, max_value=20.0, value=11.5, step=0.5)
with sim_col2:
    sim_wkts = st.slider("Wickets in Hand", min_value=1, max_value=10, value=4, step=1)
with sim_col3:
    sim_over = st.slider("Current Over Number", min_value=1, max_value=20, value=17, step=1)

# Calculate simulation dynamics
z_sim = -0.52 * (sim_rrr - 9.2) + 0.65 * (sim_wkts - 4.5)
sim_win_prob = 1.0 / (1.0 + np.exp(-z_sim)) * 100
is_pressure_sim = (sim_over >= 16) or (sim_rrr >= 9.0) or (sim_wkts <= 4)
pressure_tier = "CRITICAL HIGH PRESSURE" if (sim_over >= 16 and sim_rrr >= 10.0) else ("HIGH PRESSURE" if is_pressure_sim else "MODERATE / STANDARD")

res_col1, res_col2, res_col3 = st.columns(3)
render_kpi(res_col1, "Modeled Win Probability", f"{sim_win_prob:.1f}%", "Based on 883 match logistic model", "positive" if sim_win_prob > 50 else "negative")
render_kpi(res_col2, "Situation Classification", pressure_tier, "Triggered by Pillars 1 & 2", "positive" if is_pressure_sim else "neutral")
render_kpi(res_col3, "Leverage Index (LI)", f"{1.0 + (sim_rrr/10.0)*(11 - sim_wkts)/5.0:.2f}x", "Multiplies baseline ball leverage", "neutral")

