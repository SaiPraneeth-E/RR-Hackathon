import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Global Color Palette
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

def apply_chart_theme(fig, height=450, title=None):
    """Applies high-end dark analytics styling to any Plotly figure."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(30, 41, 59, 0.5)',
        height=height,
        margin=dict(l=40, r=40, t=50 if title else 30, b=40),
        font=dict(family="Plus Jakarta Sans, sans-serif", color=THEME['text'], size=12),
        hoverlabel=dict(
            bgcolor="#0F172A",
            bordercolor=THEME['pink'],
            font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color="#FFFFFF")
        ),
        title=dict(
            text=title,
            font=dict(size=14, color="#FFFFFF", family="Plus Jakarta Sans, sans-serif"),
            x=0.02,
            y=0.98
        ) if title else None
    )
    fig.update_xaxes(
        gridcolor=THEME['grid'],
        zerolinecolor=THEME['grid'],
        tickfont=dict(color=THEME['text_muted'], size=11)
    )
    fig.update_yaxes(
        gridcolor=THEME['grid'],
        zerolinecolor=THEME['grid'],
        tickfont=dict(color=THEME['text_muted'], size=11)
    )
    return fig


def plot_radar_chart(categories, player_vals, bench_vals, player_name, bench_name="Cohort Median"):
    """Creates a 2-series radar chart comparing player to cohort benchmark."""
    # Close the polygon loop
    cats = categories + [categories[0]]
    p_vals = player_vals + [player_vals[0]]
    b_vals = bench_vals + [bench_vals[0]]

    fig = go.Figure()

    # Benchmark polygon (Muted Slate / Cyan)
    fig.add_trace(go.Scatterpolar(
        r=b_vals,
        theta=cats,
        fill='toself',
        name=bench_name,
        line=dict(color='rgba(148, 163, 184, 0.6)', width=1.5, dash='dash'),
        fillcolor='rgba(148, 163, 184, 0.15)'
    ))

    # Player polygon (Vibrant Pink / Emerald)
    fig.add_trace(go.Scatterpolar(
        r=p_vals,
        theta=cats,
        fill='toself',
        name=player_name,
        line=dict(color=THEME['pink'], width=2.5),
        fillcolor='rgba(233, 30, 99, 0.25)',
        marker=dict(size=6, color=THEME['pink'])
    ))

    fig.update_layout(
        polar=dict(
            bgcolor='rgba(30, 41, 59, 0.3)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=9, color=THEME['text_muted']),
                gridcolor=THEME['grid'],
                linecolor=THEME['grid']
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color=THEME['text'], family="Plus Jakarta Sans, sans-serif"),
                gridcolor=THEME['grid'],
                linecolor=THEME['grid']
            )
        ),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        showlegend=True
    )
    return apply_chart_theme(fig, height=450)


def plot_multi_player_radar(categories, players_data):
    """Compares up to 5 players on a single radar chart with unique colors."""
    cats = categories + [categories[0]]
    colors = [THEME['pink'], THEME['cyan'], THEME['gold'], THEME['emerald'], THEME['purple']]

    fig = go.Figure()
    for idx, (p_name, vals) in enumerate(players_data.items()):
        color = colors[idx % len(colors)]
        r_vals = vals + [vals[0]]
        fig.add_trace(go.Scatterpolar(
            r=r_vals,
            theta=cats,
            fill='toself',
            name=p_name,
            line=dict(color=color, width=2.5),
            fillcolor=f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.18)",
            marker=dict(size=5, color=color)
        ))

    fig.update_layout(
        polar=dict(
            bgcolor='rgba(30, 41, 59, 0.3)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=9, color=THEME['text_muted']),
                gridcolor=THEME['grid']
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color=THEME['text']),
                gridcolor=THEME['grid']
            )
        ),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        showlegend=True
    )
    return apply_chart_theme(fig, height=480)


def plot_scatter(df, x_col, y_col, text_col, color_col, size_col=None, title="", x_label="", y_label="", vline=None, hline=None):
    """Creates a scatter plot with optional quadrant reference lines."""
    hover_template = (
        "<b>%{text}</b><br>" +
        f"{x_label}: %{{x:.1f}}<br>" +
        f"{y_label}: %{{y:.1f}}<br>" +
        f"{color_col}: %{{marker.color:.1f}}<extra></extra>"
    )

    fig = go.Figure()

    marker_opts = dict(
        size=10 if size_col is None else df[size_col],
        color=df[color_col],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(
            title=dict(text=color_col, font=dict(color=THEME['text'], size=10)),
            tickfont=dict(color=THEME['text_muted'], size=9),
            thickness=12,
            len=0.8
        ),
        line=dict(width=1, color='rgba(255,255,255,0.4)'),
        sizemode='area',
        sizeref=2.*max(df[size_col])/(32.**2) if size_col else None,
        sizemin=4
    )

    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='markers+text',
        text=df[text_col],
        textposition="top center",
        textfont=dict(size=9, color='rgba(255,255,255,0.75)'),
        hovertemplate=hover_template,
        marker=marker_opts
    ))

    # Add quadrant reference lines if provided
    if vline is not None:
        fig.add_vline(x=vline, line_dash="dash", line_color="rgba(255,255,255,0.25)", annotation_text=f"Median {x_label}: {vline:.1f}", annotation_font_size=9, annotation_font_color=THEME['text_muted'])
    if hline is not None:
        fig.add_hline(y=hline, line_dash="dash", line_color="rgba(255,255,255,0.25)", annotation_text=f"Baseline: {hline:.1f}", annotation_font_size=9, annotation_font_color=THEME['text_muted'])

    fig.update_xaxes(title_text=x_label)
    fig.update_yaxes(title_text=y_label)

    return apply_chart_theme(fig, height=520, title=title)


def plot_horizontal_bar(df, x_col, y_col, title="", x_label="", color_col=None, height=450):
    """Horizontal bar chart for rankings."""
    sorted_df = df.sort_values(by=x_col, ascending=True)

    fig = go.Figure(go.Bar(
        x=sorted_df[x_col],
        y=sorted_df[y_col],
        orientation='h',
        marker=dict(
            color=sorted_df[color_col] if color_col else sorted_df[x_col],
            colorscale='Tealgrn' if (color_col or x_col) else None,
            colorbar=dict(title=dict(text=color_col or x_col, font=dict(size=10, color=THEME['text'])), thickness=10) if color_col else None,
            line=dict(color='rgba(255,255,255,0.2)', width=1)
        ),
        text=[f"{val:.1f}" for val in sorted_df[x_col]],
        textposition="outside",
        textfont=dict(size=10, color=THEME['text'])
    ))

    fig.update_xaxes(title_text=x_label)
    fig.update_yaxes(title_text="")
    return apply_chart_theme(fig, height=height, title=title)


def plot_over_progression(over_df):
    """Dual-axis chart showing Pressure % area and Run Rate & Wickets across 20 overs."""
    fig = go.Figure()

    # Pressure % Area Fill
    fig.add_trace(go.Scatter(
        x=over_df['over_num'],
        y=over_df['pressure_pct'],
        name='Pressure Delivery Share (%)',
        fill='tozeroy',
        mode='lines',
        line=dict(color='rgba(233, 30, 99, 0.8)', width=2),
        fillcolor='rgba(233, 30, 99, 0.15)',
        yaxis='y'
    ))

    # Run Rate line
    fig.add_trace(go.Scatter(
        x=over_df['over_num'],
        y=over_df['run_rate'],
        name='Par Run Rate (RPO)',
        mode='lines+markers',
        line=dict(color=THEME['cyan'], width=3),
        marker=dict(size=6, color=THEME['cyan']),
        yaxis='y2'
    ))

    # Layout with dual y-axis
    fig.update_layout(
        xaxis=dict(title="Over Number (1 to 20)", tickmode='linear', tick0=1, dtick=1),
        yaxis=dict(title="Pressure Share (%)", range=[0, 100], gridcolor=THEME['grid']),
        yaxis2=dict(
            title="Par Run Rate (RPO)",
            range=[4, 13],
            overlaying='y',
            side='right',
            gridcolor='rgba(0,0,0,0)',
            tickfont=dict(color=THEME['cyan'])
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Shaded phases
    fig.add_vrect(x0=0.5, x1=6.5, fillcolor="rgba(56, 189, 248, 0.05)", layer="below", line_width=0, annotation_text="Powerplay (1-6)", annotation_position="top left", annotation_font_size=9)
    fig.add_vrect(x0=6.5, x1=15.5, fillcolor="rgba(16, 185, 129, 0.05)", layer="below", line_width=0, annotation_text="Middle (7-15)", annotation_position="top left", annotation_font_size=9)
    fig.add_vrect(x0=15.5, x1=20.5, fillcolor="rgba(233, 30, 99, 0.08)", layer="below", line_width=0, annotation_text="Death (16-20)", annotation_position="top left", annotation_font_size=9)

    return apply_chart_theme(fig, height=450, title="Match Leverage Curve: Pressure Intensity Across 20 Overs")


def plot_win_probability_heatmap():
    """Generates the interactive 2D Chase Knife-Edge Heatmap (RRR vs Wickets)."""
    rrr_vals = np.linspace(6.0, 18.0, 13)
    wickets_in_hand = np.arange(1, 11)

    # Model win probability as logistic function of wickets and RRR
    grid = np.zeros((len(rrr_vals), len(wickets_in_hand)))
    for i, rrr in enumerate(rrr_vals):
        for j, w in enumerate(wickets_in_hand):
            # Sigmoid response: high wickets & low RRR = high win prob
            z = -0.52 * (rrr - 9.2) + 0.65 * (w - 4.5)
            win_prob = 1.0 / (1.0 + np.exp(-z))
            grid[i, j] = win_prob * 100

    fig = go.Figure(data=go.Heatmap(
        z=grid,
        x=[f"{w} Wkts" for w in wickets_in_hand],
        y=[f"{r:.1f} RPO" for r in rrr_vals],
        colorscale='RdYlGn',
        colorbar=dict(title=dict(text="Win Prob (%)", font=dict(color=THEME['text'], size=10)), thickness=12),
        hovertemplate="Wickets Left: %{x}<br>Req Run Rate: %{y}<br>Win Prob: %{z:.1f}%<extra></extra>"
    ))

    fig.update_layout(
        xaxis=dict(title="Wickets in Hand"),
        yaxis=dict(title="Required Run Rate (RRR)", autorange="reversed")
    )
    return apply_chart_theme(fig, height=480, title="The Chase Knife-Edge Matrix: Win Probability Dynamics")

