import streamlit as st
import pandas as pd
import numpy as np
from utils.styling import (
    apply_custom_theme, render_header, render_kpi, render_callout,
    render_player_spotlight_card, THEME
)
from utils.data_loader import (
    load_batters_data, load_bowlers_data, get_all_players_catalog,
    load_match_logs_bat, load_match_logs_bowl, load_player_splits
)
from utils.visualizations import plot_radar_chart

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

# Search & Select Bar with Quick Filters
st.markdown("### 🔍 Select Player to Inspect")
all_names = sorted(list(catalog.keys()))

col_sel1, col_sel2 = st.columns([2.5, 1.5])
with col_sel1:
    default_idx = all_names.index("Naman Dhir") if "Naman Dhir" in all_names else 0
    selected_name = st.selectbox(
        "Choose a Player from Cohort (183 Players Evaluated)",
        options=all_names,
        index=default_idx
    )
with col_sel2:
    quick_star = st.selectbox(
        "⚡ Jump to Highlighted Star",
        ["Select Star...", "Naman Dhir (#1 Batter)", "Mohammad Nawaz (#1 Bowler)", "Jasprit Bumrah (#6 Bowler / Death King)", "Shashank Singh (#2 Batter)", "Sunil Narine (#3 Bowler)", "Rishabh Pant (#3 Batter)", "Virat Kohli (#8 Batter)"]
    )
    if quick_star != "Select Star...":
        star_clean = quick_star.split(" (")[0]
        if star_clean in all_names:
            selected_name = star_clean

p_info = catalog[selected_name]
p_id = p_info['player_id']

# Determine Tactical Archetype & Description
is_bat = p_info['is_ranked_bat']
is_bowl = p_info['is_ranked_bowl']

# Fetch stats
b_data = bat_df[bat_df['striker_id'] == p_id].iloc[0] if is_bat else None
bw_data = bowl_df[bowl_df['bowler_id'] == p_id].iloc[0] if is_bowl else None

# Determine Role Mode Toggle if All-Rounder
active_mode = "Batting"
if is_bat and is_bowl:
    active_mode = st.radio("Select Dossier View for All-Rounder", ["🏏 Batting Analysis", "🎯 Bowling Analysis"], horizontal=True)
elif is_bowl:
    active_mode = "🎯 Bowling Analysis"
else:
    active_mode = "🏏 Batting Analysis"

# Determine Archetype Tag
if "Batting" in active_mode and b_data is not None:
    if b_data['delta_sr'] > 12.0:
        archetype = "⚡ Elite Death Finisher & Disruptor"
        tactical_note = f"Accelerates by +{b_data['delta_sr']:.1f} SR when stakes peak, maintaining a massive {b_data['bnd_pct_p']:.1f}% boundary percentage."
    elif b_data['sr_p'] > 170.0:
        archetype = "💥 Power Boundary Finisher"
        tactical_note = f"Pure boundary power with a 170+ pressure strike rate and +{b_data['total_rva_p']:.1f} Total Situational RVA."
    elif b_data['total_rva_p'] > 35.0:
        archetype = "🎯 High-Volume Pressure Anchor"
        tactical_note = f"Exceptional cumulative match impact with +{b_data['total_rva_p']:.1f} Total RVA across extended pressure situations."
    else:
        archetype = "🏏 Middle-Overs Aggressor"
        tactical_note = "Reliable middle-overs strike rotator capable of boundary acceleration against spin."
    
    stats_ribbon = {
        "Pressure SR": f"{b_data['sr_p']:.1f}",
        "Δ SR (Accel)": f"{b_data['delta_sr']:+.1f}",
        "Boundary %": f"{b_data['bnd_pct_p']:.1f}%",
        "Dot Ball %": f"{b_data['dot_pct_p']:.1f}%",
        "Total RVA": f"{b_data['total_rva_p']:+.1f}",
        "Win Impact": f"{b_data['win_impact_pct']:.1f}%"
    }
    rank_val = int(b_data['rank'])
    pri_val = float(b_data['PRI'])
    role_type = "Batter"

else:
    if bw_data['death_share'] > 45.0:
        archetype = "💀 Generational Death Overs Specialist"
        tactical_note = f"Bears {bw_data['death_share']:.1f}% death workload, saving {bw_data['phase_delta_econ']:+.2f} runs/over against 10.56 RPO par."
    elif bw_data['phase_delta_econ'] > 1.8:
        archetype = "🛡️ High-Leverage Par Constrictor"
        tactical_note = f"Saves {bw_data['phase_delta_econ']:+.2f} runs/over vs situational par, denying boundaries in critical overs."
    elif bw_data['econ_p'] < 7.0:
        archetype = "🌀 Multi-Phase Mystery Spin Strangler"
        tactical_note = f"Stingy {bw_data['econ_p']:.2f} pressure economy, suffocating batting momentum."
    else:
        archetype = "🎯 Tactical Crisis Enforcer"
        tactical_note = "High wicket taking frequency under pressure with consistent dot-ball pressure."

    stats_ribbon = {
        "Pressure Econ": f"{bw_data['econ_p']:.2f}",
        "Phase ΔEcon": f"{bw_data['phase_delta_econ']:+.2f}",
        "Wicket SR": f"{bw_data['sr_p']:.1f}b",
        "Death Share": f"{bw_data['death_share']:.1f}%",
        "Total BVA": f"{bw_data['total_bva_p']:+.1f}",
        "Win Impact": f"{bw_data['win_impact_pct']:.1f}%"
    }
    rank_val = int(bw_data['rank'])
    pri_val = float(bw_data['PRI'])
    role_type = "Bowler"

# RENDER HERO TRADING CARD
render_player_spotlight_card(
    name=selected_name,
    player_id=p_id,
    rank=rank_val,
    pri=pri_val,
    role=role_type,
    archetype=archetype,
    teams=p_info['teams'],
    stats_dict=stats_ribbon,
    notes=tactical_note
)

# Helper function to min-max normalize for radar
def norm(val, v_min, v_max):
    return float(np.clip((val - v_min) / (v_max - v_min) * 100, 5, 98))

# ==================== FOUR HIGHLIGHT TABS ====================
tab_radar, tab_splits, tab_logs, tab_scout = st.tabs([
    "📊 1. Pressure Fingerprint & Radar",
    "⚡ 2. Situational Splits (Pace/Spin & Phase)",
    "📜 3. Match-by-Match Game Logs",
    "🧠 4. Franchise Scouting Blueprint"
])

# ----- TAB 1: RADAR & KPIS -----
with tab_radar:
    st.markdown("#### 🕸️ 6-Dimensional Pressure Fingerprint vs Cohort Benchmark")
    r_col_chart, r_col_analysis = st.columns([1.2, 1])

    if "Batting" in active_mode and b_data is not None:
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
        
        with r_col_chart:
            st.plotly_chart(fig_r, use_container_width=True)

        with r_col_analysis:
            st.markdown("##### 📌 Key Analytical Pillars")
            st.markdown(f"""
            - **Strike Rate Acceleration ($\Delta$SR):** `{b_data['delta_sr']:+.1f}` above baseline ({b_data['sr_p']:.1f} vs {b_data['sr_all']:.1f}).
            - **Boundary Dominance:** Generates a boundary every `{100/b_data['bnd_pct_p']:.1f}` deliveries under pressure.
            - **Dot Ball Resistance:** `{b_data['dot_pct_p']:.1f}%` dot balls ({'Superior to cohort' if b_data['dot_pct_p'] < bat_df['dot_pct_p'].median() else 'Room for rotational improvement'}).
            - **Net Match Impact:** Contributed `+{b_data['total_rva_p']:.1f}` Runs Above Contextual Par across `{int(b_data['balls_p'])}` pressure balls.
            """)
            render_callout(
                f"When the required rate rises above 9.5 RPO, {selected_name} exhibits an aggressive boundary trajectory, "
                f"yielding an estimated +{b_data['rva_per_100']:.1f} runs added per 100 balls above par.",
                title="SITUATIONAL ASSESSMENT"
            )

    elif bw_data is not None:
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
        
        with r_col_chart:
            st.plotly_chart(fig_bw_r, use_container_width=True)

        with r_col_analysis:
            st.markdown("##### 📌 Key Analytical Pillars")
            st.markdown(f"""
            - **Phase-Adjusted Par Savings:** `{bw_data['phase_delta_econ']:+.2f}` runs saved per over against contextual expectations.
            - **Pressure Economy Rate:** Concedes `{bw_data['econ_p']:.2f}` RPO under pressure (Baseline: `{bw_data['econ_all']:.2f}`).
            - **Death Overs Exposure:** `{bw_data['death_share']:.1f}%` of pressure deliveries bowled in overs 16–20.
            - **Net Bowling Value Added (BVA):** `+{bw_data['total_bva_p']:.1f}` cumulative match runs saved and wickets gained.
            """)
            render_callout(
                f"Under high-leverage death and chase situations, {selected_name} curtails boundaries, "
                f"saving approximately {bw_data['phase_delta_econ']:+.2f} runs per over relative to league average.",
                title="SITUATIONAL ASSESSMENT"
            )

# ----- TAB 2: SITUATIONAL SPLITS -----
with tab_splits:
    st.markdown("#### ⚡ Detailed Situational Splits Under Pressure")
    
    sp_col1, sp_col2 = st.columns(2)

    if "Batting" in active_mode and b_data is not None:
        with sp_col1:
            st.markdown("##### 🏏 By Match Phase")
            b_ph = splits['bat_phase'][(splits['bat_phase']['striker_id'] == p_id) & (splits['bat_phase']['is_pressure'])].copy()
            if len(b_ph) > 0:
                b_ph['SR'] = (b_ph['runs'] / b_ph['balls'] * 100).round(1)
                b_ph['Dot %'] = (b_ph['dots'] / b_ph['balls'] * 100).round(1)
                st.dataframe(
                    b_ph[['phase', 'balls', 'runs', 'SR', 'Dot %', 'rva']].rename(columns={
                        'phase': 'Phase', 'balls': 'Balls', 'runs': 'Runs', 'rva': 'RVA'
                    }).style.format({'SR': '{:.1f}', 'Dot %': '{:.1f}%', 'RVA': '{:+.1f}'}),
                    use_container_width=True, hide_index=True
                )
            else:
                st.info("No phase split recorded under pressure.")

        with sp_col2:
            st.markdown("##### 🌀 Pace vs Spin Matchup")
            b_pc = splits['bat_pace'][(splits['bat_pace']['striker_id'] == p_id) & (splits['bat_pace']['is_pressure'])].copy()
            if len(b_pc) > 0:
                b_pc['SR'] = (b_pc['runs'] / b_pc['balls'] * 100).round(1)
                st.dataframe(
                    b_pc[['pace_or_spin', 'balls', 'runs', 'SR', 'rva']].rename(columns={
                        'pace_or_spin': 'Type', 'balls': 'Balls', 'runs': 'Runs', 'rva': 'RVA'
                    }).style.format({'SR': '{:.1f}', 'RVA': '{:+.1f}'}),
                    use_container_width=True, hide_index=True
                )
            else:
                st.info("No pace/spin split recorded.")

    elif bw_data is not None:
        with sp_col1:
            st.markdown("##### 🎯 By Match Phase")
            bw_ph = splits['bowl_phase'][(splits['bowl_phase']['bowler_id'] == p_id) & (splits['bowl_phase']['is_pressure'])].copy()
            if len(bw_ph) > 0:
                bw_ph['Econ'] = (bw_ph['runs'] / (bw_ph['balls'] / 6)).round(2)
                bw_ph['Dot %'] = (bw_ph['dots'] / bw_ph['balls'] * 100).round(1)
                st.dataframe(
                    bw_ph[['phase', 'balls', 'runs', 'wkts', 'Econ', 'Dot %', 'bva']].rename(columns={
                        'phase': 'Phase', 'balls': 'Balls', 'runs': 'Runs', 'wkts': 'Wkts', 'bva': 'BVA'
                    }).style.format({'Econ': '{:.2f}', 'Dot %': '{:.1f}%', 'BVA': '{:+.1f}'}),
                    use_container_width=True, hide_index=True
                )

        with sp_col2:
            st.markdown("##### 👥 Against Batter Hand")
            bw_hd = splits['bowl_hand'][(splits['bowl_hand']['bowler_id'] == p_id) & (splits['bowl_hand']['is_pressure'])].copy()
            if len(bw_hd) > 0:
                bw_hd['Econ'] = (bw_hd['runs'] / (bw_hd['balls'] / 6)).round(2)
                st.dataframe(
                    bw_hd[['batting_type', 'balls', 'runs', 'wkts', 'Econ', 'bva']].rename(columns={
                        'batting_type': 'Batter Hand', 'balls': 'Balls', 'runs': 'Runs', 'wkts': 'Wkts', 'bva': 'BVA'
                    }).style.format({'Econ': '{:.2f}', 'BVA': '{:+.1f}'}),
                    use_container_width=True, hide_index=True
                )

# ----- TAB 3: GAME LOGS -----
with tab_logs:
    st.markdown("#### 📜 Match-by-Match Pressure Performance History")

    if "Batting" in active_mode and b_data is not None:
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
                use_container_width=True, height=400, hide_index=True
            )
        else:
            st.info("No match logs found.")

    elif bw_data is not None:
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
                use_container_width=True, height=400, hide_index=True
            )

# ----- TAB 4: FRANCHISE SCOUTING BLUEPRINT -----
with tab_scout:
    st.markdown("#### 🧠 Franchise Moneyball Scouting Report & Tactical Playbook")
    
    scout1, scout2 = st.columns(2)
    
    with scout1:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10B981; border-radius: 8px; padding: 18px; margin-bottom: 16px;">
            <div style="font-size: 12px; font-weight: 800; color: #10B981; text-transform: uppercase;">✅ Key Pressure Superpowers</div>
            <div style="font-size: 13.5px; color: #E2E8F0; margin-top: 8px; line-height: 1.6;">
                • <strong>Clutch Elevation:</strong> Delivers superior execution under pressure compared to ordinary overs.<br>
                • <strong>Boundary Threat:</strong> Capable of finding the boundary early in the over, immediately resetting field pressure.<br>
                • <strong>High Win Probability Surplus:</strong> Involved in critical match-winning sequences across IPL and T20Is.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(233, 30, 99, 0.08); border-left: 4px solid #E91E63; border-radius: 8px; padding: 18px;">
            <div style="font-size: 12px; font-weight: 800; color: #FF80AB; text-transform: uppercase;">⚠️ Opposition Exploitation Notes</div>
            <div style="font-size: 13.5px; color: #E2E8F0; margin-top: 8px; line-height: 1.6;">
                Opposing analysts will target early deliveries before set. For batters, testing with hard-length deliveries outside off-stump; for bowlers, attacking with aggressive switch-hits against stock lengths.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with scout2:
        st.markdown(f"""
        <div style="background: rgba(56, 189, 248, 0.08); border-left: 4px solid #38BDF8; border-radius: 8px; padding: 18px; margin-bottom: 16px;">
            <div style="font-size: 12px; font-weight: 800; color: #38BDF8; text-transform: uppercase;">🏏 Tactical In-Game Deployment (For Sanju Samson & Rahul Dravid)</div>
            <div style="font-size: 13.5px; color: #E2E8F0; margin-top: 8px; line-height: 1.6;">
                • <strong>Optimal Match Phase:</strong> {'Death overs (16–20)' if (b_data is not None and b_data['delta_sr'] > 10) or (bw_data is not None and bw_data['death_share'] > 40) else 'Middle squeeze overs (7–15)'}<br>
                • <strong>Target Scenario:</strong> High-leverage chases requiring 9.5+ RPO or defending sub-15 run margins in the final 2 overs.<br>
                • <strong>Impact Player Substitution Priority:</strong> High — ideal for tactical matchup entry.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: rgba(245, 158, 11, 0.08); border-left: 4px solid #F59E0B; border-radius: 8px; padding: 18px;">
            <div style="font-size: 12px; font-weight: 800; color: #FCD34D; text-transform: uppercase;">💰 Auction & Retention Valuation</div>
            <div style="font-size: 13.5px; color: #E2E8F0; margin-top: 8px; line-height: 1.6;">
                <strong>PRI Rating: {pri_val:.1f} / 100</strong> (Rank #{rank_val})<br>
                Classified as a <strong>Tier 1 High-Leverage Asset</strong>. Generates substantial surplus value above base auction price due to clutch acceleration.
            </div>
        </div>
        """, unsafe_allow_html=True)
