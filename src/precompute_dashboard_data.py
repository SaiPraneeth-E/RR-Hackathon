import pandas as pd
import numpy as np
import os

print("Loading enriched ball-by-ball and metadata...")
bbb = pd.read_pickle('src/enriched_bbb.pkl')
matches = pd.read_csv('6af458274c1e8_data_pack/Data Pack/matches.csv')
teams = pd.read_csv('6af458274c1e8_data_pack/Data Pack/teams.csv')
comps = pd.read_csv('6af458274c1e8_data_pack/Data Pack/competitions.csv')
mapping = pd.read_csv('6af458274c1e8_data_pack/Data Pack/competition_team_player_mapping.csv')

# Build team id to name lookup
team_map = dict(zip(teams['team_id'], teams['team_name']))
# Also add from matches if any missing
for _, r in matches.iterrows():
    if pd.notna(r['home_team_id']) and r['home_team_id'] not in team_map:
        team_map[r['home_team_id']] = r['home_team']
    if pd.notna(r['away_team_id']) and r['away_team_id'] not in team_map:
        team_map[r['away_team_id']] = r['away_team']

match_meta = matches[['match_id', 'match_date', 'venue_country']].drop_duplicates()

print("1. Computing Player Match Logs (Batting)...")
# Filter legal balls for batting
legal_b = bbb[bbb['is_legal']].copy()
legal_b = legal_b.merge(match_meta, on='match_id', how='left')
legal_b['bat_team_name'] = legal_b['batting_team_id'].map(team_map).fillna('Unknown')
legal_b['bowl_team_name'] = legal_b['bowling_team_id'].map(team_map).fillna('Unknown')
legal_b['is_win'] = (legal_b['win_team_id'] == legal_b['batting_team_id'])

# Batting match logs
bat_all = legal_b.groupby(['striker_id', 'striker_name', 'match_id', 'match_date', 'comp_name', 'bat_team_name', 'bowl_team_name', 'stage', 'is_win']).agg(
    balls_all=('runs', 'count'),
    runs_all=('runs', 'sum'),
    rva_all=('bat_rva', 'sum'),
    fours_all=('is_four', 'sum'),
    sixes_all=('is_six', 'sum'),
    dots_all=('runs', lambda x: (x == 0).sum())
).reset_index()

bat_p = legal_b[legal_b['is_pressure']].groupby(['striker_id', 'match_id']).agg(
    balls_p=('runs', 'count'),
    runs_p=('runs', 'sum'),
    rva_p=('bat_rva', 'sum'),
    fours_p=('is_four', 'sum'),
    sixes_p=('is_six', 'sum'),
    dots_p=('runs', lambda x: (x == 0).sum())
).reset_index()

bat_logs = bat_all.merge(bat_p, on=['striker_id', 'match_id'], how='left')
bat_logs['balls_p'] = bat_logs['balls_p'].fillna(0).astype(int)
bat_logs['runs_p'] = bat_logs['runs_p'].fillna(0).astype(int)
bat_logs['rva_p'] = bat_logs['rva_p'].fillna(0.0)
bat_logs['fours_p'] = bat_logs['fours_p'].fillna(0).astype(int)
bat_logs['sixes_p'] = bat_logs['sixes_p'].fillna(0).astype(int)
bat_logs['dots_p'] = bat_logs['dots_p'].fillna(0).astype(int)
bat_logs['sr_all'] = (bat_logs['runs_all'] / bat_logs['balls_all'] * 100).round(1)
bat_logs['sr_p'] = np.where(bat_logs['balls_p'] > 0, (bat_logs['runs_p'] / bat_logs['balls_p'] * 100).round(1), np.nan)
bat_logs.sort_values(by=['match_date', 'striker_name'], ascending=[False, True], inplace=True)
bat_logs.to_pickle('src/player_match_logs_bat.pkl')
print(f"Batting logs saved: {bat_logs.shape}")

print("2. Computing Player Match Logs (Bowling)...")
# Bowling balls
legal_bowl = bbb[bbb['is_legal']].copy()
legal_bowl = legal_bowl.merge(match_meta, on='match_id', how='left')
legal_bowl['bowl_team_name'] = legal_bowl['bowling_team_id'].map(team_map).fillna('Unknown')
legal_bowl['bat_team_name'] = legal_bowl['batting_team_id'].map(team_map).fillna('Unknown')
legal_bowl['is_win'] = (legal_bowl['win_team_id'] == legal_bowl['bowling_team_id'])

bowl_all = legal_bowl.groupby(['bowler_id', 'bowler_name', 'match_id', 'match_date', 'comp_name', 'bowl_team_name', 'bat_team_name', 'stage', 'is_win']).agg(
    balls_all=('bowler_runs', 'count'),
    runs_all=('bowler_runs', 'sum'),
    wkts_all=('is_bowler_wicket', 'sum'),
    bva_all=('bowl_bva', 'sum'),
    dots_all=('bowler_runs', lambda x: (x == 0).sum())
).reset_index()

bowl_p = legal_bowl[legal_bowl['is_pressure']].groupby(['bowler_id', 'match_id']).agg(
    balls_p=('bowler_runs', 'count'),
    runs_p=('bowler_runs', 'sum'),
    wkts_p=('is_bowler_wicket', 'sum'),
    bva_p=('bowl_bva', 'sum'),
    dots_p=('bowler_runs', lambda x: (x == 0).sum())
).reset_index()

bowl_logs = bowl_all.merge(bowl_p, on=['bowler_id', 'match_id'], how='left')
bowl_logs['balls_p'] = bowl_logs['balls_p'].fillna(0).astype(int)
bowl_logs['runs_p'] = bowl_logs['runs_p'].fillna(0).astype(int)
bowl_logs['wkts_p'] = bowl_logs['wkts_p'].fillna(0).astype(int)
bowl_logs['bva_p'] = bowl_logs['bva_p'].fillna(0.0)
bowl_logs['dots_p'] = bowl_logs['dots_p'].fillna(0).astype(int)
bowl_logs['econ_all'] = (bowl_logs['runs_all'] / (bowl_logs['balls_all'] / 6)).round(2)
bowl_logs['econ_p'] = np.where(bowl_logs['balls_p'] > 0, (bowl_logs['runs_p'] / (bowl_logs['balls_p'] / 6)).round(2), np.nan)
bowl_logs.sort_values(by=['match_date', 'bowler_name'], ascending=[False, True], inplace=True)
bowl_logs.to_pickle('src/player_match_logs_bowl.pkl')
print(f"Bowling logs saved: {bowl_logs.shape}")

print("3. Computing Player Splits (Pace/Spin, Phase, Innings)...")
# Batting Splits
bat_splits = {}
# Phase splits
b_phase = legal_b.groupby(['striker_id', 'phase', 'is_pressure']).agg(
    balls=('runs', 'count'),
    runs=('runs', 'sum'),
    rva=('bat_rva', 'sum'),
    dots=('runs', lambda x: (x == 0).sum()),
    dismissals=('is_wicket', 'sum')
).reset_index()

# Pace/Spin splits
b_pace = legal_b.groupby(['striker_id', 'pace_or_spin', 'is_pressure']).agg(
    balls=('runs', 'count'),
    runs=('runs', 'sum'),
    rva=('bat_rva', 'sum'),
    dots=('runs', lambda x: (x == 0).sum()),
    dismissals=('is_wicket', 'sum')
).reset_index()

# Innings splits
b_inngs = legal_b.groupby(['striker_id', 'innings', 'is_pressure']).agg(
    balls=('runs', 'count'),
    runs=('runs', 'sum'),
    rva=('bat_rva', 'sum'),
    dots=('runs', lambda x: (x == 0).sum()),
    dismissals=('is_wicket', 'sum')
).reset_index()

# Bowling Splits
bowl_phase = legal_bowl.groupby(['bowler_id', 'phase', 'is_pressure']).agg(
    balls=('bowler_runs', 'count'),
    runs=('bowler_runs', 'sum'),
    bva=('bowl_bva', 'sum'),
    dots=('bowler_runs', lambda x: (x == 0).sum()),
    wkts=('is_bowler_wicket', 'sum')
).reset_index()

bowl_hand = legal_bowl.groupby(['bowler_id', 'batting_type', 'is_pressure']).agg(
    balls=('bowler_runs', 'count'),
    runs=('bowler_runs', 'sum'),
    bva=('bowl_bva', 'sum'),
    dots=('bowler_runs', lambda x: (x == 0).sum()),
    wkts=('is_bowler_wicket', 'sum')
).reset_index()

bowl_inngs = legal_bowl.groupby(['bowler_id', 'innings', 'is_pressure']).agg(
    balls=('bowler_runs', 'count'),
    runs=('bowler_runs', 'sum'),
    bva=('bowl_bva', 'sum'),
    dots=('bowler_runs', lambda x: (x == 0).sum()),
    wkts=('is_bowler_wicket', 'sum')
).reset_index()

splits_dict = {
    'bat_phase': b_phase,
    'bat_pace': b_pace,
    'bat_inngs': b_inngs,
    'bowl_phase': bowl_phase,
    'bowl_hand': bowl_hand,
    'bowl_inngs': bowl_inngs
}
pd.to_pickle(splits_dict, 'src/player_splits.pkl')
print("Player splits saved successfully.")

print("4. Computing Team Analytics...")
# Team pressure batting & bowling stats
team_bat = legal_b.groupby(['bat_team_name', 'is_pressure']).agg(
    balls=('runs', 'count'),
    runs=('runs', 'sum'),
    fours=('is_four', 'sum'),
    sixes=('is_six', 'sum'),
    dots=('runs', lambda x: (x == 0).sum()),
    wkts=('is_wicket', 'sum'),
    rva=('bat_rva', 'sum')
).reset_index()

team_bowl = legal_bowl.groupby(['bowl_team_name', 'is_pressure']).agg(
    balls=('bowler_runs', 'count'),
    runs=('bowler_runs', 'sum'),
    fours=('is_four', 'sum'),
    sixes=('is_six', 'sum'),
    dots=('bowler_runs', lambda x: (x == 0).sum()),
    wkts=('is_bowler_wicket', 'sum'),
    bva=('bowl_bva', 'sum')
).reset_index()

# Aggregate team summary
team_summary = []
all_team_names = sorted(list(set(team_bat['bat_team_name']).union(set(team_bowl['bowl_team_name']))))
for tm in all_team_names:
    if tm == 'Unknown': continue
    tb_p = team_bat[(team_bat['bat_team_name'] == tm) & (team_bat['is_pressure'])]
    tb_all = team_bat[(team_bat['bat_team_name'] == tm)]
    tbo_p = team_bowl[(team_bowl['bowl_team_name'] == tm) & (team_bowl['is_pressure'])]
    tbo_all = team_bowl[(team_bowl['bowl_team_name'] == tm)]
    
    b_balls_p = tb_p['balls'].sum() if len(tb_p) > 0 else 0
    b_runs_p = tb_p['runs'].sum() if len(tb_p) > 0 else 0
    bo_balls_p = tbo_p['balls'].sum() if len(tbo_p) > 0 else 0
    bo_runs_p = tbo_p['runs'].sum() if len(tbo_p) > 0 else 0
    
    if b_balls_p >= 150 or bo_balls_p >= 150:
        bat_sr_p = round((b_runs_p / b_balls_p * 100), 1) if b_balls_p > 0 else 0
        bowl_econ_p = round((bo_runs_p / (bo_balls_p / 6)), 2) if bo_balls_p > 0 else 0
        net_margin = round((bat_sr_p / 100 * 6) - bowl_econ_p, 2)
        team_summary.append({
            'team_name': tm,
            'p_bat_balls': b_balls_p,
            'p_bat_runs': b_runs_p,
            'p_bat_sr': bat_sr_p,
            'p_bowl_balls': bo_balls_p,
            'p_bowl_runs': bo_runs_p,
            'p_bowl_econ': bowl_econ_p,
            'net_pressure_margin': net_margin,
            'p_bat_rva': round(tb_p['rva'].sum(), 1) if len(tb_p) > 0 else 0,
            'p_bowl_bva': round(tbo_p['bva'].sum(), 1) if len(tbo_p) > 0 else 0
        })

team_df = pd.DataFrame(team_summary).sort_values(by='net_pressure_margin', ascending=False)
team_df.to_pickle('src/team_stats.pkl')
print(f"Team stats saved: {team_df.shape}")

print("5. Computing Macro Stats & Over Curves...")
# Over by over progression
over_prog = bbb.groupby('overid').agg(
    total_balls=('runs', 'count'),
    pressure_balls=('is_pressure', 'sum'),
    runs=('total_ball_runs', 'sum'),
    wickets=('is_wicket', 'sum'),
    dots=('total_ball_runs', lambda x: (x == 0).sum()),
    boundaries=('runs', lambda x: (x >= 4).sum())
).reset_index()

over_prog['over_num'] = over_prog['overid'] + 1
over_prog['pressure_pct'] = (over_prog['pressure_balls'] / over_prog['total_balls'] * 100).round(1)
over_prog['run_rate'] = (over_prog['runs'] / (over_prog['total_balls'] / 6)).round(2)
over_prog['wicket_freq_balls'] = (over_prog['total_balls'] / over_prog['wickets']).round(1)
over_prog['dot_pct'] = (over_prog['dots'] / over_prog['total_balls'] * 100).round(1)
over_prog['boundary_pct'] = (over_prog['boundaries'] / over_prog['total_balls'] * 100).round(1)

# Macro comparison
macro_compare = {
    'Pressure': {
        'balls': int(bbb['is_pressure'].sum()),
        'runs_per_over': round(float(bbb[bbb['is_pressure']]['total_ball_runs'].sum() / (bbb['is_pressure'].sum() / 6)), 2),
        'dot_pct': round(float((bbb[bbb['is_pressure']]['total_ball_runs'] == 0).sum() / bbb['is_pressure'].sum() * 100), 1),
        'boundary_pct': round(float((bbb[bbb['is_pressure']]['runs'] >= 4).sum() / bbb['is_pressure'].sum() * 100), 1),
        'wicket_freq_balls': round(float(bbb['is_pressure'].sum() / bbb[bbb['is_pressure']]['is_wicket'].sum()), 1)
    },
    'Ordinary': {
        'balls': int((~bbb['is_pressure']).sum()),
        'runs_per_over': round(float(bbb[~bbb['is_pressure']]['total_ball_runs'].sum() / ((~bbb['is_pressure']).sum() / 6)), 2),
        'dot_pct': round(float((bbb[~bbb['is_pressure']]['total_ball_runs'] == 0).sum() / (~bbb['is_pressure']).sum() * 100), 1),
        'boundary_pct': round(float((bbb[~bbb['is_pressure']]['runs'] >= 4).sum() / (~bbb['is_pressure']).sum() * 100), 1),
        'wicket_freq_balls': round(float((~bbb['is_pressure']).sum() / bbb[~bbb['is_pressure']]['is_wicket'].sum()), 1)
    }
}

macro_dict = {
    'over_prog': over_prog,
    'macro_compare': macro_compare
}
pd.to_pickle(macro_dict, 'src/macro_stats.pkl')
print("Macro stats saved successfully!")
print("ALL PRECOMPUTATION FINISHED!")
