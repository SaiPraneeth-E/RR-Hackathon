import pandas as pd
import numpy as np

bat = pd.read_pickle(r'src/final_bat_ranked.pkl')
bowl = pd.read_pickle(r'src/final_bowl_ranked.pkl')

def test_bat_weights(w_mastery, w_delta, w_volume):
    df = bat.copy()
    mastery = 0.5 * df['z_sr_p'] + 0.25 * df['z_avg_p'] + 0.25 * df['z_bnd_dot']
    delta = 0.7 * df['z_delta_sr'] + 0.3 * df['z_delta_avg']
    impact = 0.5 * df['z_total_rva'] + 0.3 * df['z_consistency'] + 0.2 * df['z_rva_rate']
    
    df['score'] = w_mastery * mastery + w_delta * delta + w_volume * impact
    df['rank'] = df['score'].rank(ascending=False, method='min').astype(int)
    return df.sort_values('rank')[['rank', 'striker_name', 'balls_p', 'sr_p', 'delta_sr', 'total_rva_p']].head(10)

def test_bowl_weights(w_mastery, w_delta, w_volume):
    df = bowl.copy()
    mastery = 0.45 * df['z_econ_p'] + 0.30 * df['z_sr_p'] + 0.25 * df['z_dot_p']
    delta = 0.70 * df['z_phase_delta_econ'] + 0.30 * df['z_delta_econ']
    impact = 0.50 * df['z_total_bva'] + 0.30 * df['z_consistency'] + 0.20 * df['z_bva_rate']
    
    df['score'] = w_mastery * mastery + w_delta * delta + w_volume * impact
    df['rank'] = df['score'].rank(ascending=False, method='min').astype(int)
    return df.sort_values('rank')[['rank', 'bowler_name', 'balls_p', 'econ_p', 'phase_delta_econ', 'total_bva_p']].head(10)

print('--- BATTERS (Balanced: 35/30/35) ---')
print(test_bat_weights(0.35, 0.30, 0.35).to_string(index=False))

print('\n--- BATTERS (Higher Volume/Impact: 30/25/45) ---')
print(test_bat_weights(0.30, 0.25, 0.45).to_string(index=False))

print('\n--- BOWLERS (Balanced: 35/30/35) ---')
print(test_bowl_weights(0.35, 0.30, 0.35).to_string(index=False))

print('\n--- BOWLERS (Higher Volume/Impact: 30/25/45) ---')
print(test_bowl_weights(0.30, 0.25, 0.45).to_string(index=False))
