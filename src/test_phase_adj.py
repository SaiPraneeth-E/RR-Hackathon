import pandas as pd
import numpy as np

bbb = pd.read_pickle(r'src/enriched_bbb.pkl')
p_bbb = bbb[bbb['is_pressure']].copy()

# Expected runs per ball by phase across all pressure balls
phase_exp = p_bbb.groupby('phase')['bowler_runs'].mean() * 6
print('Phase expected economy in pressure:')
print(phase_exp)

# Per bowler expected economy in pressure based on their exact delivery phases
p_bowl_phase = p_bbb.groupby(['bowler_id', 'bowler_name']).agg(
    balls_p=('is_legal', 'sum'),
    runs_p=('bowler_runs', 'sum'),
    exp_runs_p=('exp_bowler_runs', 'sum'),
    wickets_p=('is_bowler_wicket', 'sum'),
    total_bva_p=('bowl_bva', 'sum'),
    death_balls=('is_legal', lambda x: x[p_bbb.loc[x.index, 'phase'] == 'Death'].sum())
).reset_index()

p_bowl_phase['econ_p'] = (p_bowl_phase['runs_p'] / p_bowl_phase['balls_p']) * 6
p_bowl_phase['exp_econ_p'] = (p_bowl_phase['exp_runs_p'] / p_bowl_phase['balls_p']) * 6
p_bowl_phase['phase_delta_econ'] = p_bowl_phase['exp_econ_p'] - p_bowl_phase['econ_p'] # positive means saved runs relative to phase par!
p_bowl_phase['death_share'] = (p_bowl_phase['death_balls'] / p_bowl_phase['balls_p']) * 100

print('\nTop 20 bowlers by phase_delta_econ (min 200 balls):')
print(p_bowl_phase[p_bowl_phase['balls_p'] >= 200].sort_values('phase_delta_econ', ascending=False)[['bowler_name', 'balls_p', 'death_share', 'econ_p', 'exp_econ_p', 'phase_delta_econ', 'total_bva_p']].head(20).to_string())

