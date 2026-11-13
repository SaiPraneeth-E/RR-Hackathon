import os
os.environ['MPLCONFIGDIR'] = os.path.abspath('figures')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

bbb = pd.read_pickle(r'src/enriched_bbb.pkl')
bat = pd.read_pickle(r'src/final_bat_ranked.pkl')
bowl = pd.read_pickle(r'src/final_bowl_ranked.pkl')

# 1. Figure 6: The Anatomy of Pressure over 20 Overs
fig, ax1 = plt.subplots(figsize=(10, 5.2), dpi=300)
over_stats = bbb.groupby('overid').agg(
    run_rate=('bowler_runs', lambda x: (x.sum() / max(bbb.loc[x.index, 'is_legal'].sum(), 1)) * 6),
    wkt_pct=('is_wicket', lambda x: x.mean() * 100),
    dot_pct=('bowler_runs', lambda x: ((x == 0).sum() / max(bbb.loc[x.index, 'is_legal'].sum(), 1)) * 100)
).reset_index()

color = '#1A5276'
ax1.set_xlabel('Over Number of the Innings (1 to 20)', fontsize=11, fontweight='bold', labelpad=8)
ax1.set_ylabel('Run Rate (Runs Conceded per Over)', color=color, fontsize=11, fontweight='bold')
l1 = ax1.plot(over_stats['overid'], over_stats['run_rate'], color=color, linewidth=2.5, marker='o', label='League Run Rate (RPO)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticks(range(1, 21))
ax1.grid(True, linestyle='--', alpha=0.5)

ax2 = ax1.twinx()  
color2 = '#E74C3C'
ax2.set_ylabel('Wicket Hazard Rate (% balls losing wicket)', color=color2, fontsize=11, fontweight='bold')
l2 = ax2.plot(over_stats['overid'], over_stats['wkt_pct'], color=color2, linewidth=2.5, marker='s', linestyle='--', label='Wicket Fall Probability (%)')
ax2.tick_params(axis='y', labelcolor=color2)

# Shading Death Phase
ax1.axvspan(15.5, 20.5, color='#FADBD8', alpha=0.4, label='Death Overs (Peak Pressure)')
ax1.axvspan(0.5, 6.5, color='#E8F8F5', alpha=0.4, label='Powerplay')

plt.title('The 20-Over Pressure Escalation Curve: Run Rate & Wicket Mortality by Over\nWhy Death Overs Represent the Most Extreme Tactical Crucible in Sport', fontsize=12, fontweight='bold', pad=12)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, facecolor='white')

plt.tight_layout()
plt.savefig('figures/fig6_over_pressure_curve.png')
plt.close()
print('Figure 6 saved.')

# 2. Figure 7: The 'Rise vs Dip' Slope Chart (Comparing Top Accelerators vs Regressors)
top_rise = ['Ruturaj Gaikwad', 'Naman Dhir', 'Ishan Kishan', 'Rishabh Pant', 'Virat Kohli']
top_dip = ['Curtis Campher', 'Washington Sundar', 'Deepak Hooda', 'Jimmy Neesham', 'Wanindu Hasaranga']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300)

# Accelerators
ax1.grid(True, linestyle='--', alpha=0.5)
for name in top_rise:
    row = bat[bat['striker_name'] == name].iloc[0]
    ax1.plot([0, 1], [row['sr_all'], row['sr_p']], marker='o', linewidth=2.5, label=f"{name} (+{row['delta_sr']:.1f})")
    ax1.text(-0.03, row['sr_all'], f"{row['sr_all']:.1f}", ha='right', va='center', fontsize=8.5, fontweight='bold')
    ax1.text(1.03, row['sr_p'], f"{row['sr_p']:.1f}", ha='left', va='center', fontsize=8.5, fontweight='bold')

ax1.set_xticks([0, 1])
ax1.set_xticklabels(['Usual Career Baseline', 'Under High Pressure'], fontsize=10, fontweight='bold')
ax1.set_ylabel('Strike Rate (Runs / 100 Balls)', fontsize=10, fontweight='bold')
ax1.set_title('CLUTCH RISERS: Accelerating Under Pressure\n(Turning Tension into Boundaries)', fontsize=11, fontweight='bold', color='#196F3D', pad=10)
ax1.legend(loc='lower left', fontsize=8.5, frameon=True)
ax1.set_ylim(130, 205)

# Regressors
ax2.grid(True, linestyle='--', alpha=0.5)
for name in top_dip:
    sub = bbb[bbb['striker_name'] == name]
    sr_all = (sub['runs'].sum() / max(sub['is_legal'].sum(), 1)) * 100
    sub_p = sub[sub['is_pressure']]
    sr_p = (sub_p['runs'].sum() / max(sub_p['is_legal'].sum(), 1)) * 100
    delta = sr_p - sr_all
    ax2.plot([0, 1], [sr_all, sr_p], marker='s', linewidth=2.5, label=f"{name} ({delta:.1f})")
    ax2.text(-0.03, sr_all, f"{sr_all:.1f}", ha='right', va='center', fontsize=8.5, fontweight='bold')
    ax2.text(1.03, sr_p, f"{sr_p:.1f}", ha='left', va='center', fontsize=8.5, fontweight='bold')

ax2.set_xticks([0, 1])
ax2.set_xticklabels(['Usual Career Baseline', 'Under High Pressure'], fontsize=10, fontweight='bold')
ax2.set_ylabel('Strike Rate (Runs / 100 Balls)', fontsize=10, fontweight='bold')
ax2.set_title('PRESSURE REGRESSORS: Stalling Under Tension\n(Retreating into a Defensive Shell)', fontsize=11, fontweight='bold', color='#922B21', pad=10)
ax2.legend(loc='lower left', fontsize=8.5, frameon=True)
ax2.set_ylim(105, 150)

plt.suptitle('The Psychological Divide: How Match Pressure Distinguishes True Clutch Stars', fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('figures/fig7_rise_vs_dip.png')
plt.close()
print('Figure 7 saved.')

