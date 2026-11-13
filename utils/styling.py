import streamlit as st

THEME = {
    'bg_card': '#1E293B',
    'bg_dark': '#0B132B',
    'pink': '#E91E63',
    'cyan': '#38BDF8',
    'emerald': '#10B981',
    'gold': '#F59E0B',
    'red': '#EF4444',
    'purple': '#8B5CF6',
    'text': '#F8FAFC',
    'text_muted': '#94A3B8',
    'grid': 'rgba(255, 255, 255, 0.08)'
}

__all__ = [
    'apply_custom_theme', 'render_header', 'render_kpi', 'render_callout',
    'render_ticker', 'render_player_spotlight_card', 'THEME'
]

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

        /* App Base Styling with Cricket Stadium Ambience */
        .stApp {
            background: radial-gradient(circle at 15% 15%, rgba(233, 30, 99, 0.09) 0%, transparent 45%), 
                        radial-gradient(circle at 85% 85%, rgba(56, 189, 248, 0.09) 0%, transparent 45%),
                        radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.04) 0%, transparent 60%),
                        #0B132B !important;
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
            color: var(--text-primary) !important;
        }

        /* Cricket Stadium Crease Border Lines */
        .cricket-crease-line {
            height: 2px;
            background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.15) 20%, rgba(233, 30, 99, 0.6) 50%, rgba(56, 189, 248, 0.6) 80%, transparent 100%);
            margin: 20px 0;
        }

        /* Player Spotlight Card (Luxury Cricket Trading Card) */
        .player-spotlight-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 16px 36px -10px rgba(0, 0, 0, 0.6), 0 0 25px rgba(233, 30, 99, 0.15);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }

        .player-spotlight-card.rank-gold {
            border: 1px solid rgba(245, 158, 11, 0.45);
            box-shadow: 0 16px 36px -10px rgba(0, 0, 0, 0.7), 0 0 30px rgba(245, 158, 11, 0.2);
        }

        .player-spotlight-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #E91E63 0%, #38BDF8 50%, #F59E0B 100%);
        }

        /* Player Avatar Circle with Glowing Ring */
        .player-avatar {
            width: 72px;
            height: 72px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: 800;
            color: #FFFFFF;
            border: 3px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
            background: linear-gradient(135deg, #1E293B, #0F172A);
        }

        .player-avatar.gold {
            background: linear-gradient(135deg, #F59E0B, #B45309);
            border-color: #FCD34D;
            box-shadow: 0 0 20px rgba(245, 158, 11, 0.5);
            color: #000;
        }

        .player-avatar.pink {
            background: linear-gradient(135deg, #E91E63, #880E4F);
            border-color: #FF80AB;
            box-shadow: 0 0 20px rgba(233, 30, 99, 0.5);
        }

        .player-avatar.cyan {
            background: linear-gradient(135deg, #0284C7, #0C4A6E);
            border-color: #7DD3FC;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
        }

        /* Archetype Pill */
        .archetype-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-top: 4px;
        }

        .archetype-badge.finisher {
            background: rgba(233, 30, 99, 0.18);
            border: 1px solid #E91E63;
            color: #FF80AB;
        }

        .archetype-badge.death-bowler {
            background: rgba(56, 189, 248, 0.18);
            border: 1px solid #38BDF8;
            color: #7DD3FC;
        }

        .archetype-badge.spin-maestro {
            background: rgba(139, 92, 246, 0.18);
            border: 1px solid #8B5CF6;
            color: #C4B5FD;
        }

        .archetype-badge.anchor {
            background: rgba(16, 185, 129, 0.18);
            border: 1px solid #10B981;
            color: #6EE7B7;
        }

        /* Stat Ribbon Tiles */
        .stat-ribbon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 12px;
            margin-top: 18px;
        }

        .stat-ribbon-tile {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            padding: 12px 14px;
            text-align: center;
            transition: 0.2s ease;
        }

        .stat-ribbon-tile:hover {
            border-color: rgba(56, 189, 248, 0.4);
            transform: translateY(-2px);
            background: rgba(30, 41, 59, 0.8);
        }

        .stat-ribbon-label {
            font-size: 10px;
            font-weight: 700;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .stat-ribbon-val {
            font-size: 18px;
            font-weight: 800;
            color: #FFFFFF;
            margin-top: 4px;
        }

        .stat-ribbon-val.positive {
            color: #10B981;
        }
        .stat-ribbon-val.gold {
            color: #F59E0B;
        }
        .stat-ribbon-val.cyan {
            color: #38BDF8;
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
    if hasattr(st, "html"):
        st.html(custom_css)
    else:
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
    if hasattr(st, "html"):
        st.html(html)
    else:
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
    if hasattr(st, "html"):
        st.html(header_html)
    else:
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
    if hasattr(col, "html"):
        col.html(html)
    else:
        col.markdown(html, unsafe_allow_html=True)


def render_callout(text, title="ANALYST NOTE"):
    """Renders a stylish callout box for commentary or takeaways."""
    html = f"""
    <div class="rr-callout">
        <strong>{title}:</strong> {text}
    </div>
    """
    if hasattr(st, "html"):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)


def render_player_spotlight_card(name, player_id, rank, pri, role, archetype, teams, stats_dict, notes=None):
    """Renders a high-end luxury cricket trading card for highlighted players without markdown indentation issues."""
    is_gold = (rank == 1)
    card_class = "player-spotlight-card rank-gold" if is_gold else "player-spotlight-card"
    avatar_class = "player-avatar gold" if is_gold else ("player-avatar pink" if role == "Batter" else "player-avatar cyan")
    medal_emoji = "🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else f"#{rank}"))

    # Determine archetype badge style
    arch_lower = archetype.lower()
    if "finisher" in arch_lower or "closer" in arch_lower or "accelerat" in arch_lower:
        badge_style = "archetype-badge finisher"
    elif "death" in arch_lower or "pacer" in arch_lower:
        badge_style = "archetype-badge death-bowler"
    elif "spin" in arch_lower or "mystery" in arch_lower:
        badge_style = "archetype-badge spin-maestro"
    else:
        badge_style = "archetype-badge anchor"

    # Build stat tiles HTML without leading indentation
    tiles_list = []
    for label, val in stats_dict.items():
        val_str = str(val)
        val_class = "stat-ribbon-val"
        if "+" in val_str or (any(c.isdigit() for c in val_str) and "%" in val_str and float(val_str.replace("%","")) > 60):
            val_class += " positive"
        elif is_gold:
            val_class += " gold"
        else:
            val_class += " cyan"
        tiles_list.append(
            f'<div class="stat-ribbon-tile">'
            f'<div class="stat-ribbon-label">{label}</div>'
            f'<div class="{val_class}">{val}</div>'
            f'</div>'
        )
    tiles_html = "".join(tiles_list)

    notes_html = f'<div style="margin-top:16px;padding-top:14px;border-top:1px solid rgba(255,255,255,0.06);font-size:12.5px;color:#CBD5E1;line-height:1.5;"><strong>⚡ Tactical Intelligence:</strong> {notes}</div>' if notes else ''

    # Clean unindented card HTML
    card_html = (
        f'<div class="{card_class}">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">'
        f'<div style="display:flex;align-items:center;gap:18px;">'
        f'<div class="{avatar_class}">{name[0]}</div>'
        f'<div>'
        f'<div style="display:flex;align-items:center;gap:10px;">'
        f'<span style="font-size:22px;font-weight:800;color:#FFFFFF;">{name}</span>'
        f'<span style="font-size:16px;">{medal_emoji}</span>'
        f'</div>'
        f'<div style="font-size:12px;color:#94A3B8;margin-top:2px;">'
        f'Player ID: <code style="color:#38BDF8;background:rgba(56,189,248,0.1);padding:2px 6px;border-radius:4px;">{player_id}</code> • '
        f'<span style="color:#CBD5E1;">{teams}</span>'
        f'</div>'
        f'<div class="{badge_style}">{archetype}</div>'
        f'</div>'
        f'</div>'
        f'<div style="display:flex;gap:12px;">'
        f'<div style="background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.4);border-radius:10px;padding:10px 18px;text-align:center;">'
        f'<div style="font-size:10px;color:#FCD34D;font-weight:800;text-transform:uppercase;">PRI Score</div>'
        f'<div style="font-size:22px;font-weight:800;color:#FFF;">{pri:.1f}</div>'
        f'</div>'
        f'<div style="background:rgba(233,30,99,0.12);border:1px solid rgba(233,30,99,0.4);border-radius:10px;padding:10px 18px;text-align:center;">'
        f'<div style="font-size:10px;color:#FF80AB;font-weight:800;text-transform:uppercase;">Official Rank</div>'
        f'<div style="font-size:22px;font-weight:800;color:#FFF;">#{rank}</div>'
        f'</div>'
        f'</div>'
        f'</div>'
        f'<div class="stat-ribbon-grid">{tiles_html}</div>'
        f'{notes_html}'
        f'</div>'
    )
    if hasattr(st, "html"):
        st.html(card_html)
    else:
        st.markdown(card_html, unsafe_allow_html=True)

