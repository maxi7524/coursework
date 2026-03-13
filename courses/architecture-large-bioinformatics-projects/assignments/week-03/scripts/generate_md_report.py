import argparse
import pandas as pd
import os
import glob

def parse_args():
    parser = argparse.ArgumentParser(description="Generate Markdown report from method results.")
    parser.add_argument("--experiment", required=True, help="Name of the experiment")
    parser.add_argument("--probe", required=True, help="Name of the probe/fasta file")
    parser.add_argument("--results_dir", required=True, help="Directory containing CSV outputs")
    parser.add_argument("--out_report", required=True, help="Path to save the Markdown report")
    return parser.parse_args()

def generate_report():
    args = parse_args()
    
    # 1. Collect all CSV files
    meta_files = glob.glob(os.path.join(args.results_dir, "*_metadata.csv"))
    result_files = glob.glob(os.path.join(args.results_dir, "*_output.csv"))
    
    # 2. Combine metadata
    meta_dfs = [pd.read_csv(f) for f in meta_files]
    if meta_dfs:
        joined_meta = pd.concat(meta_dfs, ignore_index=True)
    else:
        joined_meta = pd.DataFrame()

    methods_used = joined_meta['method'].tolist() if not joined_meta.empty else []
    methods_str = ", ".join(methods_used)

    # 3. Start writing the Markdown file
    os.makedirs(os.path.dirname(args.out_report), exist_ok=True)
    
    with open(args.out_report, 'w') as f:
        # Header section
        f.write(f"# Structure report of {args.experiment} - {args.probe}\n\n")
        f.write(f"Report contains comparison of {args.experiment} - {args.probe} using: **{methods_str}**.\n\n")
        
        # Joined results section
        f.write("## Joined results\n\n")
        f.write("This table summarizes the performance and hit count across all executed methods:\n\n")
        if not joined_meta.empty:
            f.write(joined_meta.to_markdown(index=False))
            f.write("\n\n")
        else:
            f.write("*No metadata found.*\n\n")
            
        # Single method results section
        f.write("## Single method results\n\n")
        
        for res_file in result_files:
            # Extract method name from filename (e.g., 'blast_output.csv' -> 'blast')
            method_name = os.path.basename(res_file).replace('_output.csv', '').upper()
            
            f.write(f"### {method_name}\n\n")
            
            df = pd.read_csv(res_file)
            if not df.empty:
                # We drop the 'method' column here since it's redundant in the specific section
                if 'method' in df.columns:
                    df = df.drop(columns=['method'])
                f.write(df.to_markdown(index=False))
                f.write("\n\n")
            else:
                f.write("*No reliable hits found for this method.*\n\n")
                
    print(f"Report generated successfully at: {args.out_report}")

if __name__ == "__main__":
    generate_report()