import os
import pandas as pd
import numpy as np

data_dir = r'6af458274c1e8_data_pack\Data Pack'
matches = pd.read_csv(f'{data_dir}/matches.csv')
bbb = pd.read_csv(f'{data_dir}/ball_by_ball.csv')

bbb['total_ball_runs'] = bbb['runs'] + bbb['extras1_runs'] + bbb['extras_2_runs']
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

# Let's inspect batter performance overall vs pressure
bat_all = bbb.groupby(['striker_id', 'striker_name']).agg(
    balls_all=('is_legal', 'sum'),
    runs_all=('runs', 'sum'),
    dismissals_all=('is_wicket', 'sum'),
    dots_all=('runs', lambda x: (x == 0).sum()),
    boundaries_all=('is_four', lambda x: x.sum()) # approximate, will sum 4s and 6s
).reset_index()

# Add 6s
bat_all['sixes_all'] = bbb.groupby(['striker_id', 'striker_name'])['is_six'].sum().values
bat_all['fours_all'] = bbb.groupby(['striker_id', 'striker_name'])['is_four'].sum().values
bat_all['bnd_all'] = bat_all['fours_all'] + bat_all['sixes_all']
bat_all['sr_all'] = (bat_all['runs_all'] / np.maximum(bat_all['balls_all'], 1)) * 100
bat_all['avg_all'] = bat_all['runs_all'] / np.maximum(bat_all['dismissals_all'], 1)

# Now pressure
bbb_p = bbb[bbb['is_pressure']]
bat_p = bbb_p.groupby(['striker_id', 'striker_name']).agg(
    balls_p=('is_legal', 'sum'),
    runs_p=('runs', 'sum'),
    dismissals_p=('is_wicket', 'sum'),
    dots_p=('runs', lambda x: (x == 0).sum()),
    fours_p=('is_four', 'sum'),
    sixes_p=('is_six', 'sum')
).reset_index()

bat_p['bnd_p'] = bat_p['fours_p'] + bat_p['sixes_p']
bat_p['sr_p'] = (bat_p['runs_p'] / np.maximum(bat_p['balls_p'], 1)) * 100
bat_p['avg_p'] = bat_p['runs_p'] / np.maximum(bat_p['dismissals_p'], 1)
bat_p['dot_pct_p'] = (bat_p['dots_p'] / np.maximum(bat_p['balls_p'], 1)) * 100
bat_p['bnd_pct_p'] = (bat_p['bnd_p'] / np.maximum(bat_p['balls_p'], 1)) * 100

merged_bat = bat_p.merge(bat_all[['striker_id', 'balls_all', 'runs_all', 'sr_all', 'avg_all']], on='striker_id')
merged_bat['delta_sr'] = merged_bat['sr_p'] - merged_bat['sr_all']

print('Top 20 batters by balls_p (min 200 pressure balls):')
eligible_bat = merged_bat[merged_bat['balls_p'] >= 200].copy()
eligible_bat['clutch_score_raw'] = eligible_bat['sr_p'] * (eligible_bat['avg_p'] ** 0.3)
print(eligible_bat.sort_values('balls_p', ascending=False)[['striker_name', 'balls_p', 'runs_p', 'sr_p', 'avg_p', 'sr_all', 'delta_sr']].head(20).to_string())

