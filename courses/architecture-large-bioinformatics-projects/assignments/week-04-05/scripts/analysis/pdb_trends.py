import argparse
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path
from pdb_utils import process_pdb_data

def create_pie_chart(df, mapping, output_path):
    """Generates a static pie chart for total PDB method shares."""
    data = {}
    for cat, methods in mapping.items():
        mask = df['method'].apply(lambda x: any(m in x for m in methods))
        data[cat] = df[mask]['value'].sum()
    
    plt.figure(figsize=(10, 8))
    plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=140)
    plt.title(r'PDB Methods Share $\sum(n \cdot 1/r)$')
    plt.savefig(output_path)
    plt.close()

def create_interactive_plotly(df, mapping, out_dir):
    """Generates an interactive bar chart race using Plotly."""
    def map_cat(m):
        for cat, methods in mapping.items():
            if any(met in m for met in methods): return cat
        return "OTHER"

    df['category'] = df['method'].apply(map_cat)
    # Filter years and relevant categories
    df_f = df[(df['year'] >= 2005) & (df['year'] <= 2025) & (df['category'] != "OTHER")]
    
    # Calculate cumulative values per year
    pivot = df_f.groupby(['year', 'category'])['value'].sum().unstack(fill_value=0).cumsum()
    
    # Calculate percentages for the hover data
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100
    
    # Reset index for melting
    pivot = pivot.reset_index()
    pivot_pct = pivot_pct.reset_index()
    
    # Melt both to long format
    df_long = pivot.melt(id_vars=['year'], value_name='Cumulative Value', var_name='Method')
    df_pct = pivot_pct.melt(id_vars=['year'], value_name='Percentage', var_name='Method')
    
    # Merge to have both Value and Percentage in one DataFrame
    df_final = df_long.merge(df_pct, on=['year', 'Method'])
    
    fig_abs = px.bar(
        df_final, 
        x="Cumulative Value", 
        y="Method", 
        color="Method", 
        animation_frame="year", 
        animation_group="Method",
        title=fr"PDB Growth (Absolute $\sum(n \cdot 1/r)$) [2005-2025]",
        hover_data={"Percentage": ":.2f", "Cumulative Value": ":.2f"},
        range_x=[0, df_final['Cumulative Value'].max() * 1.1]
    )
    
    fig_abs.write_html(str(out_dir / "pdb_trends_interactive.html"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        conf = yaml.safe_load(f)

    data_dir = conf['paths']['data_pdb']
    plot_dir = Path(conf['paths']['plots'])
    mapping = conf['params']['pdb_class_mapping']

    # Ensure output directory exists
    plot_dir.mkdir(parents=True, exist_ok=True)

    df_pdb = process_pdb_data(data_dir)
    create_pie_chart(df_pdb, mapping, plot_dir / "pdb_pie_chart.png")
    create_interactive_plotly(df_pdb, mapping, plot_dir)