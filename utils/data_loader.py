import os
import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_batters_data():
    """Load precalculated, official ranked batters data."""
    df = pd.read_pickle('src/final_bat_ranked.pkl')
    return df

@st.cache_data
def load_bowlers_data():
    """Load precalculated, official ranked bowlers data."""
    df = pd.read_pickle('src/final_bowl_ranked.pkl')
    return df

@st.cache_data
def load_macro_stats():
    """Load macro pressure comparison and over progression statistics."""
    return pd.read_pickle('src/macro_stats.pkl')

@st.cache_data
def load_team_stats():
    """Load team level pressure performance data."""
    return pd.read_pickle('src/team_stats.pkl')

@st.cache_data
def load_match_logs_bat():
    """Load batter match-by-match logs."""
    return pd.read_pickle('src/player_match_logs_bat.pkl')

@st.cache_data
def load_match_logs_bowl():
    """Load bowler match-by-match logs."""
    return pd.read_pickle('src/player_match_logs_bowl.pkl')

@st.cache_data
def load_player_splits():
    """Load situational splits (Pace/Spin, Phase, Innings)."""
    return pd.read_pickle('src/player_splits.pkl')

@st.cache_data
def load_player_mapping():
    """Load player-to-team and competition mapping."""
    if os.path.exists('src/competition_team_player_mapping.csv'):
        return pd.read_csv('src/competition_team_player_mapping.csv')
    return pd.read_csv('6af458274c1e8_data_pack/Data Pack/competition_team_player_mapping.csv')

@st.cache_data
def load_enriched_sample(n=20000):
    """Load a sample or filtered view of delivery-level data for explorer."""
    if os.path.exists('src/enriched_bbb.parquet'):
        df = pd.read_parquet('src/enriched_bbb.parquet')
    elif os.path.exists('src/enriched_bbb.pkl'):
        df = pd.read_pickle('src/enriched_bbb.pkl')
    else:
        raise FileNotFoundError("Delivery-level dataset not found.")
    if n and len(df) > n:
        return df.sample(n=n, random_state=42)
    return df
    if n and len(df) > n:
        return df.sample(n=n, random_state=42)
    return df

@st.cache_data
def get_all_players_catalog():
    """Returns a unified dictionary of all available players with roles and IDs."""
    bat = load_batters_data()
    bowl = load_bowlers_data()
    mapping = load_player_mapping()

    catalog = {}
    # Ranked Batters
    for _, r in bat.iterrows():
        pid = int(r['striker_id'])
        catalog[r['striker_name']] = {
            'player_id': pid,
            'name': r['striker_name'],
            'is_ranked_bat': True,
            'bat_rank': int(r['rank']),
            'bat_pri': float(r['PRI']),
            'is_ranked_bowl': False,
            'bowl_rank': None,
            'bowl_pri': None,
            'primary_role': 'Batter'
        }
    
    # Ranked Bowlers
    for _, r in bowl.iterrows():
        pid = int(r['bowler_id'])
        name = r['bowler_name']
        if name in catalog:
            catalog[name]['is_ranked_bowl'] = True
            catalog[name]['bowl_rank'] = int(r['rank'])
            catalog[name]['bowl_pri'] = float(r['PRI'])
            catalog[name]['primary_role'] = 'All-Rounder'
        else:
            catalog[name] = {
                'player_id': pid,
                'name': name,
                'is_ranked_bat': False,
                'bat_rank': None,
                'bat_pri': None,
                'is_ranked_bowl': True,
                'bowl_rank': int(r['rank']),
                'bowl_pri': float(r['PRI']),
                'primary_role': 'Bowler'
            }
            
    # Add team affiliations
    team_grouped = mapping.groupby('player_id')['team_name'].unique().to_dict()
    for name, data in catalog.items():
        pid = data['player_id']
        teams = team_grouped.get(pid, [])
        # Format top 3 unique teams
        clean_teams = [t for t in list(teams) if pd.notna(t)][:3]
        data['teams'] = ", ".join(clean_teams) if clean_teams else "Unknown"

    return catalog

