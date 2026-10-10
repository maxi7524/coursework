#!/bin/bash
# download_data.sh - download and basic check of proteomes



# params
## out dir file 
OUT_DIR="data/raw"
mkdir -p "$OUT_DIR"

## names for files
declare -A names
names["UP000000625_83333.fasta.gz"]="E_coli.fasta"
names["UP000005640_9606.fasta.gz"]="H_sapiens.fasta"
names["uniprot_sprot.fasta.gz"]="SwissProt.fasta"

## urls for databases files
urls=(
    "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Bacteria/UP000000625/UP000000625_83333.fasta.gz"
    "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/UP000005640/UP000005640_9606.fasta.gz"
    "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz"
)

## main download loop
for url in "${urls[@]}"; do
    raw_name=$(basename "$url")
    target_name=${names[$raw_name]}

    echo "Downloading: $raw_name as $target_name..."
    wget -q -N "$url" -P $OUT_DIR
    
    # Decompress and count sequences and rename sequences
    gunzip -c "$OUT_DIR/$raw_name" > "$OUT_DIR/$target_name"
    seq_count=$(grep -c ">" "$OUT_DIR/$target_name")
    echo "Done: $target_name contains $seq_count sequences."
    # remove unpacked sequences 
    rm "$OUT_DIR/$raw_name"
done


