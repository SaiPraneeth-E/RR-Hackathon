import streamlit as st
import pandas as pd
import numpy as np
from utils.styling import apply_custom_theme, render_header, render_kpi, render_callout
from utils.data_loader import load_bowlers_data
from utils.visualizations import plot_scatter, plot_horizontal_bar, THEME

st.set_page_config(page_title="Bowling Analytics | SUPERR SELECTOR", page_icon="🎯", layout="wide")
apply_custom_theme()

render_header(
    title="BOWLER ANALYTICS CENTER",
    subtitle="Evaluating Phase-Adjusted Containment, Death Overs Domination & Bowling Value Added (BVA)",
    tag="Bowling Division"
)

bowl_df = load_bowlers_data()

# Filter Controls Bar
st.markdown("### 🔍 Filter & Explore Bowling Leaderboard")
f_c1, f_c2, f_c3, f_c4 = st.columns([2, 1.5, 1.5, 1.5])

with f_c1:
    search_query = st.text_input("Search Bowler Name", placeholder="e.g. Bumrah, Narine, Rashid Khan, Nawaz...")

with f_c2:
    min_balls = st.slider("Min Pressure Balls Bowled", min_value=60, max_value=300, value=60, step=10)

with f_c3:
    tier_filter = st.selectbox("Rank Scope", ["Top 10", "Top 25", "Top 50", "All Qualified (98)"], index=3)

with f_c4:
    sort_by = st.selectbox("Sort Table By", ["PRI Score", "Phase ΔEcon (Par Savings)", "Pressure Economy", "Total BVA", "Death Overs Share %", "Dot Ball %"])

# Apply Filters
filtered = bowl_df[bowl_df['balls_p'] >= min_balls].copy()

if search_query:
    filtered = filtered[filtered['bowler_name'].str.contains(search_query, case=False, na=False)]

if tier_filter == "Top 10":
    filtered = filtered.head(10)
elif tier_filter == "Top 25":
    filtered = filtered.head(25)
elif tier_filter == "Top 50":
    filtered = filtered.head(50)

# Sort Mapping
if sort_by == "Pressure Economy":
    filtered = filtered.sort_values(by='econ_p', ascending=True)
else:
    sort_map = {
        "PRI Score": "PRI",
        "Phase ΔEcon (Par Savings)": "phase_delta_econ",
        "Total BVA": "total_bva_p",
        "Death Overs Share %": "death_share",
        "Dot Ball %": "dot_pct_p"
    }
    filtered = filtered.sort_values(by=sort_map[sort_by], ascending=False)

# KPI Summary
k1, k2, k3, k4 = st.columns(4)
render_kpi(k1, "Bowlers Displayed", f"{len(filtered)}", f"Out of {len(bowl_df)} qualified", "neutral")
render_kpi(k2, "Avg Pressure Economy", f"{filtered['econ_p'].mean():.2f}", f"Baseline: {filtered['econ_all'].mean():.2f}", "neutral")
top_bva_player = filtered.sort_values(by='total_bva_p', ascending=False).iloc[0]
render_kpi(k3, "Top Total BVA", f"+{top_bva_player['total_bva_p']:.1f}", f"{top_bva_player['bowler_name']}", "positive")
top_phase_saver = filtered.sort_values(by='phase_delta_econ', ascending=False).iloc[0]
render_kpi(k4, "Top Phase Saver", f"+{top_phase_saver['phase_delta_econ']:.2f} RPO", f"{top_phase_saver['bowler_name']}", "positive")

# Analytical Callout on Phase Adjustment
render_callout(
    "A raw economy of 8.00 RPO in the Powerplay is below average (par is ~7.4 RPO), but 8.00 RPO in the Death overs (16–20) "
    "is world-class (par is 10.56 RPO). Jasprit Bumrah's raw economy is 7.32 RPO, but because 68% of his pressure deliveries "
    "occur in the death overs, his <strong>Phase-Adjusted Economy Savings (Phase ΔEcon) is +1.99 runs saved per over vs par!</strong>",
    title="WHY PHASE-ADJUSTED ECONOMY MATTERS"
)

# Leaderboard Table
st.markdown("### 📋 Interactive Bowling Leaderboard")

display_cols = [
    'rank', 'bowler_name', 'bowler_id', 'balls_p', 'wickets_p',
    'econ_p', 'econ_all', 'phase_delta_econ', 'death_share', 'dot_pct_p',
    'win_impact_pct', 'total_bva_p', 'PRI'
]
table_df = filtered[display_cols].copy()
table_df.columns = [
    'Rank', 'Bowler', 'ID', 'Balls (P)', 'Wickets (P)',
    'Pressure Econ', 'Base Econ', 'Phase ΔEcon', 'Death Share %', 'Dot %',
    'Win Impact %', 'Total BVA', 'PRI Score'
]

st.dataframe(
    table_df.style.format({
        'Pressure Econ': '{:.2f}',
        'Base Econ': '{:.2f}',
        'Phase ΔEcon': '{:+.2f}',
        'Death Share %': '{:.1f}%',
        'Dot %': '{:.1f}%',
        'Win Impact %': '{:.1f}%',
        'Total BVA': '{:+.1f}',
        'PRI Score': '{:.1f}'
    }).background_gradient(subset=['PRI Score'], cmap='YlGn')
      .background_gradient(subset=['Phase ΔEcon'], cmap='coolwarm', vmin=-2.0, vmax=2.5),
    use_container_width=True,
    height=420,
    hide_index=True
)

# Download CSV Button
csv_data = table_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Bowling Leaderboard (CSV)",
    data=csv_data,
    file_name="superr_selector_bowling_leaderboard.csv",
    mime="text/csv"
)

# Visualizations Section
st.markdown("---")
st.markdown("### 📈 Analytical Visualizations")

chart_tab1, chart_tab2, chart_tab3 = st.tabs([
    "🛡️ Phase-Adjusted Economy Savings vs Par",
    "💀 Death Overs (16–20) Specialist Matrix",
    "📊 Cumulative Bowling Value Added (BVA)"
])

with chart_tab1:
    st.markdown("#### Phase-Adjusted Economy Savings: Who Beats Contextual Par?")
    median_econ = float(filtered['econ_p'].median())
    fig_phase = plot_scatter(
        df=filtered,
        x_col='econ_p',
        y_col='phase_delta_econ',
        text_col='bowler_name',
        color_col='PRI',
        size_col='balls_p',
        title="Pressure Economy vs Phase Savings (Top Left is Optimal: Low Econ, Massive Par Savings)",
        x_label="Pressure Economy Rate (Lower is Better)",
        y_label="Phase-Adjusted Economy Savings (Phase ΔEcon: Higher is Better)",
        vline=median_econ,
        hline=0.0
    )
    st.plotly_chart(fig_phase, use_container_width=True)

with chart_tab2:
    st.markdown("#### Death Overs Specialization: Bowling When Stakes Peak")
    death_filtered = filtered[filtered['death_balls'] >= 30].copy()
    death_filtered['death_econ'] = (death_filtered['runs_p'] / (death_filtered['balls_p'] / 6)).round(2)
    fig_death = plot_scatter(
        df=death_filtered,
        x_col='death_share',
        y_col='phase_delta_econ',
        text_col='bowler_name',
        color_col='PRI',
        size_col='death_balls',
        title="Death Overs Workload Share vs Phase Savings (Min 30 Death Balls)",
        x_label="Death Overs Share of Pressure Deliveries (%)",
        y_label="Phase-Adjusted Economy Savings (RPO)",
        vline=float(death_filtered['death_share'].median()),
        hline=0.0
    )
    st.plotly_chart(fig_death, use_container_width=True)

with chart_tab3:
    st.markdown("#### Cumulative Match Value: Top 15 Bowlers by Total Bowling Value Added (BVA)")
    top15_bva = bowl_df.sort_values(by='total_bva_p', ascending=False).head(15)
    fig_bva_bar = plot_horizontal_bar(
        df=top15_bva,
        x_col='total_bva_p',
        y_col='bowler_name',
        title="Top 15 Bowlers by Total Situational BVA Added",
        x_label="Total BVA (Runs Saved & Wickets Gained Above Contextual Par)",
        color_col='PRI',
        height=480
    )
    st.plotly_chart(fig_bva_bar, use_container_width=True)

