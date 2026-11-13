import os
import pandas as pd
import numpy as np

data_dir = r'6af458274c1e8_data_pack\Data Pack'
matches = pd.read_csv(f'{data_dir}/matches.csv')
comp = pd.read_csv(f'{data_dir}/competitions.csv')
teams = pd.read_csv(f'{data_dir}/teams.csv')
bbb = pd.read_csv(f'{data_dir}/ball_by_ball.csv')

# 1. Match & Competition Weighting
top_tier_teams = {
    'India', 'Australia', 'England', 'South Africa', 'Pakistan', 
    'New Zealand', 'West Indies', 'Sri Lanka', 'Afghanistan'
}

matches = matches.merge(comp[['comp_id', 'comp_name', 'match_format']], on='comp_id', how='left')

def get_comp_tier(row):
    comp_name = str(row['comp_name'])
    m_format = str(row['match_format'])
    if 'IPL' in comp_name:
        return 1.15  # Premier franchise league
    home_t = str(row['home_team'])
    away_t = str(row['away_team'])
    if home_t in top_tier_teams and away_t in top_tier_teams:
        return 1.10  # Tier 1 International
    elif home_t in top_tier_teams or away_t in top_tier_teams:
        return 1.00  # Tier 2 International
    else:
        return 0.90  # Lower tier

matches['comp_tier'] = matches.apply(get_comp_tier, axis=1)
matches['knockout_mult'] = np.where(matches['knock_out'] == 1, 1.25, 1.0)
matches['context_weight'] = matches['comp_tier'] * matches['knockout_mult']

# 2. Cumulative match state
bbb['total_ball_runs'] = bbb['runs'] + bbb['extras1_runs'] + bbb['extras_2_runs']
bbb['bowler_runs'] = bbb['runs'] + np.where(bbb['extras_type'].isin(['wide', 'Overstep', 'other']), bbb['extras1_runs'] + bbb['extras_2_runs'], 0)
bbb['is_legal'] = ~bbb['extras_type'].isin(['wide', 'Overstep', 'other'])
bbb['is_bowler_wicket'] = bbb['is_wicket'] & bbb['dismissal_type'].isin(['Bowled', 'Caught', 'LBW', 'Stump', 'Hit Wicket'])

inn1_runs = bbb[bbb['innings'] == 1].groupby('match_id')['total_ball_runs'].sum().to_dict()
matches['inn1_runs'] = matches['match_id'].map(inn1_runs)
matches['target'] = np.where(matches['revised_target'].notna(), matches['revised_target'], matches['inn1_runs'] + 1)

bbb = bbb.merge(matches[['match_id', 'target', 'win_team_id', 'knock_out', 'stage', 'context_weight', 
                         'second_inn_revised_overs', 'first_inn_revised_overs', 'comp_name', 'match_format']], 
                on='match_id', how='left')

bbb['runs_before'] = bbb.groupby(['match_id', 'innings'])['total_ball_runs'].cumsum() - bbb['total_ball_runs']
bbb['wickets_before'] = bbb.groupby(['match_id', 'innings'])['is_wicket'].cumsum() - bbb['is_wicket']
bbb['legal_balls_before'] = bbb.groupby(['match_id', 'innings'])['is_legal'].cumsum() - bbb['is_legal']

total_balls_inn2 = np.where(bbb['second_inn_revised_overs'].notna(), bbb['second_inn_revised_overs'] * 6, 120)
bbb['balls_rem'] = np.where(bbb['innings'] == 2, np.maximum(total_balls_inn2 - bbb['legal_balls_before'], 0), np.maximum(120 - bbb['legal_balls_before'], 0))
bbb['runs_req'] = np.where(bbb['innings'] == 2, np.maximum(bbb['target'] - bbb['runs_before'], 0), 0)
bbb['wickets_in_hand'] = 10 - bbb['wickets_before']
bbb['rrr'] = np.where((bbb['innings'] == 2) & (bbb['balls_rem'] > 0), (bbb['runs_req'] / bbb['balls_rem']) * 6, 0.0)

def get_phase(overid):
    if overid <= 6:
        return 'Powerplay'
    elif overid <= 15:
        return 'Middle'
    else:
        return 'Death'

bbb['phase'] = bbb['overid'].apply(get_phase)

# Pressure conditions
is_super_over = bbb['innings'] >= 3
inn2_death_pressure = (bbb['innings'] == 2) & (bbb['balls_rem'] <= 36) & (bbb['rrr'] >= 6.0) & (bbb['rrr'] <= 22.0) & (bbb['runs_req'] <= 80) & (bbb['wickets_in_hand'] <= 8)
inn2_mid_pressure = (bbb['innings'] == 2) & (bbb['balls_rem'] > 36) & (bbb['balls_rem'] <= 84) & ((bbb['rrr'] >= 10.0) & (bbb['wickets_in_hand'] <= 7))
inn2_collapse_pressure = (bbb['innings'] == 2) & (bbb['legal_balls_before'] <= 48) & (bbb['wickets_before'] >= 3)
inn1_death_pressure = (bbb['innings'] == 1) & (bbb['overid'] >= 16)
inn1_collapse_pressure = (bbb['innings'] == 1) & (bbb['legal_balls_before'] <= 60) & (bbb['wickets_before'] >= 3)

bbb['is_pressure'] = is_super_over | inn2_death_pressure | inn2_mid_pressure | inn2_collapse_pressure | inn1_death_pressure | inn1_collapse_pressure

# Detailed subcategory of pressure for expectation baselines
def get_situation_key(row):
    if not row['is_pressure']:
        return f"Ordinary_{row['innings']}_{row['phase']}"
    if row['innings'] >= 3:
        return 'Super_Over'
    if row['innings'] == 2:
        if row['balls_rem'] <= 36:
            return 'Inn2_Death_Pressure'
        elif row['legal_balls_before'] <= 48 and row['wickets_before'] >= 3:
            return 'Inn2_Collapse_Pressure'
        else:
            return 'Inn2_Mid_Pressure'
    else:
        if row['overid'] >= 16:
            return 'Inn1_Death_Pressure'
        else:
            return 'Inn1_Collapse_Pressure'

bbb['situation_key'] = bbb.apply(get_situation_key, axis=1)

# Baseline expectations by situation key
exp_stats = bbb.groupby('situation_key').agg(
    exp_runs=('runs', 'mean'),
    exp_bowler_runs=('bowler_runs', 'mean'),
    exp_wicket=('is_bowler_wicket', 'mean'),
    exp_batter_out=('is_wicket', 'mean')
).to_dict('index')

bbb['exp_runs'] = bbb['situation_key'].map(lambda k: exp_stats[k]['exp_runs'])
bbb['exp_bowler_runs'] = bbb['situation_key'].map(lambda k: exp_stats[k]['exp_bowler_runs'])
bbb['exp_wicket'] = bbb['situation_key'].map(lambda k: exp_stats[k]['exp_wicket'])
bbb['exp_batter_out'] = bbb['situation_key'].map(lambda k: exp_stats[k]['exp_batter_out'])

# Value Added per delivery
# For batter: runs scored above expectation - wicket cost
bbb['bat_rva'] = bbb['context_weight'] * ((bbb['runs'] - bbb['exp_runs']) - 3.5 * (bbb['is_wicket'].astype(int) - bbb['exp_batter_out']))

# For bowler: runs saved above expectation + wicket bonus
bbb['bowl_bva'] = bbb['context_weight'] * ((bbb['exp_bowler_runs'] - bbb['bowler_runs']) + 3.5 * (bbb['is_bowler_wicket'].astype(int) - bbb['exp_wicket']))

print('Expectations per situation key:')
for k, v in exp_stats.items():
    print(f'  {k}: exp_runs={v["exp_runs"]:.2f}, exp_bowler_runs={v["exp_bowler_runs"]:.2f}, exp_wicket={v["exp_wicket"]*100:.2f}%')

# Save enriched data as pickle
bbb.to_pickle(r'src/enriched_bbb.pkl')
print('Enriched ball_by_ball saved successfully as pickle!')
