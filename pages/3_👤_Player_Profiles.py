import streamlit as st
import pandas as pd
import numpy as np
from utils.styling import apply_custom_theme, render_header, render_kpi, render_callout
from utils.data_loader import (
    load_batters_data, load_bowlers_data, get_all_players_catalog,
    load_match_logs_bat, load_match_logs_bowl, load_player_splits
)
from utils.visualizations import plot_radar_chart, THEME

st.set_page_config(page_title="Player Profiles | SUPERR SELECTOR", page_icon="👤", layout="wide")
apply_custom_theme()

catalog = get_all_players_catalog()
bat_df = load_batters_data()
bowl_df = load_bowlers_data()
logs_bat = load_match_logs_bat()
logs_bowl = load_match_logs_bowl()
splits = load_player_splits()

render_header(
    title="INDIVIDUAL PLAYER DOSSIER",
    subtitle="Deep-Dive Pressure Diagnostics, Situational Splits & Complete Match-by-Match Logs",
    tag="Scouting & Player Profiling"
)

# Search & Select Bar
st.markdown("### 🔍 Select a Player to Inspect")
all_names = sorted(list(catalog.keys()))
default_idx = all_names.index("Naman Dhir") if "Naman Dhir" in all_names else 0

selected_name = st.selectbox(
    "Choose a Player",
    options=all_names,
    index=default_idx,
    help="Select from 183 officially analyzed players."
)

p_info = catalog[selected_name]
p_id = p_info['player_id']

# Player Header Banner
badge_color = "#F59E0B" if (p_info['bat_rank'] == 1 or p_info['bowl_rank'] == 1) else "#E91E63"
st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); padding: 22px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
        <div style="display: flex; align-items: center; gap: 18px;">
            <div style="width: 58px; height: 58px; border-radius: 50%; background: linear-gradient(135deg, {badge_color}, #9C27B0); display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 800; color: #fff; box-shadow: 0 4px 15px rgba(0,0,0,0.4);">
                {selected_name[0]}
            </div>
            <div>
                <div style="font-size: 24px; font-weight: 800; color: #FFFFFF;">{selected_name}</div>
                <div style="font-size: 13px; color: #94A3B8; margin-top: 3px;">
                    Player ID: <span style="color: #38BDF8; font-family: monospace;">{p_id}</span> • 
                    Role: <span style="color: #10B981; font-weight: 600;">{p_info['primary_role']}</span> • 
                    Teams: <span style="color: #E2E8F0;">{p_info['teams']}</span>
                </div>
            </div>
        </div>
        <div style="display: flex; gap: 14px;">
            {f'''<div style="background: rgba(233, 30, 99, 0.15); border: 1px solid #E91E63; border-radius: 8px; padding: 10px 18px; text-align: center;">
                <div style="font-size: 11px; color: #FF80AB; text-transform: uppercase; font-weight: 700;">Batter Rank</div>
                <div style="font-size: 20px; font-weight: 800; color: #fff;">#{p_info['bat_rank']} <span style="font-size: 13px; color: #94A3B8;">(PRI {p_info['bat_pri']:.1f})</span></div>
            </div>''' if p_info['is_ranked_bat'] else ''}
            {f'''<div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; border-radius: 8px; padding: 10px 18px; text-align: center;">
                <div style="font-size: 11px; color: #6EE7B7; text-transform: uppercase; font-weight: 700;">Bowler Rank</div>
                <div style="font-size: 20px; font-weight: 800; color: #fff;">#{p_info['bowl_rank']} <span style="font-size: 13px; color: #94A3B8;">(PRI {p_info['bowl_pri']:.1f})</span></div>
            </div>''' if p_info['is_ranked_bowl'] else ''}
        </div>
    </div>
""", unsafe_allow_html=True)

# Selectable Profile Tabs based on role
available_tabs = []
if p_info['is_ranked_bat']:
    available_tabs.append("🏏 Batting Dossier")
if p_info['is_ranked_bowl']:
    available_tabs.append("🎯 Bowling Dossier")

if not available_tabs:
    st.warning("This player does not meet the minimum sample size threshold (60 pressure balls) for official ranking.")
    st.stop()

tabs = st.tabs(available_tabs)

# Helper function to min-max normalize
def norm(val, v_min, v_max):
    return float(np.clip((val - v_min) / (v_max - v_min) * 100, 5, 98))

# ==================== BATTING TAB ====================
if p_info['is_ranked_bat']:
    tab_bat = tabs[0]
    with tab_bat:
        b_data = bat_df[bat_df['striker_id'] == p_id].iloc[0]

        # Top KPI Row
        bk1, bk2, bk3, bk4, bk5, bk6 = st.columns(6)
        render_kpi(bk1, "Pressure Balls", f"{int(b_data['balls_p'])}", f"{int(b_data['balls_all'])} total balls", "neutral")
        render_kpi(bk2, "Pressure Runs", f"{int(b_data['runs_p'])}", f"{int(b_data['runs_all'])} total runs", "neutral")
        render_kpi(bk3, "Pressure SR", f"{b_data['sr_p']:.1f}", f"Base SR: {b_data['sr_all']:.1f}", "positive" if b_data['sr_p'] >= b_data['sr_all'] else "negative")
        render_kpi(bk4, "Acceleration (ΔSR)", f"{b_data['delta_sr']:+.1f}", "vs Baseline SR", "positive" if b_data['delta_sr'] >= 0 else "negative")
        render_kpi(bk5, "Total RVA", f"{b_data['total_rva_p']:+.1f}", f"{b_data['rva_per_100']:+.1f} / 100b", "positive" if b_data['total_rva_p'] >= 0 else "negative")
        render_kpi(bk6, "Win Impact %", f"{b_data['win_impact_pct']:.1f}%", f"Involved matches", "positive")

        # Two-Column Section: Radar & Archetype
        st.markdown("---")
        b_col_radar, b_col_splits = st.columns([1.1, 1])

        with b_col_radar:
            st.markdown("#### 🕸️ 6-Dimensional Pressure Fingerprint")
            cat_labels = ["Pressure SR", "Acceleration (ΔSR)", "Boundary %", "Low Dot %", "Pressure Avg", "RVA Rate"]
            p_vals = [
                norm(b_data['sr_p'], 110, 210),
                norm(b_data['delta_sr'], -15, 25),
                norm(b_data['bnd_pct_p'], 10, 32),
                norm(100 - b_data['dot_pct_p'], 50, 85),
                norm(b_data['avg_p'], 15, 60),
                norm(b_data['rva_per_100'], -15, 30)
            ]
            bench_vals = [
                norm(bat_df['sr_p'].median(), 110, 210),
                norm(bat_df['delta_sr'].median(), -15, 25),
                norm(bat_df['bnd_pct_p'].median(), 10, 32),
                norm(100 - bat_df['dot_pct_p'].median(), 50, 85),
                norm(bat_df['avg_p'].median(), 15, 60),
                norm(bat_df['rva_per_100'].median(), -15, 30)
            ]
            fig_r = plot_radar_chart(cat_labels, p_vals, bench_vals, selected_name, "Cohort Median")
            st.plotly_chart(fig_r, use_container_width=True)

        with b_col_splits:
            st.markdown("#### ⚡ Situational Splits (Pressure)")
            
            # Phase Split
            b_ph = splits['bat_phase'][(splits['bat_phase']['striker_id'] == p_id) & (splits['bat_phase']['is_pressure'])].copy()
            if len(b_ph) > 0:
                b_ph['SR'] = (b_ph['runs'] / b_ph['balls'] * 100).round(1)
                b_ph['Dot %'] = (b_ph['dots'] / b_ph['balls'] * 100).round(1)
                st.markdown("**By Match Phase:**")
                st.dataframe(
                    b_ph[['phase', 'balls', 'runs', 'SR', 'Dot %', 'rva']].rename(columns={
                        'phase': 'Phase', 'balls': 'Balls', 'runs': 'Runs', 'rva': 'RVA'
                    }).style.format({'SR': '{:.1f}', 'Dot %': '{:.1f}%', 'RVA': '{:+.1f}'}),
                    use_container_width=True,
                    hide_index=True
                )

            # Pace vs Spin
            b_pc = splits['bat_pace'][(splits['bat_pace']['striker_id'] == p_id) & (splits['bat_pace']['is_pressure'])].copy()
            if len(b_pc) > 0:
                b_pc['SR'] = (b_pc['runs'] / b_pc['balls'] * 100).round(1)
                st.markdown("**By Bowling Type:**")
                st.dataframe(
                    b_pc[['pace_or_spin', 'balls', 'runs', 'SR', 'rva']].rename(columns={
                        'pace_or_spin': 'Type', 'balls': 'Balls', 'runs': 'Runs', 'rva': 'RVA'
                    }).style.format({'SR': '{:.1f}', 'RVA': '{:+.1f}'}),
                    use_container_width=True,
                    hide_index=True
                )

        # Match Logs
        st.markdown("---")
        st.markdown("#### 📜 Match-by-Match Performance Log")
        p_bat_logs = logs_bat[logs_bat['striker_id'] == p_id].copy()
        if len(p_bat_logs) > 0:
            p_bat_logs['Match Result'] = np.where(p_bat_logs['is_win'], 'Won', 'Lost')
            disp_logs = p_bat_logs[[
                'match_date', 'comp_name', 'bowl_team_name', 'stage',
                'balls_p', 'runs_p', 'sr_p', 'rva_p', 'balls_all', 'runs_all', 'Match Result'
            ]].copy()
            disp_logs.columns = [
                'Date', 'Tournament', 'Opponent', 'Stage',
                'Balls (P)', 'Runs (P)', 'SR (P)', 'RVA (P)', 'Total Balls', 'Total Runs', 'Result'
            ]
            st.dataframe(
                disp_logs.style.format({
                    'SR (P)': lambda x: f"{x:.1f}" if pd.notna(x) else "-",
                    'RVA (P)': '{:+.1f}'
                }).map(lambda v: 'color: #10B981; font-weight: 700;' if v == 'Won' else 'color: #EF4444;', subset=['Result']),
                use_container_width=True,
                height=350,
                hide_index=True
            )

# ==================== BOWLING TAB ====================
if p_info['is_ranked_bowl']:
    tab_bowl = tabs[1] if (p_info['is_ranked_bat'] and len(tabs) > 1) else tabs[0]
    with tab_bowl:
        bw_data = bowl_df[bowl_df['bowler_id'] == p_id].iloc[0]

        # Top KPI Row
        bw1, bw2, bw3, bw4, bw5, bw6 = st.columns(6)
        render_kpi(bw1, "Pressure Balls", f"{int(bw_data['balls_p'])}", f"{int(bw_data['balls_all'])} total balls", "neutral")
        render_kpi(bw2, "Pressure Wickets", f"{int(bw_data['wickets_p'])}", f"Strike Rate: {bw_data['sr_p']:.1f}b", "positive")
        render_kpi(bw3, "Pressure Economy", f"{bw_data['econ_p']:.2f}", f"Base Econ: {bw_data['econ_all']:.2f}", "positive" if bw_data['econ_p'] <= bw_data['econ_all'] else "negative")
        render_kpi(bw4, "Phase ΔEcon", f"{bw_data['phase_delta_econ']:+.2f}", "Runs saved/ov vs par", "positive" if bw_data['phase_delta_econ'] >= 0 else "negative")
        render_kpi(bw5, "Total BVA", f"{bw_data['total_bva_p']:+.1f}", f"{bw_data['bva_per_100']:+.1f} / 100b", "positive" if bw_data['total_bva_p'] >= 0 else "negative")
        render_kpi(bw6, "Death Share %", f"{bw_data['death_share']:.1f}%", f"{int(bw_data['death_balls'])} death balls", "neutral")

        # Two-Column Section: Radar & Splits
        st.markdown("---")
        bw_col_radar, bw_col_splits = st.columns([1.1, 1])

        with bw_col_radar:
            st.markdown("#### 🕸️ 6-Dimensional Pressure Fingerprint")
            bw_cat_labels = ["Containment (Econ)", "Phase Savings", "Wicket Frequency", "Dot Ball %", "Death Share %", "BVA Rate"]
            bw_p_vals = [
                norm(12.0 - bw_data['econ_p'], 2.0, 6.0),
                norm(bw_data['phase_delta_econ'], -2.0, 2.5),
                norm(35.0 - bw_data['sr_p'], 5.0, 25.0),
                norm(bw_data['dot_pct_p'], 20.0, 55.0),
                norm(bw_data['death_share'], 0.0, 70.0),
                norm(bw_data['bva_per_100'], -15.0, 25.0)
            ]
            bw_bench_vals = [
                norm(12.0 - bowl_df['econ_p'].median(), 2.0, 6.0),
                norm(bowl_df['phase_delta_econ'].median(), -2.0, 2.5),
                norm(35.0 - bowl_df['sr_p'].median(), 5.0, 25.0),
                norm(bowl_df['dot_pct_p'].median(), 20.0, 55.0),
                norm(bowl_df['death_share'].median(), 0.0, 70.0),
                norm(bowl_df['bva_per_100'].median(), -15.0, 25.0)
            ]
            fig_bw_r = plot_radar_chart(bw_cat_labels, bw_p_vals, bw_bench_vals, selected_name, "Cohort Median")
            st.plotly_chart(fig_bw_r, use_container_width=True)

        with bw_col_splits:
            st.markdown("#### ⚡ Situational Splits (Pressure)")
            
            # Phase Split
            bw_ph = splits['bowl_phase'][(splits['bowl_phase']['bowler_id'] == p_id) & (splits['bowl_phase']['is_pressure'])].copy()
            if len(bw_ph) > 0:
                bw_ph['Econ'] = (bw_ph['runs'] / (bw_ph['balls'] / 6)).round(2)
                bw_ph['Dot %'] = (bw_ph['dots'] / bw_ph['balls'] * 100).round(1)
                st.markdown("**By Match Phase:**")
                st.dataframe(
                    bw_ph[['phase', 'balls', 'runs', 'wkts', 'Econ', 'Dot %', 'bva']].rename(columns={
                        'phase': 'Phase', 'balls': 'Balls', 'runs': 'Runs', 'wkts': 'Wkts', 'bva': 'BVA'
                    }).style.format({'Econ': '{:.2f}', 'Dot %': '{:.1f}%', 'BVA': '{:+.1f}'}),
                    use_container_width=True,
                    hide_index=True
                )

            # Batter Handedness Split
            bw_hd = splits['bowl_hand'][(splits['bowl_hand']['bowler_id'] == p_id) & (splits['bowl_hand']['is_pressure'])].copy()
            if len(bw_hd) > 0:
                bw_hd['Econ'] = (bw_hd['runs'] / (bw_hd['balls'] / 6)).round(2)
                st.markdown("**By Batter Hand:**")
                st.dataframe(
                    bw_hd[['batting_type', 'balls', 'runs', 'wkts', 'Econ', 'bva']].rename(columns={
                        'batting_type': 'Batter Hand', 'balls': 'Balls', 'runs': 'Runs', 'wkts': 'Wkts', 'bva': 'BVA'
                    }).style.format({'Econ': '{:.2f}', 'BVA': '{:+.1f}'}),
                    use_container_width=True,
                    hide_index=True
                )

        # Match Logs
        st.markdown("---")
        st.markdown("#### 📜 Match-by-Match Performance Log")
        p_bowl_logs = logs_bowl[logs_bowl['bowler_id'] == p_id].copy()
        if len(p_bowl_logs) > 0:
            p_bowl_logs['Match Result'] = np.where(p_bowl_logs['is_win'], 'Won', 'Lost')
            disp_bw_logs = p_bowl_logs[[
                'match_date', 'comp_name', 'bat_team_name', 'stage',
                'balls_p', 'runs_p', 'wkts_p', 'econ_p', 'bva_p', 'balls_all', 'runs_all', 'wkts_all', 'Match Result'
            ]].copy()
            disp_bw_logs.columns = [
                'Date', 'Tournament', 'Opponent', 'Stage',
                'Balls (P)', 'Runs (P)', 'Wkts (P)', 'Econ (P)', 'BVA (P)', 'Total Balls', 'Total Runs', 'Total Wkts', 'Result'
            ]
            st.dataframe(
                disp_bw_logs.style.format({
                    'Econ (P)': lambda x: f"{x:.2f}" if pd.notna(x) else "-",
                    'BVA (P)': '{:+.1f}'
                }).map(lambda v: 'color: #10B981; font-weight: 700;' if v == 'Won' else 'color: #EF4444;', subset=['Result']),
                use_container_width=True,
                height=350,
                hide_index=True
            )
