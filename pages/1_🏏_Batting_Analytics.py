import streamlit as st
import pandas as pd
import numpy as np
from utils.styling import apply_custom_theme, render_header, render_kpi, render_callout
from utils.data_loader import load_batters_data
from utils.visualizations import plot_scatter, plot_horizontal_bar, THEME

st.set_page_config(page_title="Batting Analytics | SUPERR SELECTOR", page_icon="🏏", layout="wide")
apply_custom_theme()

render_header(
    title="BATTER ANALYTICS CENTER",
    subtitle="Evaluating Clutch Acceleration, Boundary Dominance & Situational Run Value Added (RVA)",
    tag="Batting Division"
)

bat_df = load_batters_data()

# Filter Controls Bar
st.markdown("### 🔍 Filter & Explore Batting Leaderboard")
f_c1, f_c2, f_c3, f_c4 = st.columns([2, 1.5, 1.5, 1.5])

with f_c1:
    search_query = st.text_input("Search Batter Name", placeholder="e.g. Naman Dhir, Shashank Singh, Kohli...")

with f_c2:
    min_balls = st.slider("Min Pressure Balls Faced", min_value=60, max_value=300, value=60, step=10)

with f_c3:
    tier_filter = st.selectbox("Rank Scope", ["Top 10", "Top 25", "Top 50", "All Qualified (85)"], index=3)

with f_c4:
    sort_by = st.selectbox("Sort Table By", ["PRI Score", "Pressure SR", "Δ SR (Acceleration)", "Total RVA", "Boundary %", "Win Impact %"])

# Apply Filters
filtered = bat_df[bat_df['balls_p'] >= min_balls].copy()

if search_query:
    filtered = filtered[filtered['striker_name'].str.contains(search_query, case=False, na=False)]

if tier_filter == "Top 10":
    filtered = filtered.head(10)
elif tier_filter == "Top 25":
    filtered = filtered.head(25)
elif tier_filter == "Top 50":
    filtered = filtered.head(50)

# Sort Mapping
sort_map = {
    "PRI Score": "PRI",
    "Pressure SR": "sr_p",
    "Δ SR (Acceleration)": "delta_sr",
    "Total RVA": "total_rva_p",
    "Boundary %": "bnd_pct_p",
    "Win Impact %": "win_impact_pct"
}
filtered = filtered.sort_values(by=sort_map[sort_by], ascending=False)

# KPI Summary of Filtered Pool
k1, k2, k3, k4 = st.columns(4)
render_kpi(k1, "Batters Displayed", f"{len(filtered)}", f"Out of {len(bat_df)} qualified", "neutral")
render_kpi(k2, "Avg Pressure SR", f"{filtered['sr_p'].mean():.1f}", f"Baseline: {filtered['sr_all'].mean():.1f}", "positive")
top_rva_player = filtered.sort_values(by='total_rva_p', ascending=False).iloc[0]
render_kpi(k3, "Top Total RVA", f"+{top_rva_player['total_rva_p']:.1f}", f"{top_rva_player['striker_name']}", "positive")
top_acc_player = filtered.sort_values(by='delta_sr', ascending=False).iloc[0]
render_kpi(k4, "Top Accelerator (ΔSR)", f"+{top_acc_player['delta_sr']:.1f}", f"{top_acc_player['striker_name']}", "positive")

# Leaderboard Table
st.markdown("---")
st.markdown("### 📋 Interactive Batting Leaderboard")

display_cols = [
    'rank', 'striker_name', 'striker_id', 'balls_p', 'runs_p',
    'sr_p', 'sr_all', 'delta_sr', 'avg_p', 'dot_pct_p',
    'bnd_pct_p', 'win_impact_pct', 'total_rva_p', 'PRI'
]
table_df = filtered[display_cols].copy()
table_df.columns = [
    'Rank', 'Batter', 'ID', 'Balls (P)', 'Runs (P)',
    'Pressure SR', 'Base SR', 'Δ SR', 'Pressure Avg', 'Dot %',
    'Bnd %', 'Win Impact %', 'Total RVA', 'PRI Score'
]

st.dataframe(
    table_df.style.format({
        'Pressure SR': '{:.1f}',
        'Base SR': '{:.1f}',
        'Δ SR': '{:+.1f}',
        'Pressure Avg': '{:.1f}',
        'Dot %': '{:.1f}%',
        'Bnd %': '{:.1f}%',
        'Win Impact %': '{:.1f}%',
        'Total RVA': '{:+.1f}',
        'PRI Score': '{:.1f}'
    }).background_gradient(subset=['PRI Score'], cmap='YlGn')
      .background_gradient(subset=['Δ SR'], cmap='coolwarm', vmin=-10, vmax=10),
    use_container_width=True,
    height=420,
    hide_index=True
)

# Download CSV Button
csv_data = table_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Batting Leaderboard (CSV)",
    data=csv_data,
    file_name="superr_selector_batting_leaderboard.csv",
    mime="text/csv"
)

# Visualizations Section
st.markdown("---")
st.markdown("### 📈 Analytical Visualizations")

chart_tab1, chart_tab2, chart_tab3 = st.tabs([
    "🎯 Strike Rate vs Acceleration (ΔSR)",
    "📊 Total Situational Run Value Added (RVA)",
    "⚡ Dot Ball % vs Boundary % Frontier"
])

with chart_tab1:
    st.markdown("#### Quadrant Analysis: Who Thrives When the Required Rate Escalates?")
    median_sr = float(filtered['sr_p'].median())
    fig_scatter = plot_scatter(
        df=filtered,
        x_col='sr_p',
        y_col='delta_sr',
        text_col='striker_name',
        color_col='PRI',
        size_col='balls_p',
        title="Pressure Strike Rate vs Acceleration (Bubble Size = Pressure Balls)",
        x_label="Pressure Strike Rate",
        y_label="Acceleration Δ SR (Pressure SR - Baseline SR)",
        vline=median_sr,
        hline=0.0
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with chart_tab2:
    st.markdown("#### Cumulative Match Value: Top 15 Batters by Situational Run Value Added (RVA)")
    top15_rva = bat_df.sort_values(by='total_rva_p', ascending=False).head(15)
    fig_bar = plot_horizontal_bar(
        df=top15_rva,
        x_col='total_rva_p',
        y_col='striker_name',
        title="Top 15 Batters by Total Situational RVA Added",
        x_label="Total RVA (Runs Added Above Contextual Par)",
        color_col='PRI',
        height=480
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_tab3:
    st.markdown("#### Boundary Hunter vs Dot Ball Minimizer: The Pressure Trade-off Frontier")
    median_dot = float(filtered['dot_pct_p'].median())
    median_bnd = float(filtered['bnd_pct_p'].median())
    fig_tradeoff = plot_scatter(
        df=filtered,
        x_col='dot_pct_p',
        y_col='bnd_pct_p',
        text_col='striker_name',
        color_col='PRI',
        size_col='balls_p',
        title="Dot Ball % vs Boundary % (Optimal Zone: High Boundary, Low Dot)",
        x_label="Dot Ball Percentage (Lower is Better)",
        y_label="Boundary Percentage (Higher is Better)",
        vline=median_dot,
        hline=median_bnd
    )
    st.plotly_chart(fig_tradeoff, use_container_width=True)

