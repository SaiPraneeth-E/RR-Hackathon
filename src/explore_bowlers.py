import os
import pandas as pd
import numpy as np

data_dir = r'6af458274c1e8_data_pack\Data Pack'
matches = pd.read_csv(f'{data_dir}/matches.csv')
bbb = pd.read_csv(f'{data_dir}/ball_by_ball.csv')

bbb['total_ball_runs'] = bbb['runs'] + bbb['extras1_runs'] + bbb['extras_2_runs']
# Bowler conceded runs: runs off bat + wides + noballs. Legbyes and byes are NOT bowler conceded!
bbb['bowler_runs'] = bbb['runs'] + np.where(bbb['extras_type'].isin(['wide', 'Overstep', 'other']), bbb['extras1_runs'] + bbb['extras_2_runs'], 0)
bbb['is_legal'] = ~bbb['extras_type'].isin(['wide', 'Overstep', 'other'])
bbb['is_bowler_wicket'] = bbb['is_wicket'] & bbb['dismissal_type'].isin(['Bowled', 'Caught', 'LBW', 'Stump', 'Hit Wicket'])

inn1_runs = bbb[bbb['innings'] == 1].groupby('match_id')['total_ball_runs'].sum().to_dict()
matches['inn1_runs'] = matches['match_id'].map(inn1_runs)
matches['target'] = np.where(matches['revised_target'].notna(), matches['revised_target'], matches['inn1_runs'] + 1)

bbb = bbb.merge(matches[['match_id', 'target', 'win_team_id', 'knock_out', 'stage', 'second_inn_revised_overs', 'first_inn_revised_overs']], on='match_id', how='left')

bbb['runs_before'] = bbb.groupby(['match_id', 'innings'])['total_ball_runs'].cumsum() - bbb['total_ball_runs']
bbb['wickets_before'] = bbb.groupby(['match_id', 'innings'])['is_wicket'].cumsum() - bbb['is_wicket']
bbb['legal_balls_before'] = bbb.groupby(['match_id', 'innings'])['is_legal'].cumsum() - bbb['is_legal']

total_balls_inn2 = np.where(bbb['second_inn_revised_overs'].notna(), bbb['second_inn_revised_overs'] * 6, 120)
bbb['balls_rem'] = np.where(bbb['innings'] == 2, np.maximum(total_balls_inn2 - bbb['legal_balls_before'], 0), np.maximum(120 - bbb['legal_balls_before'], 0))
bbb['runs_req'] = np.where(bbb['innings'] == 2, np.maximum(bbb['target'] - bbb['runs_before'], 0), 0)
bbb['wickets_in_hand'] = 10 - bbb['wickets_before']
bbb['rrr'] = np.where((bbb['innings'] == 2) & (bbb['balls_rem'] > 0), (bbb['runs_req'] / bbb['balls_rem']) * 6, 0.0)

is_super_over = bbb['innings'] >= 3
inn2_death_pressure = (bbb['innings'] == 2) & (bbb['balls_rem'] <= 36) & (bbb['rrr'] >= 6.0) & (bbb['rrr'] <= 22.0) & (bbb['runs_req'] <= 80) & (bbb['wickets_in_hand'] <= 8)
inn2_mid_pressure = (bbb['innings'] == 2) & (bbb['balls_rem'] > 36) & (bbb['balls_rem'] <= 84) & ((bbb['rrr'] >= 10.0) & (bbb['wickets_in_hand'] <= 7))
inn2_collapse_pressure = (bbb['innings'] == 2) & (bbb['legal_balls_before'] <= 48) & (bbb['wickets_before'] >= 3)
inn1_death_pressure = (bbb['innings'] == 1) & (bbb['overid'] >= 16)
inn1_collapse_pressure = (bbb['innings'] == 1) & (bbb['legal_balls_before'] <= 60) & (bbb['wickets_before'] >= 3)

bbb['is_pressure'] = is_super_over | inn2_death_pressure | inn2_mid_pressure | inn2_collapse_pressure | inn1_death_pressure | inn1_collapse_pressure

# Overall bowler stats
bowl_all = bbb.groupby(['bowler_id', 'bowler_name']).agg(
    balls_all=('is_legal', 'sum'),
    runs_all=('bowler_runs', 'sum'),
    wickets_all=('is_bowler_wicket', 'sum'),
    dots_all=('bowler_runs', lambda x: (x == 0).sum())
).reset_index()

bowl_all['econ_all'] = (bowl_all['runs_all'] / np.maximum(bowl_all['balls_all'], 1)) * 6
bowl_all['sr_all'] = bowl_all['balls_all'] / np.maximum(bowl_all['wickets_all'], 1)
bowl_all['dot_pct_all'] = (bowl_all['dots_all'] / np.maximum(bowl_all['balls_all'], 1)) * 100

# Pressure bowler stats
bbb_p = bbb[bbb['is_pressure']]
bowl_p = bbb_p.groupby(['bowler_id', 'bowler_name']).agg(
    balls_p=('is_legal', 'sum'),
    runs_p=('bowler_runs', 'sum'),
    wickets_p=('is_bowler_wicket', 'sum'),
    dots_p=('bowler_runs', lambda x: (x == 0).sum()),
    fours_p=('is_four', 'sum'),
    sixes_p=('is_six', 'sum')
).reset_index()

bowl_p['econ_p'] = (bowl_p['runs_p'] / np.maximum(bowl_p['balls_p'], 1)) * 6
bowl_p['sr_p'] = bowl_p['balls_p'] / np.maximum(bowl_p['wickets_p'], 1)
bowl_p['dot_pct_p'] = (bowl_p['dots_p'] / np.maximum(bowl_p['balls_p'], 1)) * 100
bowl_p['bnd_pct_p'] = ((bowl_p['fours_p'] + bowl_p['sixes_p']) / np.maximum(bowl_p['balls_p'], 1)) * 100

merged_bowl = bowl_p.merge(bowl_all[['bowler_id', 'balls_all', 'runs_all', 'econ_all', 'sr_all', 'dot_pct_all']], on='bowler_id')
merged_bowl['delta_econ'] = merged_bowl['econ_all'] - merged_bowl['econ_p'] # positive means tighter under pressure!

print('Top 20 bowlers by balls_p (min 200 pressure balls):')
eligible_bowl = merged_bowl[merged_bowl['balls_p'] >= 200].copy()
print(eligible_bowl.sort_values('balls_p', ascending=False)[['bowler_name', 'balls_p', 'runs_p', 'wickets_p', 'econ_p', 'sr_p', 'econ_all', 'delta_econ', 'dot_pct_p']].head(20).to_string())

