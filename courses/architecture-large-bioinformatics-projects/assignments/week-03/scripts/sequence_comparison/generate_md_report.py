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


def load_and_concat(method_list, file_dict):
    """
    Helper method for iterating through `file_dict` with method list condition
    """
    dfs = []
    for method in method_list:
        if method in file_dict:
            #TODO different methods would need special loading !!!
            if method == 'tmalign':
                df = tmalign_loader(file_dict[method])
            else:
                df = pd.read_csv(file_dict[method])
            
            # method column is included - we not need to add it
            dfs.append(df)
        else:
            print("[GENERATE REPORT]: No file for {method}")
        
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
                    yield header, "".join(seq)
                header = line
                seq = []
            else:
                seq.append(line)
        if header:
            yield header, "".join(seq)

# --- analysis ---

def tmalign_loader(path: Path | str):
    '''
    Function for loading output from tmalign to make it comparable
    '''
    df = pd.read_csv(path)
    df_out = pd.DataFrame(
        # query, and target 
        df['query'],
        df['target'],
        # TM = max(TM1, TM2) - we can obtain homologous on certain part
        df[['TM1', 'TM2']].max(axis=1),
        # evalue - we can not provide it (what is probability of obtaining this sequence at random - we compare here two structure)
        pd.Series(np.zeros(len(df), dtype=float), name='evalue'),
        # method - pass
        df['method'],
        columns=['query', 'target', 'tmscore', 'evalue', 'method']
    )
    return df_out
 




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
    meta_dict = {}
    for f in meta_files:
        method_name = os.path.basename(f).split('_')[0]
        meta_dict[method_name] = f

    output_dict = {}
    for f in result_files:
        method_name = os.path.basename(f).split('_')[0]
        output_dict[method_name] = f
    
    ## Combine dfs (all files)
    ### metadata
    df_meta = load_and_concat(methods, meta_dict) 
    ### sequence
    df_sequnece = load_and_concat(seq_methods, output_dict)
    ### structure 
    df_structure = load_and_concat(struct_methods, output_dict)
    ### fasta files information:
    fasta_queries = pd.DataFrame(
        [head for head, sequence in parse_fasta(args.fasta_sequences_file)],
        columns=['query']
    ) 

    # TODO tylko te analizy są do zrobienia - trzeba będzie to zostawić

    # --- Start writing the Markdown file ---
    ## create output dir
    os.makedirs(os.path.dirname(args.out_report), exist_ok=True)
    
    with open(args.out_report, 'w') as f:
        # --- Header section ---
        f.write(f"# Structure report of {args.experiment} - {args.probe}\n\n")
        f.write(f"Report contains comparison of {args.experiment} - {args.probe} using: \n**Structural methods**: {', '.join(struct_methods)} \n**Sequence methods**: {', '.join(seq_methods)}\n\n")
        
        # --- Metadata section ---
        f.write("## Metadata\n\n")
        
        # --- Joined results section --- 
        f.write("## Joined results\n\n")
        f.write("This table summarizes the performance and hit count across all executed methods:\n\n")
        if not df_meta.empty:
            f.write(df_meta.to_markdown(index=False))
            f.write("\n\n")
        else:
            f.write("*No metadata found.*\n\n")
        
        ## --- Comparison between sequential and structural analysis ---

        # TODO - czy to jest jeszcze potrzebne 
        # --- Single method results section ---
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