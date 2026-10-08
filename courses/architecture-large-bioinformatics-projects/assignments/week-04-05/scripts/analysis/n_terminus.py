import argparse
import pandas as pd
from collections import Counter
import ast

# --- Lab 4, Ex 3: N-Terminus Case ---

def parse_fasta_n_term(fasta_file):
    """Extracts the first amino acid of each sequence in a FASTA file."""
    n_terms = []
    with open(fasta_file, 'r') as f:
        seq = ""
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq:
                    n_terms.append(seq[0]) # Get the very first AA
                seq = ""
            else:
                seq += line
        if seq:
            n_terms.append(seq[0])
    return n_terms

def main():
    parser = argparse.ArgumentParser()
    # Accept multiple input files as a string list, eval it to python list
    parser.add_argument("--input", required=True, type=str, help="List of fasta files")
    parser.add_argument("--output", required=True, type=str, help="Output CSV path")
    args = parser.parse_args()

    # Convert string representation of list to actual list
    fasta_files = ast.literal_eval(args.input) if '[' in args.input else args.input.split()

    all_n_terms = []
    for fasta in fasta_files:
        all_n_terms.extend(parse_fasta_n_term(fasta))
    
    counts = Counter(all_n_terms)
    
    df = pd.DataFrame(counts.items(), columns=["AminoAcid", "Count"])
    df = df.sort_values(by="Count", ascending=False)
    
    df.to_csv(args.output, index=False)
    print(f"Saved N-terminus stats to {args.output}")

if __name__ == "__main__":
    main()