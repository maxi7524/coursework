import os
import requests
import argparse
import random

# --- Lab 5, Ex 3a & 3c: UniProt Data Download ---

# Mapping simplified names to UniProt taxonomy queries
SPECIES_QUERY_MAP = {
    "E_coli": 'organism_name:"Escherichia coli"',
    "Human": 'organism_name:"Homo sapiens"',
    "Yeast": 'organism_name:"Saccharomyces cerevisiae"',
    "A_thaliana": 'organism_name:"Arabidopsis thaliana"',
    "D_melanogaster": 'organism_name:"Drosophila melanogaster"',
    "C_elegans": 'organism_name:"Caenorhabditis elegans"',
    "Mouse": 'organism_name:"Mus musculus"',
    "Zebrafish": 'organism_name:"Danio rerio"',
    "B_subtilis": 'organism_name:"Bacillus subtilis"'
}

def fetch_uniprot_fasta(query, limit=None):
    """Fetches FASTA sequences from UniProtKB based on a query."""
    # Base URL for UniProt REST API (stream format for bulk download)
    url = f"https://rest.uniprot.org/uniprotkb/stream?format=fasta&query=({query}) AND (reviewed:true)"
    
    print(f"Fetching from UniProt: {query}")
    response = requests.get(url)
    response.raise_for_status()
    
    fasta_data = response.text
    
    if limit:
        # Split by '>' to separate sequences, filter out empty strings, and sample
        sequences = [">" + seq for seq in fasta_data.split(">")[1:]]
        if len(sequences) > limit:
            sequences = random.sample(sequences, limit)
        fasta_data = "".join(sequences)
        
    return fasta_data

def main():
    parser = argparse.ArgumentParser(description="Download UniProt FASTA data.")
    parser.add_argument("--species", type=str, help="Specific species name to download")
    parser.add_argument("--kingdom", type=str, help="Kingdom name for random sampling")
    parser.add_argument("--limit", type=int, default=100, help="Number of random sequences")
    parser.add_argument("--out", type=str, required=True, help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    if args.species:
        query = SPECIES_QUERY_MAP.get(args.species)
        if not query:
            raise ValueError(f"Species {args.species} not configured in mapping.")
        fasta = fetch_uniprot_fasta(query)
        out_path = os.path.join(args.out, f"{args.species}.fasta")
        
    elif args.kingdom:
        # e.g., taxonomy_name:"Bacteria"
        query = f'taxonomy_name:"{args.kingdom}"'
        fasta = fetch_uniprot_fasta(query, limit=args.limit)
        out_path = os.path.join(args.out, f"{args.kingdom}.fasta")
    
    else:
        raise ValueError("Must provide either --species or --kingdom")

    with open(out_path, "w") as f:
        f.write(fasta)
    print(f"Saved FASTA to {out_path}")

if __name__ == "__main__":
    main()