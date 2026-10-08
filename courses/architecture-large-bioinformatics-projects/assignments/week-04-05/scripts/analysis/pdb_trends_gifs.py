import argparse
import yaml
import matplotlib.pyplot as plt
import bar_chart_race as bcr
from pathlib import Path
from pdb_utils import patch_pandas_fillna, process_pdb_data

# Apply pandas patch before any processing
patch_pandas_fillna()

def create_pie_chart(df, mapping, output_path):
    """Generates a static pie chart for PDB method shares."""
    data = {}
    for cat, methods in mapping.items():
        mask = df['method'].apply(lambda x: any(m in x for m in methods))
        data[cat] = df[mask]['value'].sum()
    
    plt.figure(figsize=(10, 8))
    plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=140)
    plt.title(r'PDB Methods Share $\sum(n \cdot 1/r)$')
    plt.savefig(output_path)
    plt.close()

def create_animations(df, mapping, out_dir):
    """Generates animated bar chart race GIFs."""
    def map_cat(m):
        for cat, methods in mapping.items():
            if any(met in m for met in methods): return cat
        return "OTHER"

    df['category'] = df['method'].apply(map_cat)
    df_f = df[(df['year'] >= 2005) & (df['year'] <= 2025) & (df['category'] != "OTHER")]
    
    pivot = df_f.groupby(['year', 'category'])['value'].sum().unstack(fill_value=0).cumsum()
    
    # Absolute values GIF
    #TODO change path -> str 
    bcr.bar_chart_race(df=pivot, filename=str(out_dir / "pdb_trends_absolute.gif"), 
                       title=r'PDB Growth (Absolute $\sum(n \cdot 1/r)$)', n_bars=3)
    
    # Percentage values GIF
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100
    bcr.bar_chart_race(df=pivot_pct, filename=str(out_dir / "pdb_trends_percentage.gif"), 
                       title='PDB Methods % Share (2005-2025)', n_bars=3)

def generate_report_snippet():
    """Returns a markdown string for the report."""
    return """
## PDB Trends Analysis
The following charts represent the growth and distribution of structural determination methods 
in the PDB, weighted by sequence length and resolution ($\sum n \cdot 1/r$).

![PDB Method Share](results/plots/pdb_pie_chart.png)
![Absolute Growth](results/plots/pdb_trends_absolute.gif)
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        conf = yaml.safe_load(f)

    data_dir = conf['paths']['data_pdb']
    plot_dir = Path(conf['paths']['plots'])
    mapping = conf['params']['pdb_class_mapping']

    df = process_pdb_data(data_dir)
    
    # create_pie_chart(df, mapping, plot_dir / "pdb_pie_chart.png")
    create_animations(df, mapping, plot_dir)
    
    # Print snippet for create_md_report.py or manual insertion
    print("--- REPORT SNIPPET GENERATED ---")
    print(generate_report_snippet())