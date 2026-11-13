import streamlit as st

def apply_custom_theme():
    """Injects high-end sports analytics dark theme CSS into Streamlit."""
    custom_css = """
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

        /* Root CSS Variables */
        :root {
            --bg-main: #0B132B;
            --bg-card: #1E293B;
            --bg-card-hover: #26354D;
            --bg-header: #0F172A;
            --rr-pink: #E91E63;
            --rr-pink-glow: rgba(233, 30, 99, 0.3);
            --rr-blue: #1A5276;
            --accent-emerald: #10B981;
            --accent-cyan: #38BDF8;
            --accent-gold: #F59E0B;
            --accent-red: #EF4444;
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
            --text-muted: #64748B;
            --border-subtle: rgba(255, 255, 255, 0.08);
            --card-radius: 14px;
        }

        /* App Base Styling */
        .stApp {
            background-color: var(--bg-main) !important;
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
            color: var(--text-primary) !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #080D1A !important;
            border-right: 1px solid var(--border-subtle) !important;
        }
        
        section[data-testid="stSidebar"] .stMarkdown h1, 
        section[data-testid="stSidebar"] .stMarkdown h2, 
        section[data-testid="stSidebar"] .stMarkdown h3 {
            color: var(--text-primary) !important;
            letter-spacing: -0.02em;
        }

        /* Top Header Container */
        .rr-header-container {
            background: linear-gradient(135deg, #0F172A 0%, #172554 50%, #0F172A 100%);
            border: 1px solid rgba(233, 30, 99, 0.25);
            border-radius: var(--card-radius);
            padding: 24px 30px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6), 0 0 20px var(--rr-pink-glow);
            position: relative;
            overflow: hidden;
        }

        .rr-header-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--rr-pink), var(--accent-cyan), var(--accent-gold));
        }

        .rr-brand-title {
            font-size: 30px;
            font-weight: 800;
            letter-spacing: -0.03em;
            background: linear-gradient(90deg, #FFFFFF 30%, #E2E8F0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            line-height: 1.2;
        }

        .rr-brand-subtitle {
            font-size: 14px;
            font-weight: 500;
            color: var(--accent-cyan);
            margin-top: 6px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .rr-badge-pill {
            display: inline-block;
            background: rgba(233, 30, 99, 0.15);
            border: 1px solid var(--rr-pink);
            color: #FF80AB;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-right: 8px;
        }

        .rr-badge-gold {
            display: inline-block;
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid var(--accent-gold);
            color: #FCD34D;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        /* KPI Metric Cards */
        .rr-kpi-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--card-radius);
            padding: 20px;
            margin-bottom: 16px;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .rr-kpi-card:hover {
            transform: translateY(-3px);
            border-color: rgba(56, 189, 248, 0.35);
            box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.5);
            background-color: var(--bg-card-hover);
        }

        .rr-kpi-title {
            font-size: 11px;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 8px;
        }

        .rr-kpi-value {
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: #FFFFFF;
            line-height: 1.1;
        }

        .rr-kpi-sub {
            font-size: 12px;
            font-weight: 500;
            color: var(--accent-emerald);
            margin-top: 6px;
        }

        .rr-kpi-sub.neutral {
            color: var(--text-muted);
        }

        .rr-kpi-sub.negative {
            color: var(--accent-red);
        }

        /* Callout & Narrative Box */
        .rr-callout {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
            border-left: 4px solid var(--rr-pink);
            border-top: 1px solid var(--border-subtle);
            border-right: 1px solid var(--border-subtle);
            border-bottom: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 18px 22px;
            margin: 18px 0;
            color: #E2E8F0;
            font-size: 13.5px;
            line-height: 1.6;
        }

        .rr-callout strong {
            color: #FFFFFF;
        }

        /* Formula Card */
        .rr-formula-card {
            background: #0D1627;
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 12px;
            padding: 20px;
            margin: 16px 0;
        }

        .rr-formula-title {
            font-size: 13px;
            font-weight: 700;
            color: var(--accent-cyan);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 10px;
        }

        /* Rank Badges */
        .rank-circle {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            font-weight: 800;
            font-size: 12px;
            margin-right: 8px;
        }

        .rank-1 { background: linear-gradient(135deg, #F59E0B, #D97706); color: #000; box-shadow: 0 0 10px rgba(245, 158, 11, 0.4); }
        .rank-2 { background: linear-gradient(135deg, #94A3B8, #64748B); color: #000; }
        .rank-3 { background: linear-gradient(135deg, #CD7F32, #B87333); color: #fff; }
        .rank-other { background: rgba(255, 255, 255, 0.08); color: #94A3B8; }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 7px;
            height: 7px;
        }
        ::-webkit-scrollbar-track {
            background: #0B132B;
        }
        ::-webkit-scrollbar-thumb {
            background: #1E293B;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #334155;
        }

        /* Streamlit Tab Customization */
        button[data-baseweb="tab"] {
            background-color: transparent !important;
            font-weight: 700 !important;
            color: var(--text-secondary) !important;
            border-radius: 8px 8px 0 0 !important;
            padding: 10px 20px !important;
            border-bottom: 2px solid transparent !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #FFFFFF !important;
            border-bottom-color: var(--rr-pink) !important;
            background-color: rgba(233, 30, 99, 0.08) !important;
        }

        /* Streamlit Dataframe adjustments */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            overflow: hidden;
        }

        /* Expander Header */
        .streamlit-expanderHeader {
            background-color: var(--bg-card) !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            color: #F8FAFC !important;
        }

        /* Live Sports Intelligence Ticker */
        .rr-ticker-container {
            background: linear-gradient(90deg, #131E31 0%, #1A2744 50%, #131E31 100%);
            border-top: 1px solid rgba(233, 30, 99, 0.4);
            border-bottom: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 8px;
            padding: 8px 16px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }

        .rr-ticker-badge {
            background: #E91E63;
            color: #FFFFFF;
            font-size: 10px;
            font-weight: 800;
            padding: 4px 8px;
            border-radius: 4px;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            white-space: nowrap;
            margin-right: 14px;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }

        .rr-ticker-badge::before {
            content: '';
            display: inline-block;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #FFFFFF;
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(0.8); }
            100% { opacity: 1; transform: scale(1); }
        }

        .rr-ticker-content {
            font-size: 12.5px;
            font-weight: 600;
            color: #E2E8F0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .rr-ticker-highlight {
            color: var(--accent-cyan);
            font-weight: 700;
        }
        .rr-ticker-gold {
            color: var(--accent-gold);
            font-weight: 700;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def render_ticker(highlights=None):
    """Renders a live sports broadcast intelligence ticker across the top."""
    if highlights is None:
        highlights = (
            "🔥 <span class='rr-ticker-gold'>#1 Batter:</span> Naman Dhir (PRI 94.2 • 196.4 SR) • "
            "🎯 <span class='rr-ticker-gold'>#1 Bowler:</span> Mohammad Nawaz (PRI 94.5 • 6.84 Econ) • "
            "⚡ <span class='rr-ticker-highlight'>Death King:</span> Jasprit Bumrah (+1.99 Phase Par Savings) • "
            "🚀 <span class='rr-ticker-highlight'>Top Accelerator:</span> Shashank Singh (+14.8 ΔSR) • "
            "🛡️ <span class='rr-ticker-highlight'>Multi-Phase Constrictor:</span> Sunil Narine (6.45 Econ) • "
            "📊 200,999 Deliveries Evaluated across 883 Matches"
        )
    html = f"""
    <div class="rr-ticker-container">
        <div class="rr-ticker-badge">LIVE INTEL</div>
        <div class="rr-ticker-content">{highlights}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_header(title="SUPERR SELECTOR", subtitle="The Science of Performing Under Pressure", tag="Round 1 Verified Solution"):
    """Renders the signature Rajasthan Royals style dark header banner."""
    header_html = f"""
    <div class="rr-header-container">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
                <span class="rr-badge-pill">Rajasthan Royals Analytics</span>
                <span class="rr-badge-gold">{tag}</span>
                <h1 class="rr-brand-title">{title}</h1>
                <div class="rr-brand-subtitle">{subtitle}</div>
            </div>
            <div style="text-align: right; font-size: 12px; color: #94A3B8;">
                <div style="font-weight: 700; color: #F8FAFC; margin-bottom: 2px;">Data Coverage: 2022–2026</div>
                <div>IPL & T20 Internationals (883 Matches)</div>
                <div style="color: #10B981; font-weight: 600; margin-top: 4px;">● Live Model Verified</div>
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_kpi(col, title, value, sub="", sub_type="positive"):
    """Renders a responsive KPI card inside a Streamlit column."""
    sub_class = "rr-kpi-sub"
    if sub_type == "neutral":
        sub_class += " neutral"
    elif sub_type == "negative":
        sub_class += " negative"
    
    html = f"""
    <div class="rr-kpi-card">
        <div class="rr-kpi-title">{title}</div>
        <div class="rr-kpi-value">{value}</div>
        {f'<div class="{sub_class}">{sub}</div>' if sub else ''}
    </div>
    """
    col.markdown(html, unsafe_allow_html=True)


def render_callout(text, title="ANALYST NOTE"):
    """Renders a stylish callout box for commentary or takeaways."""
    html = f"""
    <div class="rr-callout">
        <strong>{title}:</strong> {text}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

