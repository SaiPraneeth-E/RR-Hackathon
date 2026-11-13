import pandas as pd
import numpy as np
from scipy.stats import zscore

bat = pd.read_pickle(r'src/merged_bat.pkl')
bowl = pd.read_pickle(r'src/merged_bowl.pkl')
bbb = pd.read_pickle(r'src/enriched_bbb.pkl')
p_bbb = bbb[bbb['is_pressure']].copy()

# Add match-level consistency
m_bat = p_bbb.groupby(['striker_id', 'match_id']).agg(
    balls=('is_legal', 'sum'),
    rva=('bat_rva', 'sum')
).reset_index()
m_bat_sig = m_bat[m_bat['balls'] >= 5]
consistency_bat = m_bat_sig.groupby('striker_id').agg(
    sig_matches=('match_id', 'count'),
    pos_rva_matches=('rva', lambda x: (x > 0).sum())
).reset_index()
consistency_bat['win_impact_pct'] = (consistency_bat['pos_rva_matches'] / consistency_bat['sig_matches']) * 100

bat = bat.merge(consistency_bat[['striker_id', 'sig_matches', 'win_impact_pct']], on='striker_id', how='left').fillna({'win_impact_pct': 50.0, 'sig_matches': 0})

m_bowl = p_bbb.groupby(['bowler_id', 'match_id']).agg(
    balls=('is_legal', 'sum'),
    bva=('bowl_bva', 'sum')
).reset_index()
m_bowl_sig = m_bowl[m_bowl['balls'] >= 6]
consistency_bowl = m_bowl_sig.groupby('bowler_id').agg(
    sig_matches=('match_id', 'count'),
    pos_bva_matches=('bva', lambda x: (x > 0).sum())
).reset_index()
consistency_bowl['win_impact_pct'] = (consistency_bowl['pos_bva_matches'] / consistency_bowl['sig_matches']) * 100

bowl = bowl.merge(consistency_bowl[['bowler_id', 'sig_matches', 'win_impact_pct']], on='bowler_id', how='left').fillna({'win_impact_pct': 50.0, 'sig_matches': 0})

# Eligibility threshold: balls_p >= 200, sig_matches >= 15
def compute_bat_rankings(min_balls=200):
    df = bat[(bat['balls_p'] >= min_balls) & (bat['sig_matches'] >= 12)].copy()
    
    # Z-scores
    df['z_sr_p'] = zscore(df['shrunk_sr_p'])
    df['z_avg_p'] = zscore(df['shrunk_avg_p'])
    df['z_bnd_dot'] = zscore(df['bnd_pct_p'] - df['dot_pct_p'])
    df['z_rva_rate'] = zscore(df['rva_per_100'])
    df['z_delta_sr'] = zscore(df['delta_sr'])
    df['z_delta_avg'] = zscore(df['delta_avg'])
    df['z_consistency'] = zscore(df['win_impact_pct'])
    df['z_total_rva'] = zscore(np.log1p(np.maximum(df['total_rva_p'], 0)))
    
    # Composite PRI
    # 40% Mastery
    mastery = 0.15 * df['z_sr_p'] + 0.10 * df['z_avg_p'] + 0.10 * df['z_bnd_dot'] + 0.05 * df['z_rva_rate']
    # 30% Delta (Rise vs Dip)
    delta = 0.20 * df['z_delta_sr'] + 0.10 * df['z_delta_avg']
    # 30% Consistency & Impact
    consistency = 0.15 * df['z_consistency'] + 0.15 * df['z_total_rva']
    
    df['pri_raw'] = mastery + delta + consistency
    min_s, max_s = df['pri_raw'].min(), df['pri_raw'].max()
    df['PRI'] = ((df['pri_raw'] - min_s) / (max_s - min_s)) * 100
    df['rank'] = df['PRI'].rank(ascending=False, method='min').astype(int)
    return df.sort_values('rank')

def compute_bowl_rankings(min_balls=200):
    df = bowl[(bowl['balls_p'] >= min_balls) & (bowl['sig_matches'] >= 12)].copy()
    
    # Z-scores
    df['z_econ_p'] = zscore(-df['shrunk_econ_p'])
    df['z_sr_p'] = zscore(-df['shrunk_sr_p'])
    df['z_dot_p'] = zscore(df['dot_pct_p'])
    df['z_bva_rate'] = zscore(df['bva_per_100'])
    df['z_delta_econ'] = zscore(df['delta_econ'])
    df['z_delta_sr'] = zscore(df['delta_sr'])
    df['z_consistency'] = zscore(df['win_impact_pct'])
    df['z_total_bva'] = zscore(np.log1p(np.maximum(df['total_bva_p'], 0)))
    
    # Composite PRI
    # 40% Mastery
    mastery = 0.15 * df['z_econ_p'] + 0.10 * df['z_sr_p'] + 0.10 * df['z_dot_p'] + 0.05 * df['z_bva_rate']
    # 30% Delta (Rise vs Dip)
    delta = 0.20 * df['z_delta_econ'] + 0.10 * df['z_delta_sr']
    # 30% Consistency & Impact
    consistency = 0.15 * df['z_consistency'] + 0.15 * df['z_total_bva']
    
    df['pri_raw'] = mastery + delta + consistency
    min_s, max_s = df['pri_raw'].min(), df['pri_raw'].max()
    df['PRI'] = ((df['pri_raw'] - min_s) / (max_s - min_s)) * 100
    df['rank'] = df['PRI'].rank(ascending=False, method='min').astype(int)
    return df.sort_values('rank')

bat_ranked = compute_bat_rankings(min_balls=200)
bowl_ranked = compute_bowl_rankings(min_balls=200)

print('=== FINAL TOP 15 BATTERS UNDER PRESSURE ===')
bcols = ['rank', 'striker_name', 'balls_p', 'runs_p', 'sr_p', 'avg_p', 'sr_all', 'delta_sr', 'win_impact_pct', 'total_rva_p', 'PRI']
print(bat_ranked.head(15)[bcols].to_string(index=False))

print('\n=== FINAL TOP 15 BOWLERS UNDER PRESSURE ===')
bwcols = ['rank', 'bowler_name', 'balls_p', 'wickets_p', 'econ_p', 'sr_p', 'econ_all', 'delta_econ', 'win_impact_pct', 'total_bva_p', 'PRI']
print(bowl_ranked.head(15)[bwcols].to_string(index=False))

