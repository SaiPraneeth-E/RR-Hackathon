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

is_pressure = is_super_over | inn2_death_pressure | inn2_mid_pressure | inn2_collapse_pressure | inn1_death_pressure | inn1_collapse_pressure
bbb['is_pressure'] = is_pressure

p_count = bbb['is_pressure'].sum()
p_pct = bbb['is_pressure'].mean() * 100
print(f'Overall deliveries: {len(bbb)}')
print(f'Pressure deliveries count: {p_count} ({p_pct:.1f}%)')
print('Breakdown:')
print(f'  Super over: {is_super_over.sum()}')
print(f'  Inn2 death pressure: {inn2_death_pressure.sum()}')
print(f'  Inn2 mid pressure: {inn2_mid_pressure.sum()}')
print(f'  Inn2 collapse pressure: {inn2_collapse_pressure.sum()}')
print(f'  Inn1 death pressure: {inn1_death_pressure.sum()}')
print(f'  Inn1 collapse pressure: {inn1_collapse_pressure.sum()}')

for label, df_sub in [('Pressure Situations', bbb[bbb['is_pressure']]), ('Ordinary Situations', bbb[~bbb['is_pressure']])]:
    runs_bat = df_sub['runs'].sum()
    balls_bat = df_sub['is_legal'].sum()
    sr = (runs_bat / balls_bat) * 100
    dots = (df_sub['runs'] == 0) & (df_sub['extras1_runs'] == 0)
    dot_pct = dots.mean() * 100
    bnd_pct = (df_sub['is_four'] | df_sub['is_six']).mean() * 100
    wickets = df_sub['is_wicket'].sum()
    balls_per_wkt = balls_bat / wickets if wickets > 0 else 0
    econ = (df_sub['total_ball_runs'].sum() / balls_bat) * 6
    print(f'\n=== {label} ===')
    print(f'Deliveries: {len(df_sub)}, Legal balls: {balls_bat}')
    print(f'Batting Strike Rate: {sr:.2f}')
    print(f'Dot Ball %: {dot_pct:.2f}%')
    print(f'Boundary %: {bnd_pct:.2f}%')
    print(f'Economy Rate: {econ:.2f}')
    print(f'Balls per Wicket: {balls_per_wkt:.2f}')

