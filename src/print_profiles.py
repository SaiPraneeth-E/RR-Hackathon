import pandas as pd
bat = pd.read_pickle(r'src/final_bat_ranked.pkl')
bowl = pd.read_pickle(r'src/final_bowl_ranked.pkl')

print('=== TOP 10 BATTERS DETAILED ===')
for idx, r in bat.head(10).iterrows():
    pname = r['striker_name']
    pid = r['striker_id']
    rank = r['rank']
    bp = r['balls_p']
    rp = r['runs_p']
    srp = r['sr_p']
    avgp = r['avg_p']
    dotp = r['dot_pct_p']
    bndp = r['bnd_pct_p']
    ball = r['balls_all']
    rall = r['runs_all']
    srall = r['sr_all']
    avgall = r['avg_all']
    dsr = r['delta_sr']
    davg = r['delta_avg']
    ddot = r['delta_dot']
    trva = r['total_rva_p']
    rva100 = r['rva_per_100']
    wip = r['win_impact_pct']
    sigm = r['sig_matches']
    pri = r['PRI']
    
    print(f'Rank {rank}: {pname} (ID: {pid})')
    print(f'  Pressure: {bp} balls, {rp} runs, SR: {srp:.2f}, Avg: {avgp:.2f}, Dot%: {dotp:.1f}%, Bnd%: {bndp:.1f}%')
    print(f'  Baseline: {ball} balls, {rall} runs, SR: {srall:.2f}, Avg: {avgall:.2f}')
    print(f'  Deltas: ΔSR: +{dsr:.2f}, ΔAvg: {davg:.2f}, ΔDot%: -{ddot:.1f}%')
    print(f'  Impact: Total RVA: +{trva:.1f}, RVA/100: +{rva100:.2f}, Win Impact: {wip:.1f}% ({sigm:.0f} matches)')
    print(f'  PRI Score: {pri:.2f}\n')

print('=== TOP 10 BOWLERS DETAILED ===')
for idx, r in bowl.head(10).iterrows():
    pname = r['bowler_name']
    pid = r['bowler_id']
    rank = r['rank']
    bp = r['balls_p']
    wp = r['wickets_p']
    econp = r['econ_p']
    srp = r['sr_p']
    dotp = r['dot_pct_p']
    ds = r['death_share']
    ball = r['balls_all']
    econall = r['econ_all']
    srall = r['sr_all']
    decon = r['delta_econ']
    pdecon = r['phase_delta_econ']
    dsr = r['delta_sr']
    tbva = r['total_bva_p']
    bva100 = r['bva_per_100']
    wip = r['win_impact_pct']
    sigm = r['sig_matches']
    pri = r['PRI']
    
    print(f'Rank {rank}: {pname} (ID: {pid})')
    print(f'  Pressure: {bp} balls, {wp} wkts, Econ: {econp:.2f}, SR: {srp:.2f}, Dot%: {dotp:.1f}%, Death Share: {ds:.1f}%')
    print(f'  Baseline: {ball} balls, Econ: {econall:.2f}, SR: {srall:.2f}')
    print(f'  Deltas: ΔEcon: +{decon:.2f}, Phase ΔEcon: +{pdecon:.2f}, ΔSR: +{dsr:.2f}')
    print(f'  Impact: Total BVA: +{tbva:.1f}, BVA/100: +{bva100:.2f}, Win Impact: {wip:.1f}% ({sigm:.0f} matches)')
    print(f'  PRI Score: {pri:.2f}\n')
