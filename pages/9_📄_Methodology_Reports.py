import streamlit as st
import os
import pandas as pd
from utils.styling import apply_custom_theme, render_header, render_kpi, render_callout
from utils.data_loader import load_batters_data, load_bowlers_data

st.set_page_config(page_title="Methodology & Reports | SUPERR SELECTOR", page_icon="📄", layout="wide")
apply_custom_theme()

render_header(
    title="METHODOLOGY & OFFICIAL REPORTS",
    subtitle="Whitepaper Documentation, Unstop Submission Data & High-Resolution Scientific Figures",
    tag="Research & Documentation"
)

bat_df = load_batters_data()
bowl_df = load_bowlers_data()

# Top 10 Unstop Submission Section
st.markdown("### 🏆 Official Top 10 Submissions for Unstop Dropdowns")
st.markdown(
    "Use the exact Player IDs and Names below to populate the required dropdown fields on the Unstop submission portal:"
)

c_top_bat, c_top_bowl = st.columns(2)

with c_top_bat:
    st.markdown("#### 🏏 Top 10 Batters Under Pressure")
    bat_top10 = bat_df.head(10)[['rank', 'striker_name', 'striker_id', 'PRI', 'sr_p', 'avg_p', 'delta_sr', 'total_rva_p']].copy()
    bat_top10.columns = ['Rank', 'Player Name', 'Player ID', 'PRI Score', 'Pressure SR', 'Pressure Avg', 'Δ SR', 'Total RVA']
    st.dataframe(
        bat_top10.style.format({
            'PRI Score': '{:.1f}',
            'Pressure SR': '{:.1f}',
            'Pressure Avg': '{:.1f}',
            'Δ SR': '+{:.1f}',
            'Total RVA': '+{:.1f}'
        }).background_gradient(subset=['PRI Score'], cmap='YlGn'),
        use_container_width=True,
        hide_index=True
    )

with c_top_bowl:
    st.markdown("#### 🎯 Top 10 Bowlers Under Pressure")
    bowl_top10 = bowl_df.head(10)[['rank', 'bowler_name', 'bowler_id', 'PRI', 'econ_p', 'phase_delta_econ', 'total_bva_p', 'death_share']].copy()
    bowl_top10.columns = ['Rank', 'Player Name', 'Player ID', 'PRI Score', 'Pressure Econ', 'Phase ΔEcon', 'Total BVA', 'Death Share %']
    st.dataframe(
        bowl_top10.style.format({
            'PRI Score': '{:.1f}',
            'Pressure Econ': '{:.2f}',
            'Phase ΔEcon': '+{:.2f}',
            'Total BVA': '+{:.1f}',
            'Death Share %': '{:.1f}%'
        }).background_gradient(subset=['PRI Score'], cmap='YlGn'),
        use_container_width=True,
        hide_index=True
    )

# Download Center
st.markdown("---")
st.markdown("### 📥 Document & Dataset Download Center")
st.markdown("Download all official publication materials, formatted executive documents, and complete CSV exports:")

d1, d2, d3, d4 = st.columns(4)

with d1:
    pdf_path = "reports/METHODOLOGY_REPORT_FINAL.pdf"
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download Report (PDF)",
                data=f.read(),
                file_name="SupeRR_Selector_Methodology_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

with d2:
    docx_path = "reports/METHODOLOGY_REPORT_FINAL.docx"
    if os.path.exists(docx_path):
        with open(docx_path, "rb") as f:
            st.download_button(
                label="📝 Download Report (Word)",
                data=f.read(),
                file_name="SupeRR_Selector_Methodology_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

with d3:
    md_path = "reports/METHODOLOGY_REPORT.md"
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            st.download_button(
                label="📑 Download Report (Markdown)",
                data=f.read(),
                file_name="SupeRR_Selector_Methodology_Report.md",
                mime="text/markdown",
                use_container_width=True
            )

with d4:
    csv_top10 = "reports/top10_batters.csv"
    if os.path.exists(csv_top10):
        with open(csv_top10, "rb") as f:
            st.download_button(
                label="📊 Download Top 10 Lists (CSV)",
                data=f.read(),
                file_name="SupeRR_Selector_Top10_Rankings.csv",
                mime="text/csv",
                use_container_width=True
            )

# Embedded Scientific Figures Gallery
st.markdown("---")
st.markdown("### 🖼️ Scientific Visualizations Gallery (Figures 1–7)")

figs_dict = {
    "Figure 1: Batting Pressure Landscape": "figures/fig1_batting_pressure_landscape.png",
    "Figure 2: Bowling Containment & Phase Economics": "figures/fig2_bowling_containment.png",
    "Figure 3: Macro Pressure Validation (Bar Comparisons)": "figures/fig3_macro_validation.png",
    "Figure 4: Win Probability Dynamic Matrix": "figures/fig4_win_probability_matrix.png",
    "Figure 5: Official Top 10 Rankings Summary": "figures/fig5_top10_rankings.png",
    "Figure 6: Match Leverage Curve (Over Progression)": "figures/fig6_over_pressure_curve.png",
    "Figure 7: The Rise vs Dip Dynamics": "figures/fig7_rise_vs_dip.png"
}

for fig_title, fig_file in figs_dict.items():
    with st.expander(f"📷 {fig_title}", expanded=False):
        if os.path.exists(fig_file):
            st.image(fig_file, use_container_width=True, caption=fig_title)
        else:
            st.warning(f"File {fig_file} not found.")

# Full Whitepaper Reader
st.markdown("---")
st.markdown("### 📖 Embedded Methodology Whitepaper")

with st.expander("🔍 Click to Read Full Technical Whitepaper (METHODOLOGY_REPORT.md)", expanded=True):
    if os.path.exists("METHODOLOGY_REPORT.md"):
        with open("METHODOLOGY_REPORT.md", "r", encoding="utf-8") as f:
            md_text = f.read()
        st.markdown(md_text, unsafe_allow_html=True)
    else:
        st.info("Report file not located.")
