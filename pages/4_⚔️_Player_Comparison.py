import streamlit as st
import pandas as pd
import numpy as np
from utils.styling import apply_custom_theme, render_header, render_kpi, render_callout
from utils.data_loader import load_batters_data, load_bowlers_data
from utils.visualizations import plot_multi_player_radar, THEME

st.set_page_config(page_title="Player Comparison Lab | SUPERR SELECTOR", page_icon="⚔️", layout="wide")
apply_custom_theme()

render_header(
    title="PLAYER COMPARISON LAB",
    subtitle="Head-to-Head Multi-Player Pressure Diagnostics, Radar Overlays & Algorithmic Verdicts",
    tag="Tactical Head-to-Head"
)

bat_df = load_batters_data()
bowl_df = load_bowlers_data()

# Comparison Mode Selector
comp_mode = st.radio("Select Discipline to Compare", ["🏏 Batters", "🎯 Bowlers"], horizontal=True)

# Helper function to min-max normalize
def norm(val, v_min, v_max):
    return float(np.clip((val - v_min) / (v_max - v_min) * 100, 5, 98))

if comp_mode == "🏏 Batters":
    st.markdown("### ⚔️ Compare 2 to 5 Batters")

    # Preset selection
    preset_choice = st.selectbox(
        "Load Pre-Configured Tactical Archetypes (Optional):",
        ["Custom Selection", "Elite Finishers (Dhir, Shashank, David, Karthik)", "Anchor Superstars (Kohli, Buttler, Gaikwad, SKY)", "Explosive Disruptors (Pant, Kishan, Dhir)"]
    )

    all_batters = bat_df['striker_name'].tolist()
    if preset_choice == "Elite Finishers (Dhir, Shashank, David, Karthik)":
        default_selected = [p for p in ["Naman Dhir", "Shashank Singh", "Tim David", "Dinesh Karthik"] if p in all_batters]
    elif preset_choice == "Anchor Superstars (Kohli, Buttler, Gaikwad, SKY)":
        default_selected = [p for p in ["Virat Kohli", "Jos Buttler", "Ruturaj Gaikwad", "Suryakumar Yadav"] if p in all_batters]
    elif preset_choice == "Explosive Disruptors (Pant, Kishan, Dhir)":
        default_selected = [p for p in ["Rishabh Pant", "Ishan Kishan", "Naman Dhir"] if p in all_batters]
    else:
        default_selected = ["Naman Dhir", "Shashank Singh", "Suryakumar Yadav"]

    selected_players = st.multiselect(
        "Choose Batters (2 to 5)",
        options=all_batters,
        default=default_selected,
        max_selections=5
    )

    if len(selected_players) < 2:
        st.info("Please select at least 2 batters to activate head-to-head comparison.")
        st.stop()

    comp_df = bat_df[bat_df['striker_name'].isin(selected_players)].copy()

    # Radar Comparison
    st.markdown("---")
    r_col, table_col = st.columns([1.1, 1])

    cat_labels = ["Pressure SR", "Acceleration (ΔSR)", "Boundary %", "Low Dot %", "Pressure Avg", "RVA Rate"]
    radar_data = {}
    for _, row in comp_df.iterrows():
        radar_data[row['striker_name']] = [
            norm(row['sr_p'], 110, 210),
            norm(row['delta_sr'], -15, 25),
            norm(row['bnd_pct_p'], 10, 32),
            norm(100 - row['dot_pct_p'], 50, 85),
            norm(row['avg_p'], 15, 60),
            norm(row['rva_per_100'], -15, 30)
        ]

    with r_col:
        st.markdown("#### 🕸️ Multi-Player Pressure Radar Overlay")
        fig_multi = plot_multi_player_radar(cat_labels, radar_data)
        st.plotly_chart(fig_multi, use_container_width=True)

    with table_col:
        st.markdown("#### 📋 Side-by-Side Statistical Matrix")
        metrics_display = comp_df[[
            'striker_name', 'rank', 'PRI', 'sr_p', 'delta_sr',
            'bnd_pct_p', 'dot_pct_p', 'avg_p', 'total_rva_p', 'win_impact_pct'
        ]].copy()
        metrics_display.columns = [
            'Batter', 'Rank', 'PRI', 'Pressure SR', 'Δ SR',
            'Bnd %', 'Dot %', 'Avg (P)', 'Total RVA', 'Win %'
        ]

        # Transpose for easier side-by-side reading
        t_metrics = metrics_display.set_index('Batter').T
        st.dataframe(
            t_metrics.style.format('{:.1f}'),
            use_container_width=True,
            height=380
        )

    # Automated Head-to-Head Analytical Verdict
    st.markdown("---")
    st.markdown("### 🧠 Automated Tactical Verdict")
    best_pri = comp_df.sort_values(by='PRI', ascending=False).iloc[0]
    best_acc = comp_df.sort_values(by='delta_sr', ascending=False).iloc[0]
    best_bnd = comp_df.sort_values(by='bnd_pct_p', ascending=False).iloc[0]
    best_rva = comp_df.sort_values(by='total_rva_p', ascending=False).iloc[0]

    verdict_text = (
        f"Among the selected cohort, <strong>{best_pri['striker_name']}</strong> holds the highest comprehensive rating (PRI: {best_pri['PRI']:.1f}, Rank #{int(best_pri['rank'])}). "
        f"For raw acceleration when the required rate surges, <strong>{best_acc['striker_name']}</strong> delivers the highest leap (+{best_acc['delta_sr']:.1f} SR above baseline). "
        f"If pure boundary power is required, <strong>{best_bnd['striker_name']}</strong> leads with {best_bnd['bnd_pct_p']:.1f}% boundary share. "
        f"In cumulative match value, <strong>{best_rva['striker_name']}</strong> has accumulated +{best_rva['total_rva_p']:.1f} Total RVA across high-pressure situations."
    )
    render_callout(verdict_text, title="ALGORITHMIC SCOUTING ASSESSMENT")

else:
    st.markdown("### ⚔️ Compare 2 to 5 Bowlers")

    # Preset selection
    preset_choice = st.selectbox(
        "Load Pre-Configured Tactical Archetypes (Optional):",
        ["Custom Selection", "Death Specialists (Bumrah, Shaheen, Nawaz, Santner)", "Spin Maestros (Narine, Rashid Khan, Abrar, Mujeeb)", "Subcontinent Enforcers (Nawaz, Shadab, Abrar)"]
    )

    all_bowlers = bowl_df['bowler_name'].tolist()
    if preset_choice == "Death Specialists (Bumrah, Shaheen, Nawaz, Santner)":
        default_selected = [p for p in ["Jasprit Bumrah", "Shaheen Afridi", "Mohammad Nawaz", "Mitchell Santner"] if p in all_bowlers]
    elif preset_choice == "Spin Maestros (Narine, Rashid Khan, Abrar, Mujeeb)":
        default_selected = [p for p in ["Sunil Narine", "Rashid Khan", "Abrar Ahmed", "Mujeeb Ur Rahman"] if p in all_bowlers]
    elif preset_choice == "Subcontinent Enforcers (Nawaz, Shadab, Abrar)":
        default_selected = [p for p in ["Mohammad Nawaz", "Shadab Khan", "Abrar Ahmed"] if p in all_bowlers]
    else:
        default_selected = ["Mohammad Nawaz", "Sunil Narine", "Jasprit Bumrah"]

    selected_players = st.multiselect(
        "Choose Bowlers (2 to 5)",
        options=all_bowlers,
        default=default_selected,
        max_selections=5
    )

    if len(selected_players) < 2:
        st.info("Please select at least 2 bowlers to activate head-to-head comparison.")
        st.stop()

    comp_df = bowl_df[bowl_df['bowler_name'].isin(selected_players)].copy()

    # Radar Comparison
    st.markdown("---")
    r_col, table_col = st.columns([1.1, 1])

    bw_cat_labels = ["Containment (Econ)", "Phase Savings", "Wicket Frequency", "Dot Ball %", "Death Share %", "BVA Rate"]
    radar_data = {}
    for _, row in comp_df.iterrows():
        radar_data[row['bowler_name']] = [
            norm(12.0 - row['econ_p'], 2.0, 6.0),
            norm(row['phase_delta_econ'], -2.0, 2.5),
            norm(35.0 - row['sr_p'], 5.0, 25.0),
            norm(row['dot_pct_p'], 20.0, 55.0),
            norm(row['death_share'], 0.0, 70.0),
            norm(row['bva_per_100'], -15.0, 25.0)
        ]

    with r_col:
        st.markdown("#### 🕸️ Multi-Player Pressure Radar Overlay")
        fig_multi_bw = plot_multi_player_radar(bw_cat_labels, radar_data)
        st.plotly_chart(fig_multi_bw, use_container_width=True)

    with table_col:
        st.markdown("#### 📋 Side-by-Side Statistical Matrix")
        bw_metrics_display = comp_df[[
            'bowler_name', 'rank', 'PRI', 'econ_p', 'phase_delta_econ',
            'death_share', 'dot_pct_p', 'sr_p', 'total_bva_p', 'win_impact_pct'
        ]].copy()
        bw_metrics_display.columns = [
            'Bowler', 'Rank', 'PRI', 'Pressure Econ', 'Phase ΔEcon',
            'Death %', 'Dot %', 'Wkt SR', 'Total BVA', 'Win %'
        ]

        t_bw_metrics = bw_metrics_display.set_index('Bowler').T
        st.dataframe(
            t_bw_metrics.style.format('{:.2f}'),
            use_container_width=True,
            height=380
        )

    # Automated Head-to-Head Analytical Verdict
    st.markdown("---")
    st.markdown("### 🧠 Automated Tactical Verdict")
    best_pri_bw = comp_df.sort_values(by='PRI', ascending=False).iloc[0]
    best_phase_bw = comp_df.sort_values(by='phase_delta_econ', ascending=False).iloc[0]
    best_death_bw = comp_df.sort_values(by='death_share', ascending=False).iloc[0]
    best_bva_bw = comp_df.sort_values(by='total_bva_p', ascending=False).iloc[0]

    bw_verdict_text = (
        f"Among the selected bowlers, <strong>{best_pri_bw['bowler_name']}</strong> secures the highest overall rating (PRI: {best_pri_bw['PRI']:.1f}, Rank #{int(best_pri_bw['rank'])}). "
        f"In terms of contextual containment vs phase expectations, <strong>{best_phase_bw['bowler_name']}</strong> saves the most runs (+{best_phase_bw['phase_delta_econ']:+.2f} RPO vs par). "
        f"If the assignment is specialized death overs (16–20), <strong>{best_death_bw['bowler_name']}</strong> shoulders the heaviest workload ({best_death_bw['death_share']:.1f}% death share). "
        f"In aggregate match-winning contribution, <strong>{best_bva_bw['bowler_name']}</strong> leads with +{best_bva_bw['total_bva_p']:.1f} Total BVA."
    )
    render_callout(bw_verdict_text, title="ALGORITHMIC SCOUTING ASSESSMENT")

