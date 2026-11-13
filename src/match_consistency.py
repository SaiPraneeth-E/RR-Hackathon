import pandas as pd
import numpy as np

bbb = pd.read_pickle(r'src/enriched_bbb.pkl')
p_bbb = bbb[bbb['is_pressure']].copy()

# Match-level impact for batters
m_bat = p_bbb.groupby(['striker_id', 'striker_name', 'match_id']).agg(
    balls=('is_legal', 'sum'),
    runs=('runs', 'sum'),
    rva=('bat_rva', 'sum'),
    is_wicket=('is_wicket', 'sum')
).reset_index()

# Only count matches where batter faced at least 5 balls under pressure
m_bat_sig = m_bat[m_bat['balls'] >= 5]
consistency_bat = m_bat_sig.groupby(['striker_id', 'striker_name']).agg(
    sig_matches=('match_id', 'count'),
    pos_rva_matches=('rva', lambda x: (x > 0).sum()),
    rva_mean=('rva', 'mean'),
    rva_std=('rva', 'std')
).reset_index()

consistency_bat['win_impact_pct'] = (consistency_bat['pos_rva_matches'] / consistency_bat['sig_matches']) * 100

# Match-level impact for bowlers
m_bowl = p_bbb.groupby(['bowler_id', 'bowler_name', 'match_id']).agg(
    balls=('is_legal', 'sum'),
    bowler_runs=('bowler_runs', 'sum'),
    bva=('bowl_bva', 'sum'),
    wickets=('is_bowler_wicket', 'sum')
).reset_index()

m_bowl_sig = m_bowl[m_bowl['balls'] >= 6] # at least 1 pressure over
consistency_bowl = m_bowl_sig.groupby(['bowler_id', 'bowler_name']).agg(
    sig_matches=('match_id', 'count'),
    pos_bva_matches=('bva', lambda x: (x > 0).sum()),
    bva_mean=('bva', 'mean'),
    bva_std=('bva', 'std')
).reset_index()

consistency_bowl['win_impact_pct'] = (consistency_bowl['pos_bva_matches'] / consistency_bowl['sig_matches']) * 100

print('Top 15 Batters by Match Consistency (min 15 significant matches):')
print(consistency_bat[consistency_bat['sig_matches'] >= 15].sort_values('win_impact_pct', ascending=False).head(15).to_string())

print('\nTop 15 Bowlers by Match Consistency (min 15 significant matches):')
print(consistency_bowl[consistency_bowl['sig_matches'] >= 15].sort_values('win_impact_pct', ascending=False).head(15).to_string())

