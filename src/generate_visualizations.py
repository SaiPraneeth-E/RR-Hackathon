import os
os.environ['MPLCONFIGDIR'] = os.path.abspath('figures')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set aesthetic style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#eeeeee'
plt.rcParams['grid.linestyle'] = '--'

bat = pd.read_pickle(r'src/final_bat_ranked.pkl')
bowl = pd.read_pickle(r'src/final_bowl_ranked.pkl')
bbb = pd.read_pickle(r'src/enriched_bbb.pkl')

# ----------------- FIGURE 1: BATTING PRESSURE LANDSCAPE -----------------
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
ax.grid(True, zorder=0)

# Scatter for all qualified batters
sc = ax.scatter(
    bat['sr_all'],
    bat['sr_p'],
    s=bat['balls_p'] * 0.4,
    c=bat['delta_sr'],
    cmap='coolwarm',
    alpha=0.85,
    edgecolors='#444444',
    linewidth=0.6,
    zorder=3
)
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label('Strike Rate Delta (ΔSR = SR_P - SR_Base)', fontsize=10)

# Reference line y = x (no change under pressure)
lims = [125, 195]
ax.plot(lims, lims, '--', color='#555555', linewidth=1.2, label='Baseline Parity (ΔSR = 0)', zorder=2)

# Annotate top 10 batters
top_10_bat = bat.head(10)
for _, r in top_10_bat.iterrows():
    ax.annotate(
        f"{r['striker_name']} (#{r['rank']})",
        (r['sr_all'], r['sr_p']),
        xytext=(6, 4),
        textcoords='offset points',
        fontsize=8.5,
        fontweight='bold',
        color='#111111',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', alpha=0.85, edgecolor='#999999', linewidth=0.6),
        zorder=5
    )

ax.set_title('Batting Under Pressure: High-Pressure SR vs Usual Baseline\nTop-Right Quadrant: Elite Finishers Who Accelerate When Match is on the Line', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Baseline Strike Rate (All Match Situations)', fontsize=10, labelpad=8)
ax.set_ylabel('High-Pressure Strike Rate (SR_P)', fontsize=10, labelpad=8)
ax.set_xlim(128, 185)
ax.set_ylim(135, 205)
ax.legend(loc='lower right', frameon=True, facecolor='#ffffff', edgecolor='#cccccc')
plt.tight_layout()
plt.savefig('figures/fig1_batting_pressure_landscape.png')
plt.close()
print('Figure 1 saved.')

# ----------------- FIGURE 2: BOWLING RUN SUPPRESSION & BVA -----------------
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
ax.grid(True, zorder=0)

sc2 = ax.scatter(
    bowl['phase_delta_econ'],
    bowl['sr_p'],
    s=bowl['balls_p'] * 0.4,
    c=bowl['total_bva_p'],
    cmap='viridis',
    alpha=0.85,
    edgecolors='#444444',
    linewidth=0.6,
    zorder=3
)
cbar2 = plt.colorbar(sc2, ax=ax)
cbar2.set_label('Total Bowling Value Added (BVA)', fontsize=10)

ax.axvline(0, linestyle='--', color='#555555', linewidth=1.2, label='Phase Parity (ΔEcon = 0)', zorder=2)

top_10_bowl = bowl.head(10)
for _, r in top_10_bowl.iterrows():
    ax.annotate(
        f"{r['bowler_name']} (#{r['rank']})",
        (r['phase_delta_econ'], r['sr_p']),
        xytext=(6, 4),
        textcoords='offset points',
        fontsize=8.5,
        fontweight='bold',
        color='#111111',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', alpha=0.85, edgecolor='#999999', linewidth=0.6),
        zorder=5
    )

ax.set_title('Bowling Under Pressure: Phase-Adjusted Economy Savings vs Strike Rate\nTop-Right: High Economy Suppression + Rapid Wicket Threat', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Phase-Adjusted Economy Savings (Runs Saved / Over vs Expected Phase Par)', fontsize=10, labelpad=8)
ax.set_ylabel('Bowling Strike Rate under Pressure (Balls / Wicket - Lower is Better)', fontsize=10, labelpad=8)
ax.invert_yaxis()
ax.legend(loc='lower right', frameon=True, facecolor='#ffffff', edgecolor='#cccccc')
plt.tight_layout()
plt.savefig('figures/fig2_bowling_containment.png')
plt.close()
print('Figure 2 saved.')

# ----------------- FIGURE 3: MACRO VALIDATION -----------------
fig, axes = plt.subplots(1, 4, figsize=(14, 4), dpi=300)

metrics = [
    ('Batting Strike Rate', 144.74, 137.83, 'Runs / 100 Balls', '#e74c3c', '#3498db'),
    ('Economy Rate', 9.20, 8.70, 'Runs / Over', '#e67e22', '#2ecc71'),
    ('Balls per Wicket', 14.25, 20.00, 'Legal Deliveries', '#9b59b6', '#1abc9c'),
    ('Dot Ball %', 30.85, 35.30, 'Percentage of Balls', '#34495e', '#95a5a6')
]

for ax, (m_title, p_val, o_val, unit, col_p, col_o) in zip(axes, metrics):
    ax.grid(True, axis='y', zorder=0)
    bars = ax.bar(['Pressure', 'Ordinary'], [p_val, o_val], color=[col_p, col_o], width=0.52, edgecolor='#333333', linewidth=0.8, zorder=3)
    ax.set_title(m_title, fontsize=11, fontweight='bold', pad=8)
    ax.set_ylabel(unit, fontsize=9)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + (0.02 * h), f'{h:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.set_ylim(0, max(p_val, o_val) * 1.25)

plt.suptitle('Empirical Macro Validation: Pressure vs Ordinary Situations (N = 200,999 Deliveries)', fontsize=13, fontweight='bold', y=1.04)
plt.tight_layout()
plt.savefig('figures/fig3_macro_validation.png')
plt.close()
print('Figure 3 saved.')

# ----------------- FIGURE 4: WIN PROBABILITY HEATMAP -----------------
inn2 = bbb[(bbb['innings'] == 2) & (bbb['balls_rem'] <= 30) & (bbb['balls_rem'] > 0)].copy()
inn2['rrr_bucket'] = pd.cut(inn2['rrr'], bins=[0, 6, 9, 12, 15, 20], labels=['<6', '6-9', '9-12', '12-15', '15-20'])
inn2['wkt_bucket'] = pd.cut(inn2['wickets_in_hand'], bins=[0, 2, 4, 6, 10], labels=['1-2 wkts', '3-4 wkts', '5-6 wkts', '7-10 wkts'])
inn2['batting_won'] = (inn2['win_team_id'] == inn2['batting_team_id']).astype(int)

pivot = pd.pivot_table(inn2, values='batting_won', index='rrr_bucket', columns='wkt_bucket', aggfunc='mean', observed=False) * 100

fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=300)
c = ax.imshow(pivot.values, cmap='Blues_r', aspect='auto', vmin=0, vmax=100)
plt.colorbar(c, ax=ax, label='Chase Win Probability (%)')

ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns, fontsize=9.5, fontweight='bold')
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index, fontsize=9.5, fontweight='bold')

for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        val = pivot.iloc[i, j]
        color = 'white' if val < 40 or val > 75 else 'black'
        ax.text(j, i, f'{val:.1f}%', ha='center', va='center', color=color, fontweight='bold', fontsize=10)

ax.set_title('Empirical Chase Win Probability in Death Overs (Overs 16-20)\nNon-Linear Interaction of RRR and Wickets in Hand', fontsize=11, fontweight='bold', pad=12)
ax.set_xlabel('Wickets in Hand', fontsize=10, labelpad=8)
ax.set_ylabel('Required Run Rate (RRR)', fontsize=10, labelpad=8)
plt.tight_layout()
plt.savefig('figures/fig4_win_probability_matrix.png')
plt.close()
print('Figure 4 saved.')

# ----------------- FIGURE 5: TOP 10 RANKINGS COMPARISON -----------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

# Batters
b_top = bat.head(10).sort_values('PRI', ascending=True)
ax1.grid(True, axis='x', zorder=0)
bars1 = ax1.barh(b_top['striker_name'], b_top['PRI'], color='#2980b9', edgecolor='#1a5276', linewidth=0.8, zorder=3)
ax1.set_title('Top 10 Batters Under Pressure (PRI Score)', fontsize=11, fontweight='bold', pad=10)
ax1.set_xlabel('Pressure Reliability Index (0 - 100)', fontsize=9.5)
for bar in bars1:
    w = bar.get_width()
    ax1.text(w + 1.2, bar.get_y() + bar.get_height()/2., f'{w:.1f}', ha='left', va='center', fontsize=8.5, fontweight='bold')
ax1.set_xlim(0, 115)

# Bowlers
bw_top = bowl.head(10).sort_values('PRI', ascending=True)
ax2.grid(True, axis='x', zorder=0)
bars2 = ax2.barh(bw_top['bowler_name'], bw_top['PRI'], color='#27ae60', edgecolor='#196f3d', linewidth=0.8, zorder=3)
ax2.set_title('Top 10 Bowlers Under Pressure (PRI Score)', fontsize=11, fontweight='bold', pad=10)
ax2.set_xlabel('Pressure Reliability Index (0 - 100)', fontsize=9.5)
for bar in bars2:
    w = bar.get_width()
    ax2.text(w + 1.2, bar.get_y() + bar.get_height()/2., f'{w:.1f}', ha='left', va='center', fontsize=8.5, fontweight='bold')
ax2.set_xlim(0, 115)

plt.suptitle('SupeRR Selector Season 2: Final Top 10 Player Rankings', fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('figures/fig5_top10_rankings.png')
plt.close()
print('Figure 5 saved.')
