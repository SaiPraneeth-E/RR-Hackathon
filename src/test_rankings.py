import pandas as pd
import numpy as np

bat = pd.read_pickle(r'src/merged_bat.pkl')
bowl = pd.read_pickle(r'src/merged_bowl.pkl')

# Let's inspect batting rankings with a standardized Z-score composite
# Minimum sample: balls_p >= 150 (approx 25 overs of pressure cricket across multiple matches)
b150 = bat[bat['balls_p'] >= 150].copy()

# Features for Batting:
# 1. Shrunk SR under pressure
# 2. Shrunk Avg under pressure
# 3. Delta SR (SR_p - SR_all)
# 4. Delta Avg (Avg_p - Avg_all)
# 5. Boundary - Dot difference in pressure
# 6. RVA per 100 balls in pressure
# 7. Total RVA (volume of positive pressure impact)

from scipy.stats import zscore

# Z-scores
b150['z_sr_p'] = zscore(b150['shrunk_sr_p'])
b150['z_avg_p'] = zscore(b150['shrunk_avg_p'])
b150['z_delta_sr'] = zscore(b150['delta_sr'])
b150['z_bnd_dot'] = zscore(b150['bnd_pct_p'] - b150['dot_pct_p'])
b150['z_rva_rate'] = zscore(b150['rva_per_100'])
b150['z_total_rva'] = zscore(np.log1p(np.maximum(b150['total_rva_p'], 0)))

# Let's test a composite:
# 35% Absolute Pressure Efficiency (shrunk SR, Avg, Bnd-Dot)
# 30% Value Added (RVA rate & Total RVA)
# 35% Clutch Elevation / Delta (Delta SR, Delta Avg)
b150['bat_pressure_score'] = (
    0.20 * b150['z_sr_p'] +
    0.15 * b150['z_avg_p'] +
    0.15 * b150['z_bnd_dot'] +
    0.20 * b150['z_rva_rate'] +
    0.10 * b150['z_total_rva'] +
    0.20 * b150['z_delta_sr']
)

# Normalize to 0-100 scale
min_s, max_s = b150['bat_pressure_score'].min(), b150['bat_pressure_score'].max()
b150['rating_100'] = ((b150['bat_pressure_score'] - min_s) / (max_s - min_s)) * 100

print('=== TOP 20 BATTERS UNDER PRESSURE (Min 150 balls) ===')
cols = ['striker_name', 'balls_p', 'runs_p', 'sr_p', 'avg_p', 'sr_all', 'delta_sr', 'total_rva_p', 'rva_per_100', 'rating_100']
top_bat = b150.sort_values('rating_100', ascending=False)[cols].head(20)
print(top_bat.to_string())

# Bowlers
b150_bowl = bowl[bowl['balls_p'] >= 150].copy()

# Features for Bowling:
# 1. Shrunk Econ under pressure (lower is better -> invert)
# 2. Shrunk SR under pressure (lower is better -> invert)
# 3. Delta Econ (Econ_all - Econ_p, higher is better)
# 4. Dot % under pressure
# 5. BVA per 100 balls in pressure
# 6. Total BVA (volume of positive pressure bowling impact)

b150_bowl['z_econ_p'] = zscore(-b150_bowl['shrunk_econ_p'])
b150_bowl['z_sr_p'] = zscore(-b150_bowl['shrunk_sr_p'])
b150_bowl['z_delta_econ'] = zscore(b150_bowl['delta_econ'])
b150_bowl['z_dot_p'] = zscore(b150_bowl['dot_pct_p'])
b150_bowl['z_bva_rate'] = zscore(b150_bowl['bva_per_100'])
b150_bowl['z_total_bva'] = zscore(np.log1p(np.maximum(b150_bowl['total_bva_p'], 0)))

b150_bowl['bowl_pressure_score'] = (
    0.25 * b150_bowl['z_econ_p'] +
    0.20 * b150_bowl['z_sr_p'] +
    0.15 * b150_bowl['z_dot_p'] +
    0.20 * b150_bowl['z_bva_rate'] +
    0.10 * b150_bowl['z_total_bva'] +
    0.10 * b150_bowl['z_delta_econ']
)

min_sb, max_sb = b150_bowl['bowl_pressure_score'].min(), b150_bowl['bowl_pressure_score'].max()
b150_bowl['rating_100'] = ((b150_bowl['bowl_pressure_score'] - min_sb) / (max_sb - min_sb)) * 100

print('\n=== TOP 20 BOWLERS UNDER PRESSURE (Min 150 balls) ===')
bcols = ['bowler_name', 'balls_p', 'wickets_p', 'econ_p', 'sr_p', 'econ_all', 'delta_econ', 'dot_pct_p', 'total_bva_p', 'rating_100']
top_bowl = b150_bowl.sort_values('rating_100', ascending=False)[bcols].head(20)
print(top_bowl.to_string())

