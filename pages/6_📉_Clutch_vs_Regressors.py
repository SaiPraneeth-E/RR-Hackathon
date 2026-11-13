import streamlit as st
import pandas as pd
import numpy as np
from utils.styling import apply_custom_theme, render_header, render_kpi, render_callout
from utils.data_loader import load_batters_data, load_bowlers_data
from utils.visualizations import plot_scatter, THEME

st.set_page_config(page_title="Clutch vs Regressors | SUPERR SELECTOR", page_icon="📉", layout="wide")
apply_custom_theme()

render_header(
    title="CLUTCH PERFORMERS VS PRESSURE REGRESSORS",
    subtitle="Identifying Who Rises to the Occasion and Exposing Who Dips When Stakes Peak",
    tag="The Anti-Rankings Analysis"
)

bat_df = load_batters_data()
bowl_df = load_bowlers_data()

render_callout(
    "A player's true character is not revealed when cruising at 60 for 0 in the 7th over, but when needing 38 off 18 "
    "or defending 12 off the final over. Our model mathematically isolates <strong>Delta Performance (Δ)</strong> "
    "— the differential between pressure output and ordinary baseline. This separates genuine match-winners from flat-track bullies.",
    title="THE RISE VS DIP PARADOX"
)

tab_bat, tab_bowl = st.tabs(["🏏 Batting: Accelerators vs Dippers", "🎯 Bowling: Protectors vs Bleeders"])

with tab_bat:
    st.markdown("### 🏏 Batting Rise vs Dip Dynamics")

    # 4-Quadrant Scatter Plot
    median_base_sr = float(bat_df['sr_all'].median())
    median_p_sr = float(bat_df['sr_p'].median())

    fig_quad_bat = plot_scatter(
        df=bat_df,
        x_col='sr_all',
        y_col='sr_p',
        text_col='striker_name',
        color_col='delta_sr',
        size_col='balls_p',
        title="Baseline Strike Rate vs Pressure Strike Rate (Diagonal Line = Par Performance)",
        x_label="Baseline Strike Rate (All Match Play)",
        y_label="Pressure Strike Rate (High Leverage Situations)",
        vline=median_base_sr,
        hline=median_p_sr
    )
    # Add parity diagonal line y = x
    fig_quad_bat.add_shape(
        type="line", line=dict(dash="dash", color="rgba(255, 255, 255, 0.4)", width=1.5),
        x0=100, y0=100, x1=200, y1=200
    )
    fig_quad_bat.add_annotation(x=175, y=175, text="y = x (Zero Performance Dip)", showarrow=False, font=dict(color="#38BDF8", size=10))
    st.plotly_chart(fig_quad_bat, use_container_width=True)

    # Tables: Top Accelerators vs Top Dippers
    col_acc, col_dip = st.columns(2)

    with col_acc:
        st.markdown("#### 🚀 Top 10 Pressure Accelerators (Highest +ΔSR)")
        top_acc = bat_df.sort_values(by='delta_sr', ascending=False).head(10)[[
            'rank', 'striker_name', 'sr_p', 'sr_all', 'delta_sr', 'total_rva_p', 'PRI'
        ]].copy()
        top_acc.columns = ['Rank', 'Batter', 'Pressure SR', 'Base SR', 'Δ SR', 'Total RVA', 'PRI']
        st.dataframe(
            top_acc.style.format({
                'Pressure SR': '{:.1f}', 'Base SR': '{:.1f}', 'Δ SR': '+{:.1f}',
                'Total RVA': '+{:.1f}', 'PRI': '{:.1f}'
            }).background_gradient(subset=['Δ SR'], cmap='Greens'),
            use_container_width=True,
            hide_index=True
        )

    with col_dip:
        st.markdown("#### ⚠️ Top 10 Pressure Dippers (Highest -ΔSR Regressors)")
        top_dip = bat_df.sort_values(by='delta_sr', ascending=True).head(10)[[
            'rank', 'striker_name', 'sr_p', 'sr_all', 'delta_sr', 'total_rva_p', 'PRI'
        ]].copy()
        top_dip.columns = ['Rank', 'Batter', 'Pressure SR', 'Base SR', 'Δ SR', 'Total RVA', 'PRI']
        st.dataframe(
            top_dip.style.format({
                'Pressure SR': '{:.1f}', 'Base SR': '{:.1f}', 'Δ SR': '{:.1f}',
                'Total RVA': '{:+.1f}', 'PRI': '{:.1f}'
            }).background_gradient(subset=['Δ SR'], cmap='Reds_r'),
            use_container_width=True,
            hide_index=True
        )

with tab_bowl:
    st.markdown("### 🎯 Bowling Rise vs Dip Dynamics")

    # 4-Quadrant Scatter Plot for Bowling
    fig_quad_bowl = plot_scatter(
        df=bowl_df,
        x_col='econ_all',
        y_col='phase_delta_econ',
        text_col='bowler_name',
        color_col='PRI',
        size_col='balls_p',
        title="Baseline Economy vs Phase-Adjusted Economy Savings (Top Left = World Class)",
        x_label="Baseline Economy Rate (Lower is Better)",
        y_label="Phase-Adjusted Economy Savings (Higher is Better)",
        vline=float(bowl_df['econ_all'].median()),
        hline=0.0
    )
    st.plotly_chart(fig_quad_bowl, use_container_width=True)

    col_prot, col_bleed = st.columns(2)

    with col_prot:
        st.markdown("#### 🛡️ Top 10 Phase Protectors (Highest +Phase ΔEcon)")
        top_prot = bowl_df.sort_values(by='phase_delta_econ', ascending=False).head(10)[[
            'rank', 'bowler_name', 'econ_p', 'econ_all', 'phase_delta_econ', 'total_bva_p', 'PRI'
        ]].copy()
        top_prot.columns = ['Rank', 'Bowler', 'Pressure Econ', 'Base Econ', 'Phase ΔEcon', 'Total BVA', 'PRI']
        st.dataframe(
            top_prot.style.format({
                'Pressure Econ': '{:.2f}', 'Base Econ': '{:.2f}', 'Phase ΔEcon': '+{:.2f}',
                'Total BVA': '+{:.1f}', 'PRI': '{:.1f}'
            }).background_gradient(subset=['Phase ΔEcon'], cmap='Greens'),
            use_container_width=True,
            hide_index=True
        )

    with col_bleed:
        st.markdown("#### ⚠️ Top 10 Pressure Bleeders (Highest Negative Phase ΔEcon)")
        top_bleed = bowl_df.sort_values(by='phase_delta_econ', ascending=True).head(10)[[
            'rank', 'bowler_name', 'econ_p', 'econ_all', 'phase_delta_econ', 'total_bva_p', 'PRI'
        ]].copy()
        top_bleed.columns = ['Rank', 'Bowler', 'Pressure Econ', 'Base Econ', 'Phase ΔEcon', 'Total BVA', 'PRI']
        st.dataframe(
            top_bleed.style.format({
                'Pressure Econ': '{:.2f}', 'Base Econ': '{:.2f}', 'Phase ΔEcon': '{:.2f}',
                'Total BVA': '{:+.1f}', 'PRI': '{:.1f}'
            }).background_gradient(subset=['Phase ΔEcon'], cmap='Reds_r'),
            use_container_width=True,
            hide_index=True
        )

# Analytical Takeaway
st.markdown("---")
render_callout(
    "<strong>Tactical Diagnosis:</strong> The steepest batting regressors (Curtis Campher, Washington Sundar, Deepak Hooda) "
    "suffer from a common structural weakness: an inability to hit boundaries against defensive lengths when the field is spread. "
    "For bowlers (Andre Russell, Nitish Reddy, Tushar Deshpande), their negative Phase ΔEcon stems from bowling full tosses "
    "or missed yorkers at the death, yielding 12+ RPO against contextual pars of 10.56.",
    title="FRANCHISE SCOUTING TAKEAWAY"
)

