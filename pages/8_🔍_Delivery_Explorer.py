import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.styling import apply_custom_theme, render_header, render_kpi, render_callout
from utils.data_loader import load_enriched_sample
from utils.visualizations import apply_chart_theme, THEME

st.set_page_config(page_title="Delivery-Level Explorer | SUPERR SELECTOR", page_icon="🔍", layout="wide")
apply_custom_theme()

render_header(
    title="DELIVERY-LEVEL EXPLORER",
    subtitle="Interactive Granular Audit of Expected Runs, Wicket Hazards & Real-Time RVA / BVA",
    tag="Deep Physics & Delivery Science"
)

# Load sample
sample_bbb = load_enriched_sample(n=25000)

# Filter Controls Bar
st.markdown("### 🎛️ Filter Delivery Sample (25,000 Deliveries)")
f1, f2, f3, f4, f5 = st.columns(5)

with f1:
    pressure_filter = st.selectbox("Situation Type", ["All Deliveries", "High Pressure Only", "Ordinary Play Only"], index=1)

with f2:
    phase_filter = st.selectbox("Match Phase", ["All Phases", "Powerplay (1-6)", "Middle (7-15)", "Death (16-20)"], index=0)

with f3:
    bowler_type = st.selectbox("Bowling Category", ["All", "Pace", "Spin"])

with f4:
    outcome_filter = st.selectbox("Event Outcome", ["All Events", "Boundaries (4s/6s)", "Wickets Only", "Dot Balls (0 Runs)"])

with f5:
    max_rows = st.selectbox("Display Limit", [20, 50, 100, 200], index=1)

# Apply filters
df_view = sample_bbb.copy()

if pressure_filter == "High Pressure Only":
    df_view = df_view[df_view['is_pressure']]
elif pressure_filter == "Ordinary Play Only":
    df_view = df_view[~df_view['is_pressure']]

if phase_filter != "All Phases":
    phase_name = phase_filter.split(" ")[0].lower()
    df_view = df_view[df_view['phase'].str.lower() == phase_name]

if bowler_type != "All":
    df_view = df_view[df_view['pace_or_spin'].str.lower() == bowler_type.lower()]

if outcome_filter == "Boundaries (4s/6s)":
    df_view = df_view[df_view['runs'] >= 4]
elif outcome_filter == "Wickets Only":
    df_view = df_view[df_view['is_wicket']]
elif outcome_filter == "Dot Balls (0 Runs)":
    df_view = df_view[df_view['runs'] == 0]

# KPI Summary
k1, k2, k3, k4 = st.columns(4)
render_kpi(k1, "Deliveries Matching", f"{len(df_view):,}", f"From 25,000 sample", "neutral")
avg_rva = df_view['bat_rva'].mean() if len(df_view) > 0 else 0
render_kpi(k2, "Mean Batter RVA", f"{avg_rva:+.2f}", "Runs added per ball", "positive" if avg_rva >= 0 else "negative")
avg_speed = df_view['bowl_speed'].dropna().mean() if 'bowl_speed' in df_view and len(df_view['bowl_speed'].dropna()) > 0 else 0
render_kpi(k3, "Mean Ball Speed", f"{avg_speed:.1f} km/h" if avg_speed > 0 else "N/A", "Radar tracking", "neutral")
wkt_count = int(df_view['is_wicket'].sum())
render_kpi(k4, "Wickets in View", f"{wkt_count}", f"{(wkt_count/len(df_view)*100):.1f}% hazard rate" if len(df_view)>0 else "-", "neutral")

# Granular Table View
st.markdown("---")
st.markdown("### 📋 Delivery Log Data")

display_cols = [
    'overid', 'over_ball_num', 'striker_name', 'bowler_name',
    'pace_or_spin', 'stroke', 'runs', 'is_wicket',
    'exp_runs', 'bat_rva', 'bowl_bva', 'is_pressure'
]
avail_cols = [c for c in display_cols if c in df_view.columns]
clean_table = df_view[avail_cols].head(max_rows).copy()
clean_table['Over.Ball'] = clean_table['overid'].astype(str) + "." + clean_table['over_ball_num'].astype(str)
cols_order = ['Over.Ball', 'striker_name', 'bowler_name', 'pace_or_spin', 'stroke', 'runs', 'is_wicket', 'exp_runs', 'bat_rva', 'bowl_bva', 'is_pressure']
clean_table = clean_table[[c for c in cols_order if c in clean_table.columns]]

clean_table.columns = [
    'Over', 'Striker', 'Bowler', 'Type', 'Shot / Stroke',
    'Runs', 'Wicket', 'Exp Runs', 'Bat RVA', 'Bowl BVA', 'Pressure Flag'
]

st.dataframe(
    clean_table.style.format({
        'Exp Runs': '{:.2f}',
        'Bat RVA': '{:+.2f}',
        'Bowl BVA': '{:+.2f}'
    }).map(lambda v: 'background-color: rgba(233, 30, 99, 0.2); font-weight: 700;' if v else '', subset=['Wicket']),
    use_container_width=True,
    height=420,
    hide_index=True
)

# Analytical Charts
st.markdown("---")
st.markdown("### 📊 Delivery Dynamics & Shot Archetypes")

d_col1, d_col2 = st.columns(2)

with d_col1:
    if 'stroke' in df_view and df_view['stroke'].dropna().nunique() > 1:
        top_strokes = df_view['stroke'].value_counts().head(10).reset_index()
        top_strokes.columns = ['Stroke Type', 'Delivery Count']
        fig_stroke = px.bar(
            top_strokes, x='Delivery Count', y='Stroke Type', orientation='h',
            title="Most Frequent Shot Types in Filtered Situation",
            color='Delivery Count', color_continuous_scale='Tealgrn'
        )
        st.plotly_chart(apply_chart_theme(fig_stroke, height=400), use_container_width=True)
    else:
        st.info("Stroke type data not available for this subset.")

with d_col2:
    if 'bowl_speed' in df_view and df_view['bowl_speed'].dropna().nunique() > 5:
        speed_data = df_view.dropna(subset=['bowl_speed'])
        fig_speed = px.histogram(
            speed_data, x='bowl_speed', color='is_pressure',
            barmode='overlay', nbins=30,
            title="Bowling Speed Distribution (Pressure vs Standard)",
            color_discrete_map={True: THEME['pink'], False: THEME['cyan']}
        )
        st.plotly_chart(apply_chart_theme(fig_speed, height=400), use_container_width=True)
    else:
        st.info("Bowling speed distribution not populated for this slice.")
