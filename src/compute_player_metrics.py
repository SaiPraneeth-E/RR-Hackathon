import pandas as pd
import numpy as np

bbb = pd.read_pickle(r'src/enriched_bbb.pkl')

# ----------------- BATTING ANALYSIS -----------------
# Overall baseline per batter
bat_all = bbb.groupby(['striker_id', 'striker_name']).agg(
    balls_all=('is_legal', 'sum'),
    runs_all=('runs', 'sum'),
    dismissals_all=('is_wicket', 'sum'),
    dots_all=('runs', lambda x: (x == 0).sum()),
    fours_all=('is_four', 'sum'),
    sixes_all=('is_six', 'sum'),
    matches_all=('match_id', 'nunique')
).reset_index()

bat_all['sr_all'] = (bat_all['runs_all'] / np.maximum(bat_all['balls_all'], 1)) * 100
bat_all['avg_all'] = bat_all['runs_all'] / np.maximum(bat_all['dismissals_all'], 1)
bat_all['dot_pct_all'] = (bat_all['dots_all'] / np.maximum(bat_all['balls_all'], 1)) * 100
bat_all['bnd_pct_all'] = ((bat_all['fours_all'] + bat_all['sixes_all']) / np.maximum(bat_all['balls_all'], 1)) * 100

# Pressure subset
bbb_p = bbb[bbb['is_pressure']].copy()
bat_p = bbb_p.groupby(['striker_id', 'striker_name']).agg(
    balls_p=('is_legal', 'sum'),
    runs_p=('runs', 'sum'),
    dismissals_p=('is_wicket', 'sum'),
    dots_p=('runs', lambda x: (x == 0).sum()),
    fours_p=('is_four', 'sum'),
    sixes_p=('is_six', 'sum'),
    matches_p=('match_id', 'nunique'),
    total_rva_p=('bat_rva', 'sum'),
    knockout_balls=('is_legal', lambda x: x[bbb_p.loc[x.index, 'knock_out'] == 1].sum())
).reset_index()

bat_p['sr_p'] = (bat_p['runs_p'] / np.maximum(bat_p['balls_p'], 1)) * 100
bat_p['avg_p'] = bat_p['runs_p'] / np.maximum(bat_p['dismissals_p'], 1)
bat_p['dot_pct_p'] = (bat_p['dots_p'] / np.maximum(bat_p['balls_p'], 1)) * 100
bat_p['bnd_pct_p'] = ((bat_p['fours_p'] + bat_p['sixes_p']) / np.maximum(bat_p['balls_p'], 1)) * 100
bat_p['rva_per_100'] = (bat_p['total_rva_p'] / np.maximum(bat_p['balls_p'], 1)) * 100

merged_bat = bat_p.merge(bat_all[['striker_id', 'balls_all', 'runs_all', 'sr_all', 'avg_all', 'dot_pct_all', 'bnd_pct_all']], on='striker_id')
merged_bat['delta_sr'] = merged_bat['sr_p'] - merged_bat['sr_all']
merged_bat['delta_avg'] = merged_bat['avg_p'] - merged_bat['avg_all']
merged_bat['delta_dot'] = merged_bat['dot_pct_all'] - merged_bat['dot_pct_p'] # positive means fewer dots under pressure

# Population priors for Bayesian shrinkage
pop_sr_p = (bbb_p['runs'].sum() / bbb_p['is_legal'].sum()) * 100
pop_avg_p = bbb_p['runs'].sum() / bbb_p['is_wicket'].sum()
k_balls_bat = 60
k_dismissals_bat = 4

merged_bat['shrunk_sr_p'] = (merged_bat['runs_p'] + (pop_sr_p * k_balls_bat / 100)) / (merged_bat['balls_p'] + k_balls_bat) * 100
merged_bat['shrunk_avg_p'] = (merged_bat['runs_p'] + (pop_avg_p * k_dismissals_bat)) / (merged_bat['dismissals_p'] + k_dismissals_bat)

print(f'Population Pressure SR: {pop_sr_p:.2f}, Population Pressure Avg: {pop_avg_p:.2f}')
print('Total batters with >= 150 pressure balls:', (merged_bat['balls_p'] >= 150).sum())
print('Total batters with >= 100 pressure balls:', (merged_bat['balls_p'] >= 100).sum())

# ----------------- BOWLING ANALYSIS -----------------
bowl_all = bbb.groupby(['bowler_id', 'bowler_name']).agg(
    balls_all=('is_legal', 'sum'),
    runs_all=('bowler_runs', 'sum'),
    wickets_all=('is_bowler_wicket', 'sum'),
    dots_all=('bowler_runs', lambda x: (x == 0).sum()),
    fours_all=('is_four', 'sum'),
    sixes_all=('is_six', 'sum'),
    matches_all=('match_id', 'nunique')
).reset_index()

bowl_all['econ_all'] = (bowl_all['runs_all'] / np.maximum(bowl_all['balls_all'], 1)) * 6
bowl_all['sr_all'] = bowl_all['balls_all'] / np.maximum(bowl_all['wickets_all'], 1)
bowl_all['dot_pct_all'] = (bowl_all['dots_all'] / np.maximum(bowl_all['balls_all'], 1)) * 100

bowl_p = bbb_p.groupby(['bowler_id', 'bowler_name']).agg(
    balls_p=('is_legal', 'sum'),
    runs_p=('bowler_runs', 'sum'),
    wickets_p=('is_bowler_wicket', 'sum'),
    dots_p=('bowler_runs', lambda x: (x == 0).sum()),
    fours_p=('is_four', 'sum'),
    sixes_p=('is_six', 'sum'),
    matches_p=('match_id', 'nunique'),
    total_bva_p=('bowl_bva', 'sum'),
    knockout_balls=('is_legal', lambda x: x[bbb_p.loc[x.index, 'knock_out'] == 1].sum())
).reset_index()

bowl_p['econ_p'] = (bowl_p['runs_p'] / np.maximum(bowl_p['balls_p'], 1)) * 6
bowl_p['sr_p'] = bowl_p['balls_p'] / np.maximum(bowl_p['wickets_p'], 1)
bowl_p['dot_pct_p'] = (bowl_p['dots_p'] / np.maximum(bowl_p['balls_p'], 1)) * 100
bowl_p['bnd_pct_p'] = ((bowl_p['fours_p'] + bowl_p['sixes_p']) / np.maximum(bowl_p['balls_p'], 1)) * 100
bowl_p['bva_per_100'] = (bowl_p['total_bva_p'] / np.maximum(bowl_p['balls_p'], 1)) * 100

merged_bowl = bowl_p.merge(bowl_all[['bowler_id', 'balls_all', 'runs_all', 'econ_all', 'sr_all', 'dot_pct_all']], on='bowler_id')
merged_bowl['delta_econ'] = merged_bowl['econ_all'] - merged_bowl['econ_p'] # positive means tighter under pressure!
merged_bowl['delta_sr'] = merged_bowl['sr_all'] - merged_bowl['sr_p'] # positive means strikes faster under pressure!
merged_bowl['delta_dot'] = merged_bowl['dot_pct_p'] - merged_bowl['dot_pct_all'] # positive means more dots under pressure!

pop_econ_p = (bbb_p['bowler_runs'].sum() / bbb_p['is_legal'].sum()) * 6
pop_bowl_sr_p = bbb_p['is_legal'].sum() / bbb_p['is_bowler_wicket'].sum()
k_balls_bowl = 60
k_wickets_bowl = 4

merged_bowl['shrunk_econ_p'] = (merged_bowl['runs_p'] + (pop_econ_p * k_balls_bowl / 6)) / (merged_bowl['balls_p'] + k_balls_bowl) * 6
merged_bowl['shrunk_sr_p'] = (merged_bowl['balls_p'] + (pop_bowl_sr_p * k_wickets_bowl)) / (merged_bowl['wickets_p'] + k_wickets_bowl)

print(f'Population Pressure Econ: {pop_econ_p:.2f}, Population Pressure Bowl SR: {pop_bowl_sr_p:.2f}')
print('Total bowlers with >= 150 pressure balls:', (merged_bowl['balls_p'] >= 150).sum())
print('Total bowlers with >= 100 pressure balls:', (merged_bowl['balls_p'] >= 100).sum())

merged_bat.to_pickle(r'src/merged_bat.pkl')
merged_bowl.to_pickle(r'src/merged_bowl.pkl')

