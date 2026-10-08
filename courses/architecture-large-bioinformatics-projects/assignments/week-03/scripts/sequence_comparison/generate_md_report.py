import argparse
import pandas as pd
import numpy as np
import os
import glob
from pathlib import Path

# debug version 


## running parser in interactive 
# mock_args = [
#     "--experiment", "synthethic_bacterium",
#     "--probe", "CP014940.1",
#     "--methods_sequence", "blast",
#     "--methods_structure", "reseek",
#     "--results_dir" , "results/synthethic_bacterium/report/CP014940.1/",
#     "--out_report", "reports/synthethic_bacterium/CP014940.1_report.md"
# ]

# import sys
# sys.argv = ['random_skrypt.py'] +  mock_args
# args = parse_args()

# --- helpers --- #


def load_and_concat(method_list, file_dict, is_meta=False):
    """
    Helper method for iterating through `file_dict` with method list condition
    """
    dfs = []
    for method in method_list:
        if method in file_dict:
            #TODO different methods would need special loading !!!
            if method == 'tmalign' and not is_meta:
                df = tmalign_loader(file_dict[method])
            
            else:
                df = pd.read_csv(file_dict[method])
            # If method is not present add it 
            if 'method' not in df.columns: 
                df['method'] = method

            if not is_meta:
                #  problem with loader (i mispelled _ -> . somewhere)
                df = clean_identifiers(df)
                # give score to every column s results are comperable
                if 'bitscore' in df.columns and 'score' not in df.columns:
                    df['score'] = df['bitscore']
                elif 'tmscore' in df.columns and 'score' not in df.columns:
                    df['score'] = df['tmscore']
                elif 'score' not in df.columns:
                    df['score'] = np.nan
                if  method in ['reseek', 'foldseek', 'blast']: # alphabet methods
                    # drop low quality findings 
                    df['evalue'] = pd.to_numeric(df['evalue'], errors='coerce')
                    df = df[df['evalue'] < 1e-2]
            
            # append list 
            dfs.append(df)
                
        else:
            print("[GENERATE REPORT]: No file for method: {method}")
        
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def parse_fasta(file_path: Path | str):
    file_path = Path(file_path)
    header = ""
    seq = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header:
                    yield header.replace('>', '').split()[0], "".join(seq)
                header = line
                seq = []
            else:
                seq.append(line)
        if header:
            yield header.replace('>', '').split()[0], "".join(seq)

# --- analysis ---

def tmalign_loader(path: Path | str):
    '''
    Function for loading output from tmalign to make it comparable
    '''
    df = pd.read_csv(path)
    df_out = pd.DataFrame({
        # query, and target 
        'query': df['query'],
        'target': df['target'],
        # TM = max(TM1, TM2) - we can obtain homologous on certain part
        'score': df[['TM1', 'TM2']].max(axis=1),
        # evalue - we can not provide it (what is probability of obtaining this sequence at random - we compare here two structure)
        'evalue': pd.Series(np.zeros(len(df), dtype=float), name='evalue'),
        # method - pass
        'method': df['method']
    })
    return df_out

def clean_identifiers(df):
    """
    Cleans IDs by removing '.pdb' extensions, '_esmfold...' suffixes, 
    and specific prefixes (handling both '_' and '.') so IDs match perfectly.
    """
    for col in ['query', 'target']:
        if col in df.columns:
            df[col] = df[col].astype(str)
            # Usuwa rozszerzenie pliku
            df[col] = df[col].str.replace(r'\.pdb$', '', regex=True)
            # Usuwa sufiksy z modeli ESMFold
            df[col] = df[col].str.replace(r'_esmfold_v.*', '', regex=True)
            # remove pre fixes
            df[col] = df[col].str.replace(r'^M[._]genitalium-', '', regex=True)
    return df
 
# --- Markdown Generators --- #

def generate_header_section(experiment, probe, struct_methods, seq_methods):
    md = f"# Structure vs Sequence Report: {experiment} - {probe}\n\n"
    md += f"This report compares the detection capabilities of:\n"
    md += f"* **Sequence methods**: {', '.join(seq_methods)}\n"
    md += f"* **Structural methods**: {', '.join(struct_methods)}\n\n"
    return md

def generate_metadata_section(df_meta):
    md = "## 1. Metadata analysis\n\n"
    md += "This table summarizes the performance, runtime, and total hit count across all executed methods:\n\n"
    if not df_meta.empty:
        md += df_meta.to_markdown(index=False) + "\n\n"
    else:
        md += "*No metadata found.*\n\n"
    return md

def generate_comparison_section(df_seq, df_struct, struct_methods, seq_methods):
    md = "## 2. Sequential vs Structure comparison\n\n"
    
    seq_queries = set(df_seq['query'].unique()) if not df_seq.empty else set()
    
    stats = []
    for method in struct_methods:
        if not df_struct.empty and method in df_struct['method'].values:
            df_m = df_struct[df_struct['method'] == method]
            df_m = df_m[df_m['score'] > 0.5]
            struct_queries = set(df_m['query'].unique())
            
            fp = seq_queries - struct_queries
            fn = struct_queries - seq_queries
            both = seq_queries.intersection(struct_queries)
            
            stats.append({
                "Structural Method": method,
                "Found by Both": len(both),
                "False Positives (Seq only)": len(fp),
                "False Negatives (Struct only)": len(fn)
            })
            
    if stats:
        md += pd.DataFrame(stats).to_markdown(index=False) + "\n\n"
    else:
        md += "*Not enough data to compute cross-method statistics.*\n\n"
        
    # --- False Negatives Sub-section ---
    md += "### False Negatives (Top 10 by score)\n\n"
    seq_methods_str = ', '.join(seq_methods).upper()
    md += f"False negatives represent sequences missed by sequential analysis ({seq_methods_str}) but successfully mapped by structural methods. They highlight distant homologs with conserved 3D folds.\n\n"
    
    found_any_fn = False
    for method in struct_methods:
        if not df_struct.empty and method in df_struct['method'].values:
            df_m = df_struct[df_struct['method'] == method]
            struct_queries = set(df_m['query'].unique())
            fn_queries = struct_queries - seq_queries
            
            if fn_queries:
                found_any_fn = True
                md += f"#### Method: {method.upper()}\n\n"
                
                # Filter structural dataframe to only include FN queries
                df_fn = df_m[df_m['query'].isin(fn_queries)].copy()
                
                # Get the best hit for each query (in case of multiple targets)
                df_fn_score = df_fn[df_fn['score'].notna()]
                idx = df_fn_score.groupby('query')['score'].idxmax()
                df_fn_best = df_fn_score.loc[idx]
                
                # Sort descending by score and take top 10
                df_top10 = df_fn_best.sort_values(by='score', ascending=False).head(10)
                
                # Clean up columns for presentation
                cols_to_show = ['query', 'target', 'score']
                if 'evalue' in df_top10.columns and not df_top10['evalue'].isna().all():
                    cols_to_show.append('evalue')
                    
                md += df_top10[cols_to_show].to_markdown(index=False) + "\n\n"
                
    if not found_any_fn:
        md += "*No structural false negatives found. Sequential methods detected all structural hits.*\n\n"

    return md

# --- main functions ---

def parse_args(args_in=None):
    parser = argparse.ArgumentParser(description="Generate Markdown report from method results.")
    parser.add_argument("--experiment", required=True, help="Name of the experiment")
    parser.add_argument("--probe", required=True, help="Name of the probe/fasta file")
    parser.add_argument("--fasta_sequences_file", required=True, help="Path to file containing FASTA sequences")
    parser.add_argument("--methods_sequence", required=True, help="Comma-separated list of sequence methods to include in the report")
    parser.add_argument("--methods_structure", required=True, help="Comma-separated list of structure methods to include in the report")
    parser.add_argument("--results_dir", required=True, help="Directory containing CSV outputs")
    parser.add_argument("--out_report", required=True, help="Path to save the Markdown report")
    return parser.parse_args()


def generate_report():
    print("[GENERATE REPORT]: Starting ...")

    # params
    args = parse_args()
    ## load lists
    seq_methods = args.methods_sequence.split(',') 
    struct_methods = args.methods_structure.split(',') 
    methods = seq_methods + struct_methods


    # --- Collect all CSV files into dfs ---
    ## find ALL files in data folder 
    meta_files = glob.glob(os.path.join(args.results_dir, "*_metadata.csv"))
    result_files = glob.glob(os.path.join(args.results_dir, "*_output.csv"))
    
    ## create dicts {method_name: file_path}
    meta_dict = {os.path.basename(f).split('_')[0]: f for f in meta_files}

    output_dict = {os.path.basename(f).split('_')[0]: f for f in result_files}
    
    ## Combine dfs (all files)
    ### metadata
    df_meta = load_and_concat(methods, meta_dict, is_meta=True) 
    ### sequence
    df_sequnece = load_and_concat(seq_methods, output_dict)
    ### structure 
    df_structure = load_and_concat(struct_methods, output_dict)
    # TODO OBSOLETE IDEA - but left for additonal functionality, (base with all input sequences, you can take them also from targets of any methods ?? )
    # ### fasta files information:
    # fasta_queries = pd.DataFrame(
    #     [head for head, sequence in parse_fasta(args.fasta_sequences_file)],
    #     columns=['query']
    # ) 

    # --- Generate markdown ---
    report_content = []
    ## single sections
    report_content.append(generate_header_section(args.experiment, args.probe, struct_methods, seq_methods))
    report_content.append(generate_metadata_section(df_meta))
    report_content.append(generate_comparison_section(df_sequnece, df_structure, struct_methods, seq_methods))

    ## Combine all sections
    final_markdown = "".join(report_content)

    ## Write md to file
    os.makedirs(os.path.dirname(args.out_report), exist_ok=True)
    with open(args.out_report, 'w', encoding='utf-8') as f:
        f.write(final_markdown)

    # # --- Start writing the Markdown file ---
    # ## create output dir
    # os.makedirs(os.path.dirname(args.out_report), exist_ok=True)
    
    # with open(args.out_report, 'w') as f:
    #     # --- Header section ---
    #     f.write(f"# Structure report of {args.experiment} - {args.probe}\n\n")
    #     f.write(f"Report contains comparison of {args.experiment} - {args.probe} using: \n**Structural methods**: {', '.join(struct_methods)} \n**Sequence methods**: {', '.join(seq_methods)}\n\n")
        
    #     # --- Metadata section ---
    #     f.write("## Metadata\n\n")
        
    #     # --- Joined results section --- 
    #     f.write("## Joined results\n\n")
    #     f.write("This table summarizes the performance and hit count across all executed methods:\n\n")
    #     if not df_meta.empty:
    #         f.write(df_meta.to_markdown(index=False))
    #         f.write("\n\n")
    #     else:
    #         f.write("*No metadata found.*\n\n")
        
    #     ## --- Comparison between sequential and structural analysis ---

    #     # TODO - czy to jest jeszcze potrzebne 
    #     # --- Single method results section ---
    #     f.write("## Single method results\n\n")
        
    #     for res_file in result_files:
    #         # Extract method name from filename (e.g., 'blast_output.csv' -> 'blast')
    #         method_name = os.path.basename(res_file).replace('_output.csv', '').upper()
            
    #         f.write(f"### {method_name}\n\n")
            
    #         df = pd.read_csv(res_file)
    #         if not df.empty:
    #             # We drop the 'method' column here since it's redundant in the specific section
    #             if 'method' in df.columns:
    #                 df = df.drop(columns=['method'])
    #             f.write(df.to_markdown(index=False))
    #             f.write("\n\n")
    #         else:
    #             f.write("*No reliable hits found for this method.*\n\n")
                
    print(f"Report generated successfully at: {args.out_report}")

if __name__ == "__main__":
    generate_report()