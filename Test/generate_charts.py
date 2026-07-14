import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_reports_and_charts(results_path="reports/test_results.json", output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(results_path):
        print(f"No test results JSON file found at {results_path}")
        return
        
    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    if not data:
        print("No test data found.")
        return
        
    df = pd.DataFrame(data)
    
    # Configure plotting style
    sns.set_theme(style="darkgrid")
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.titlesize': 16
    })
    
    # Track which charts were generated
    charts_generated = []

    # 1. Execution Times for Random Graphs vs. Number of Vertices
    df_random = df[df["case"].str.startswith("aleatorio")].copy()
    if not df_random.empty:
        df_random_avg = df_random.groupby(["algorithm", "num_vertices"])["time_taken"].mean().reset_index()
        
        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=df_random_avg, 
            x="num_vertices", 
            y="time_taken", 
            hue="algorithm", 
            marker="o", 
            linewidth=2.5,
            markersize=8
        )
        plt.axhline(y=5.0, color="red", linestyle="--", linewidth=1.5, label="Límite (5s)")
        plt.title("Tiempo de Ejecución Promedio vs. Vértices (Grafos Aleatorios)")
        plt.xlabel("Número de Vértices (N)")
        plt.ylabel("Tiempo de Ejecución Promedio (segundos)")
        plt.legend(title="Algoritmo")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "execution_times_random.png"), dpi=150)
        plt.close()
        charts_generated.append(("execution_times_random.png", "Tiempo de Ejecución Promedio vs. Vértices (Grafos Aleatorios)"))
        
    # 2. Execution Times for Manual Graphs
    df_manual = df[~df["case"].str.startswith("aleatorio")].copy()
    if not df_manual.empty:
        df_manual_avg = df_manual.groupby(["algorithm", "case"])["time_taken"].mean().reset_index()
        
        plt.figure(figsize=(12, 6))
        sns.barplot(
            data=df_manual_avg,
            x="case",
            y="time_taken",
            hue="algorithm"
        )
        plt.axhline(y=5.0, color="red", linestyle="--", linewidth=1.5, label="Límite (5s)")
        plt.title("Tiempo de Ejecución Promedio por Caso (Grafos Manuales)")
        plt.xlabel("Caso de Prueba")
        plt.ylabel("Tiempo de Ejecución (segundos)")
        plt.xticks(rotation=45, ha="right")
        plt.legend(title="Algoritmo")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "execution_times_manual.png"), dpi=150)
        plt.close()
        charts_generated.append(("execution_times_manual.png", "Tiempo de Ejecución Promedio por Caso (Grafos Manuales)"))
        
    # 3. Colors Used vs Optimal (Random Graphs)
    if not df_random.empty:
        def get_optimal_k(case_name):
            try:
                parts = case_name.split("_")
                for p in parts:
                    if p.startswith("k") and p[1:].isdigit():
                        return int(p[1:])
            except:
                pass
            return None
            
        df_random["optimal_k"] = df_random["case"].apply(get_optimal_k)
        df_colors = df_random[df_random["colors_used"].notnull()].copy()
        
        if not df_colors.empty:
            df_colors_best = df_colors.groupby(["case", "algorithm", "optimal_k"])["colors_used"].min().reset_index()
            
            plt.figure(figsize=(12, 6))
            sns.barplot(
                data=df_colors_best,
                x="case",
                y="colors_used",
                hue="algorithm"
            )
            plt.title("Mínimo de Colores Usados por Caso de Prueba (Grafos Aleatorios)")
            plt.xlabel("Caso de Prueba")
            plt.ylabel("Número de Colores Usados")
            plt.xticks(rotation=45, ha="right")
            plt.legend(title="Algoritmo")
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "colors_comparison_random.png"), dpi=150)
            plt.close()
            charts_generated.append(("colors_comparison_random.png", "Mínimo de Colores Usados (Grafos Aleatorios)"))

    # 4. Status Breakdown per Algorithm
    plt.figure(figsize=(8, 5))
    status_counts = pd.crosstab(df["algorithm"], df["status"])
    colors = []
    for col in status_counts.columns:
        if "Completed" in col:
            colors.append("#10b981")
        elif "Timeout" in col:
            colors.append("#ef4444")
        else:
            colors.append("#f59e0b")
            
    status_counts.plot(kind="bar", stacked=True, color=colors, ax=plt.gca())
    plt.title("Estado de Ejecución por Algoritmo")
    plt.xlabel("Algoritmo")
    plt.ylabel("Número de Ejecuciones")
    plt.legend(title="Estado")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "status_summary.png"), dpi=150)
    plt.close()
    charts_generated.append(("status_summary.png", "Estado de Ejecución por Algoritmo"))

    # Compute high level stats
    total_runs = len(df)
    completed_runs = len(df[df["status"] == "Completed"])
    timeout_runs = len(df[df["status"] == "Timeout"])
    avg_time = df["time_taken"].mean()
    
    # Generate HTML cards
    chart_cards_html = ""
    for filename, title in charts_generated:
        chart_cards_html += f"""
        <div class="chart-card">
            <h2>{title}</h2>
            <img class="chart-img" src="{filename}" alt="{title}">
        </div>
        """
        
    # Generate table rows
    table_rows_html = ""
    # Sort for display
    df_sorted = df.sort_values(by=["case", "algorithm", "repetition"])
    for _, row in df_sorted.iterrows():
        status_class = "completed" if row["status"] == "Completed" else ("timeout" if row["status"] == "Timeout" else "error")
        time_class = "time-fast" if row["time_taken"] < 0.1 else ("time-med" if row["time_taken"] < 4.0 else "time-slow")
        colors_str = int(row["colors_used"]) if pd.notnull(row["colors_used"]) else "-"
        seed_str = int(row["seed"]) if pd.notnull(row["seed"]) else "-"
        
        table_rows_html += f"""
        <tr>
            <td><strong>{row['algorithm']}</strong></td>
            <td>{row['case']}</td>
            <td>{row['num_vertices']}</td>
            <td>{row['num_edges']}</td>
            <td>{seed_str}</td>
            <td>{row['repetition']}</td>
            <td><span class="badge {time_class}">{row['time_taken']:.4f} s</span></td>
            <td>{colors_str}</td>
            <td><span class="badge {status_class}">{row['status']}</span></td>
        </tr>
        """
        
    # Write index.html
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Pruebas de Coloreado de Grafos - Pytest</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0b0f19;
            --card-bg: #151d30;
            --border-color: #222f47;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-cyan: #06b6d4;
            --accent-purple: #a855f7;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            background-color: var(--bg-color);
            color: var(--text-primary);
            font-family: 'Plus Jakarta Sans', sans-serif;
            padding: 2rem;
            line-height: 1.5;
        }}
        
        header {{
            margin-bottom: 2.5rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1.5rem;
        }}
        
        h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        
        .subtitle {{
            color: var(--text-secondary);
            font-size: 1.1rem;
        }}
        
        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }}
        
        .stat-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s, border-color 0.2s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(6, 182, 212, 0.4);
        }}
        
        .stat-title {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}
        
        .stat-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 2.2rem;
            font-weight: 700;
        }}
        
        .stat-value.completed {{ color: var(--success); }}
        .stat-value.timeout {{ color: var(--danger); }}
        .stat-value.average {{ color: var(--accent-cyan); }}
        
        /* Charts Grid */
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }}
        
        .chart-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }}
        
        .chart-card h2 {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.3rem;
            margin-bottom: 1rem;
            border-left: 4px solid var(--accent-cyan);
            padding-left: 0.75rem;
        }}
        
        .chart-img {{
            width: 100%;
            height: auto;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            background-color: #ffffff; /* Make white graphs contrast nicely with dark UI */
            padding: 5px;
        }}
        
        /* Table Section */
        .table-section {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }}
        
        .table-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        
        .table-header h2 {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
        }}
        
        .search-box {{
            background-color: var(--bg-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.6rem 1rem;
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.95rem;
            min-width: 300px;
            outline: none;
            transition: border-color 0.2s;
        }}
        
        .search-box:focus {{
            border-color: var(--accent-cyan);
        }}
        
        .table-wrapper {{
            overflow-x: auto;
            max-height: 500px;
            overflow-y: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }}
        
        th {{
            background-color: rgba(15, 23, 42, 0.95);
            color: var(--text-primary);
            font-weight: 600;
            padding: 0.8rem 1rem;
            border-bottom: 2px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        td {{
            padding: 0.8rem 1rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-secondary);
        }}
        
        tr:hover td {{
            color: var(--text-primary);
            background-color: rgba(255, 255, 255, 0.02);
        }}
        
        /* Badges */
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }}
        
        .badge.completed {{
            background-color: rgba(16, 185, 129, 0.15);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}
        
        .badge.timeout {{
            background-color: rgba(239, 68, 68, 0.15);
            color: var(--danger);
            border: 1px solid rgba(239, 68, 68, 0.3);
        }}
        
        .badge.error {{
            background-color: rgba(245, 158, 11, 0.15);
            color: var(--warning);
            border: 1px solid rgba(245, 158, 11, 0.3);
        }}
        
        .badge.time-fast {{
            background-color: rgba(16, 185, 129, 0.1);
            color: var(--success);
        }}
        
        .badge.time-med {{
            background-color: rgba(245, 158, 11, 0.1);
            color: var(--warning);
        }}
        
        .badge.time-slow {{
            background-color: rgba(239, 68, 68, 0.1);
            color: var(--danger);
        }}
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: var(--bg-color);
        }}
        ::-webkit-scrollbar-thumb {{
            background: var(--border-color);
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #334155;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Reporte de Ejecución - Pytest Graph Coloring</h1>
        <p class="subtitle">Análisis de rendimiento, colores utilizados y detección de tiempos límite (máx 5s)</p>
    </header>
    
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-title">Total de Ejecuciones</div>
            <div class="stat-value">{total_runs}</div>
        </div>
        <div class="stat-card">
            <div class="stat-title">Completadas con Éxito</div>
            <div class="stat-value completed">{completed_runs}</div>
        </div>
        <div class="stat-card">
            <div class="stat-title">Excedieron Límite (5s)</div>
            <div class="stat-value timeout">{timeout_runs}</div>
        </div>
        <div class="stat-card">
            <div class="stat-title">Tiempo de Ejecución Promedio</div>
            <div class="stat-value average">{avg_time:.4f} s</div>
        </div>
    </div>
    
    <div class="charts-grid">
        {chart_cards_html}
    </div>
    
    <div class="table-section">
        <div class="table-header">
            <h2>Detalle de todas las Pruebas</h2>
            <input type="text" id="searchInput" class="search-box" placeholder="Buscar por algoritmo, caso, estado..." onkeyup="filterTable()">
        </div>
        <div class="table-wrapper">
            <table id="resultsTable">
                <thead>
                    <tr>
                        <th onclick="sortTable(0)" style="cursor:pointer;">Algoritmo ↕</th>
                        <th onclick="sortTable(1)" style="cursor:pointer;">Caso ↕</th>
                        <th onclick="sortTable(2)" style="cursor:pointer;">Vértices ↕</th>
                        <th onclick="sortTable(3)" style="cursor:pointer;">Aristas ↕</th>
                        <th onclick="sortTable(4)" style="cursor:pointer;">Semilla ↕</th>
                        <th onclick="sortTable(5)" style="cursor:pointer;">Repetición ↕</th>
                        <th onclick="sortTable(6)" style="cursor:pointer;">Tiempo (s) ↕</th>
                        <th onclick="sortTable(7)" style="cursor:pointer;">Colores Usados ↕</th>
                        <th onclick="sortTable(8)" style="cursor:pointer;">Estado ↕</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows_html}
                </tbody>
            </table>
        </div>
    </div>
    
    <script>
        function filterTable() {{
            const input = document.getElementById("searchInput");
            const filter = input.value.toUpperCase();
            const table = document.getElementById("resultsTable");
            const tr = table.getElementsByTagName("tr");
            
            for (let i = 1; i < tr.length; i++) {{
                let match = false;
                const tds = tr[i].getElementsByTagName("td");
                for (let j = 0; j < tds.length; j++) {{
                    if (tds[j]) {{
                        const textValue = tds[j].textContent || tds[j].innerText;
                        if (textValue.toUpperCase().indexOf(filter) > -1) {{
                            match = true;
                            break;
                        }}
                    }}
                }}
                tr[i].style.display = match ? "" : "none";
            }}
        }}
        
        let sortDirections = [];
        function sortTable(n) {{
            const table = document.getElementById("resultsTable");
            let rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
            switching = true;
            dir = sortDirections[n] === "asc" ? "desc" : "asc";
            sortDirections[n] = dir;
            
            while (switching) {{
                switching = false;
                rows = table.rows;
                for (i = 1; i < (rows.length - 1); i++) {{
                    shouldSwitch = false;
                    x = rows[i].getElementsByTagName("TD")[n];
                    y = rows[i + 1].getElementsByTagName("TD")[n];
                    
                    let xVal = x.textContent || x.innerText;
                    let yVal = y.textContent || y.innerText;
                    
                    // Try parsing as number
                    let xNum = parseFloat(xVal);
                    let yNum = parseFloat(yVal);
                    
                    if (!isNaN(xNum) && !isNaN(yNum)) {{
                        if (dir == "asc") {{
                            if (xNum > yNum) {{
                                shouldSwitch = true;
                                break;
                            }}
                        }} else if (dir == "desc") {{
                            if (xNum < yNum) {{
                                shouldSwitch = true;
                                break;
                            }}
                        }}
                    }} else {{
                        if (dir == "asc") {{
                            if (xVal.toLowerCase() > yVal.toLowerCase()) {{
                                shouldSwitch = true;
                                break;
                            }}
                        }} else if (dir == "desc") {{
                            if (xVal.toLowerCase() < yVal.toLowerCase()) {{
                                shouldSwitch = true;
                                break;
                            }}
                        }}
                    }}
                }}
                if (shouldSwitch) {{
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    switching = true;
                    switchcount++;
                }} else {{
                    if (switchcount == 0 && dir == "asc") {{
                        dir = "desc";
                        sortDirections[n] = dir;
                        switching = true;
                    }}
                }}
            }}
        }}
    </script>
</body>
</html>
"""
    
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Generated HTML report and charts at {output_dir}/")

if __name__ == "__main__":
    generate_reports_and_charts()
