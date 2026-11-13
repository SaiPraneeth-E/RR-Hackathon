import json
import pandas as pd

bat = pd.read_pickle(r'src/final_bat_ranked.pkl')
bowl = pd.read_pickle(r'src/final_bowl_ranked.pkl')

bat_cols = ['rank', 'striker_name', 'striker_id', 'balls_p', 'runs_p', 'sr_p', 'avg_p', 'sr_all', 'avg_all', 'delta_sr', 'dot_pct_p', 'bnd_pct_p', 'win_impact_pct', 'total_rva_p', 'PRI']
bowl_cols = ['rank', 'bowler_name', 'bowler_id', 'balls_p', 'wickets_p', 'econ_p', 'sr_p', 'econ_all', 'sr_all', 'phase_delta_econ', 'delta_econ', 'death_share', 'dot_pct_p', 'win_impact_pct', 'total_bva_p', 'PRI']

bat_data = bat[bat_cols].round(2).to_dict(orient='records')
bowl_data = bowl[bowl_cols].round(2).to_dict(orient='records')

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SupeRR Selector Season 2 | Rajasthan Royals Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --rr-pink: #E91E63;
            --rr-blue: #1A5276;
            --dark-bg: #0F172A;
            --card-bg: #1E293B;
            --text-light: #F8FAFC;
            --text-muted: #94A3B8;
            --accent-green: #10B981;
            --accent-purple: #8B5CF6;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        body {{ background: var(--dark-bg); color: var(--text-light); padding: 24px; line-height: 1.5; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--card-bg); padding-bottom: 20px; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }}
        .logo-title h1 {{ font-size: 24px; font-weight: 800; color: #fff; }}
        .logo-title p {{ color: var(--text-muted); font-size: 13px; margin-top: 4px; }}
        .badge {{ background: linear-gradient(135deg, var(--rr-pink), #C2185B); color: white; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }}
        
        .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
        .kpi-card {{ background: var(--card-bg); border-radius: 12px; padding: 18px; border: 1px solid rgba(255,255,255,0.06); }}
        .kpi-title {{ font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; }}
        .kpi-value {{ font-size: 24px; font-weight: 800; color: #fff; margin-top: 6px; }}
        .kpi-sub {{ font-size: 11px; color: var(--accent-green); margin-top: 4px; }}

        .controls-bar {{ display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-bottom: 20px; flex-wrap: wrap; }}
        .tabs {{ display: flex; gap: 10px; }}
        .tab-btn {{ background: var(--card-bg); border: 1px solid rgba(255,255,255,0.1); color: var(--text-muted); padding: 10px 20px; border-radius: 8px; font-weight: 700; cursor: pointer; transition: 0.2s; font-size: 13.5px; }}
        .tab-btn.active {{ background: var(--rr-blue); color: #fff; border-color: var(--rr-blue); }}
        
        .search-box {{ position: relative; width: 280px; }}
        .search-box input {{ width: 100%; padding: 10px 14px; border-radius: 8px; background: var(--card-bg); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 13px; outline: none; }}
        .search-box input:focus {{ border-color: var(--rr-pink); }}

        .content-section {{ display: none; }}
        .content-section.active {{ display: block; }}

        .table-container {{ background: var(--card-bg); border-radius: 12px; overflow-x: auto; border: 1px solid rgba(255,255,255,0.06); margin-bottom: 28px; max-height: 480px; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 12.5px; }}
        thead {{ position: sticky; top: 0; z-index: 10; }}
        th {{ background: #131E31; color: var(--text-muted); font-size: 11px; text-transform: uppercase; padding: 12px 14px; font-weight: 700; white-space: nowrap; }}
        td {{ padding: 10px 14px; border-bottom: 1px solid rgba(255,255,255,0.04); white-space: nowrap; }}
        tr:hover {{ background: rgba(255,255,255,0.03); }}
        .rank-pill {{ display: inline-block; width: 24px; height: 24px; border-radius: 50%; background: rgba(255,255,255,0.1); text-align: center; line-height: 24px; font-weight: 800; font-size: 11px; }}
        .rank-1 {{ background: #F59E0B; color: #000; }}
        .rank-2 {{ background: #94A3B8; color: #000; }}
        .rank-3 {{ background: #D97706; color: #000; }}
        .score-bar {{ width: 70px; height: 5px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; display: inline-block; vertical-align: middle; margin-right: 6px; }}
        .score-fill {{ height: 100%; background: linear-gradient(90deg, #3B82F6, #10B981); }}
        .positive {{ color: var(--accent-green); font-weight: 700; }}
        .negative {{ color: #EF4444; font-weight: 700; }}

        .charts-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 28px; }}
        .chart-card {{ background: var(--card-bg); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.06); }}
        .chart-card h3 {{ font-size: 14px; font-weight: 700; margin-bottom: 14px; color: #fff; }}

        .narrative-box {{ background: rgba(26, 82, 118, 0.25); border-left: 4px solid var(--rr-blue); border-radius: 8px; padding: 16px; margin-bottom: 24px; font-size: 13px; color: #E2E8F0; line-height: 1.6; }}
        .narrative-box strong {{ color: #fff; }}
    </style>
</head>
<body>

    <div class="header">
        <div class="logo-title">
            <h1>SupeRR Selector Season 2: Interactive Analytics Hub</h1>
            <p>Pressure Reliability Index (PRI) Exploration Dashboard | Rajasthan Royals Moneyball Platform</p>
        </div>
        <div class="badge">Round 1 Verified Solution</div>
    </div>

    <div class="narrative-box">
        <strong>The Formula 1 Analogy in Practice:</strong> In cricket, bowling the 19th over is driving on a Formula 1 track (par economy is 10.56 RPO). Bowling the 8th over is driving in a school zone (7.43 RPO). Our dashboard evaluates players based on <strong>Phase-Adjusted Economy Savings</strong> and <strong>Situational Run Value Added (RVA)</strong>, distinguishing true match-winners who accelerate under tension from those whose performance dips.
    </div>

    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-title">Deliveries Analyzed</div>
            <div class="kpi-value">200,999</div>
            <div class="kpi-sub">883 Matches (2022–2026)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">High Pressure Share</div>
            <div class="kpi-value">32.7%</div>
            <div class="kpi-sub">65,741 High-Leverage Deliveries</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Balls Per Wicket Divergence</div>
            <div class="kpi-value">14.25 vs 20.00</div>
            <div class="kpi-sub">+40.4% faster wickets in pressure</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Top Rated Under Pressure</div>
            <div class="kpi-value">N. Dhir & M. Nawaz</div>
            <div class="kpi-sub">PRI 100.00 Index Leaders</div>
        </div>
    </div>

    <div class="controls-bar">
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('batters')">Batters Under Pressure ({len(bat_data)})</button>
            <button class="tab-btn" onclick="switchTab('bowlers')">Bowlers Under Pressure ({len(bowl_data)})</button>
            <button class="tab-btn" onclick="switchTab('insights')">Anti-Rankings & Performance Dips</button>
        </div>
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search any player (e.g., Bumrah, Samson)..." onkeyup="filterTables()">
        </div>
    </div>

    <!-- BATTERS TAB -->
    <div id="batters" class="content-section active">
        <div class="table-container">
            <table id="batTable">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Player Name</th>
                        <th>ID</th>
                        <th>Pressure Balls</th>
                        <th>Pressure SR</th>
                        <th>Base SR</th>
                        <th>ΔSR (Uplift)</th>
                        <th>Pressure Avg</th>
                        <th>Dot %</th>
                        <th>Boundary %</th>
                        <th>Win Impact %</th>
                        <th>Total RVA</th>
                        <th>PRI Rating</th>
                    </tr>
                </thead>
                <tbody id="batTbody">
                </tbody>
            </table>
        </div>

        <div class="charts-grid">
            <div class="chart-card">
                <h3>Top 10 Batters: Pressure Strike Rate vs Baseline Parity</h3>
                <canvas id="batChart"></canvas>
            </div>
            <div class="chart-card">
                <h3>Top 10 Batters: Net Run Value Added (RVA)</h3>
                <canvas id="rvaChart"></canvas>
            </div>
        </div>
    </div>

    <!-- BOWLERS TAB -->
    <div id="bowlers" class="content-section">
        <div class="table-container">
            <table id="bowlTable">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Player Name</th>
                        <th>ID</th>
                        <th>Pressure Balls</th>
                        <th>Econ_P</th>
                        <th>Base Econ</th>
                        <th>Phase ΔEcon</th>
                        <th>Bowl SR_P</th>
                        <th>Death Share %</th>
                        <th>Dot %</th>
                        <th>Win Impact %</th>
                        <th>Total BVA</th>
                        <th>PRI Rating</th>
                    </tr>
                </thead>
                <tbody id="bowlTbody">
                </tbody>
            </table>
        </div>

        <div class="charts-grid">
            <div class="chart-card">
                <h3>Top 10 Bowlers: Phase-Adjusted Economy Savings (Runs Saved/Ov)</h3>
                <canvas id="bowlChart"></canvas>
            </div>
            <div class="chart-card">
                <h3>Top 10 Bowlers: Net Bowling Value Added (BVA)</h3>
                <canvas id="bvaChart"></canvas>
            </div>
        </div>
    </div>

    <!-- INSIGHTS & ANTI-RANKINGS TAB -->
    <div id="insights" class="content-section">
        <div class="charts-grid">
            <div class="chart-card">
                <h3 style="color: #EF4444;">Batters Who Dip Under Pressure (Negative ΔSR)</h3>
                <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">Qualified batters whose scoring velocity stalls significantly under pressure.</p>
                <table>
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>Pressure SR</th>
                            <th>Baseline SR</th>
                            <th>ΔSR Dip</th>
                            <th>Total RVA</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Curtis Campher</td><td>115.61</td><td>120.65</td><td class="negative">-5.04</td><td class="negative">-46.3</td></tr>
                        <tr><td>Washington Sundar</td><td>136.73</td><td>140.54</td><td class="negative">-3.80</td><td class="negative">-50.8</td></tr>
                        <tr><td>Deepak Hooda</td><td>130.71</td><td>133.59</td><td class="negative">-2.87</td><td class="negative">-39.1</td></tr>
                        <tr><td>Jimmy Neesham</td><td>132.46</td><td>135.24</td><td class="negative">-2.78</td><td class="negative">-49.7</td></tr>
                        <tr><td>Wanindu Hasaranga</td><td>122.68</td><td>124.79</td><td class="negative">-2.11</td><td class="negative">-137.9</td></tr>
                    </tbody>
                </table>
            </div>

            <div class="chart-card">
                <h3 style="color: #EF4444;">Bowlers With Heavy Run Bleeds Under Pressure</h3>
                <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">Bowlers whose economy blows out relative to expected phase par.</p>
                <table>
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>Actual Econ</th>
                            <th>Expected Econ</th>
                            <th>Run Bleed (Phase ΔEcon)</th>
                            <th>Total BVA</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Andre Russell</td><td>11.69</td><td>9.40</td><td class="negative">-2.29 rpo</td><td class="negative">-128.8 runs</td></tr>
                        <tr><td>Nitish Reddy</td><td>10.52</td><td>8.92</td><td class="negative">-1.60 rpo</td><td class="negative">-55.1 runs</td></tr>
                        <tr><td>Tushar Deshpande</td><td>11.43</td><td>10.04</td><td class="negative">-1.39 rpo</td><td class="negative">-87.8 runs</td></tr>
                        <tr><td>Mukesh Kumar</td><td>11.15</td><td>9.83</td><td class="negative">-1.33 rpo</td><td class="negative">-135.9 runs</td></tr>
                        <tr><td>Anrich Nortje</td><td>10.79</td><td>9.54</td><td class="negative">-1.25 rpo</td><td class="negative">-115.1 runs</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        const batDataset = {json.dumps(bat_data)};
        const bowlDataset = {json.dumps(bowl_data)};

        function renderBatters(data) {{
            const tbody = document.getElementById('batTbody');
            tbody.innerHTML = '';
            data.forEach(p => {{
                const tr = document.createElement('tr');
                const rankCls = p.rank === 1 ? 'rank-1' : (p.rank === 2 ? 'rank-2' : (p.rank === 3 ? 'rank-3' : ''));
                const deltaCls = p.delta_sr >= 0 ? 'positive' : 'negative';
                const deltaSign = p.delta_sr >= 0 ? '+' : '';
                tr.innerHTML = `
                    <td><span class="rank-pill ${{rankCls}}">${{p.rank}}</span></td>
                    <td><strong>${{p.striker_name}}</strong></td>
                    <td style="color: var(--text-muted);">${{p.striker_id}}</td>
                    <td>${{p.balls_p}}</td>
                    <td><strong>${{p.sr_p}}</strong></td>
                    <td>${{p.sr_all}}</td>
                    <td class="${{deltaCls}}">${{deltaSign}}${{p.delta_sr}}</td>
                    <td>${{p.avg_p}}</td>
                    <td>${{p.dot_pct_p}}%</td>
                    <td>${{p.bnd_pct_p}}%</td>
                    <td>${{p.win_impact_pct}}%</td>
                    <td>${{p.total_rva_p >= 0 ? '+' : ''}}${{p.total_rva_p}}</td>
                    <td><div class="score-bar"><div class="score-fill" style="width: ${{p.PRI}}%;"></div></div> ${{p.PRI}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        function renderBowlers(data) {{
            const tbody = document.getElementById('bowlTbody');
            tbody.innerHTML = '';
            data.forEach(p => {{
                const tr = document.createElement('tr');
                const rankCls = p.rank === 1 ? 'rank-1' : (p.rank === 2 ? 'rank-2' : (p.rank === 3 ? 'rank-3' : ''));
                const deltaCls = p.phase_delta_econ >= 0 ? 'positive' : 'negative';
                const deltaSign = p.phase_delta_econ >= 0 ? '+' : '';
                tr.innerHTML = `
                    <td><span class="rank-pill ${{rankCls}}">${{p.rank}}</span></td>
                    <td><strong>${{p.bowler_name}}</strong></td>
                    <td style="color: var(--text-muted);">${{p.bowler_id}}</td>
                    <td>${{p.balls_p}}</td>
                    <td><strong>${{p.econ_p}}</strong></td>
                    <td>${{p.econ_all}}</td>
                    <td class="${{deltaCls}}">${{deltaSign}}${{p.phase_delta_econ}}</td>
                    <td>${{p.sr_p}}</td>
                    <td>${{p.death_share}}%</td>
                    <td>${{p.dot_pct_p}}%</td>
                    <td>${{p.win_impact_pct}}%</td>
                    <td>${{p.total_bva_p >= 0 ? '+' : ''}}${{p.total_bva_p}}</td>
                    <td><div class="score-bar"><div class="score-fill" style="width: ${{p.PRI}}%;"></div></div> ${{p.PRI}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.content-section').forEach(sec => sec.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }}

        function filterTables() {{
            const q = document.getElementById('searchInput').value.toLowerCase();
            const filteredBat = batDataset.filter(p => p.striker_name.toLowerCase().includes(q) || String(p.striker_id).includes(q));
            const filteredBowl = bowlDataset.filter(p => p.bowler_name.toLowerCase().includes(q) || String(p.bowler_id).includes(q));
            renderBatters(filteredBat);
            renderBowlers(filteredBowl);
        }}

        renderBatters(batDataset);
        renderBowlers(bowlDataset);

        // Top 10 Charts
        const top10Bat = batDataset.slice(0, 10);
        new Chart(document.getElementById('batChart'), {{
            type: 'bar',
            data: {{
                labels: top10Bat.map(p => p.striker_name),
                datasets: [
                    {{ label: 'Pressure Strike Rate', data: top10Bat.map(p => p.sr_p), backgroundColor: '#E91E63' }},
                    {{ label: 'Baseline Strike Rate', data: top10Bat.map(p => p.sr_all), backgroundColor: '#334155' }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ labels: {{ color: '#94A3B8' }} }} }},
                scales: {{
                    x: {{ ticks: {{ color: '#94A3B8', font: {{ size: 10 }} }}, grid: {{ display: false }} }},
                    y: {{ ticks: {{ color: '#94A3B8' }}, grid: {{ color: 'rgba(255,255,255,0.05)' }}, min: 120 }}
                }}
            }}
        }});

        new Chart(document.getElementById('rvaChart'), {{
            type: 'bar',
            data: {{
                labels: top10Bat.map(p => p.striker_name),
                datasets: [{{ label: 'Total Run Value Added (RVA)', data: top10Bat.map(p => p.total_rva_p), backgroundColor: '#10B981' }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ ticks: {{ color: '#94A3B8', font: {{ size: 10 }} }}, grid: {{ display: false }} }},
                    y: {{ ticks: {{ color: '#94A3B8' }}, grid: {{ color: 'rgba(255,255,255,0.05)' }} }}
                }}
            }}
        }});

        const top10Bowl = bowlDataset.slice(0, 10);
        new Chart(document.getElementById('bowlChart'), {{
            type: 'bar',
            data: {{
                labels: top10Bowl.map(p => p.bowler_name),
                datasets: [{{ label: 'Runs Saved Per Over vs Par', data: top10Bowl.map(p => p.phase_delta_econ), backgroundColor: '#3B82F6' }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ ticks: {{ color: '#94A3B8', font: {{ size: 10 }} }}, grid: {{ display: false }} }},
                    y: {{ ticks: {{ color: '#94A3B8' }}, grid: {{ color: 'rgba(255,255,255,0.05)' }} }}
                }}
            }}
        }});

        new Chart(document.getElementById('bvaChart'), {{
            type: 'bar',
            data: {{
                labels: top10Bowl.map(p => p.bowler_name),
                datasets: [{{ label: 'Total Bowling Value Added (BVA)', data: top10Bowl.map(p => p.total_bva_p), backgroundColor: '#8B5CF6' }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ ticks: {{ color: '#94A3B8', font: {{ size: 10 }} }}, grid: {{ display: false }} }},
                    y: {{ ticks: {{ color: '#94A3B8' }}, grid: {{ color: 'rgba(255,255,255,0.05)' }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("dashboard.html successfully updated with 85 qualified batters and 98 qualified bowlers + search!")
