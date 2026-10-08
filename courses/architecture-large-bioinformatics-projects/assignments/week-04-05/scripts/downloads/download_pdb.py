import os
import requests
import argparse
import gzip
import shutil
from pathlib import Path

# --- Lab 4, Ex 1 & Lab 5, Ex 3b: PDB Data Download ---

def download_file(url, folder):
    """Downloads a file from a URL to a specific folder."""
    local_filename = os.path.join(folder, url.split('/')[-1])
    print(f"Downloading {url}...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Saved to {local_filename}")
    return local_filename

def main():
    parser = argparse.ArgumentParser(description="Download PDB derived data.")
    parser.add_argument("--out", type=str, default="data/pdb", help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    urls = [
        "https://files.rcsb.org/pub/pdb/derived_data/index/entries.idx",    # IDs, Methods, Dates, Resolution
        "https://files.rcsb.org/pub/pdb/derived_data/pdb_entry_type.txt",   # To filter 'protein' only entries
        "https://files.rcsb.org/pub/pdb/derived_data/pdb_seqres.txt.gz"     # Sequences for length/AA content
    ]

    for url in urls:
        downloaded_file = download_file(url, args.out)
        
        # Automatically extract .gz files so downstream analysis just reads text
        if downloaded_file.endswith(".gz"):
            extracted_file = downloaded_file[:-3]
            print(f"Extracting {downloaded_file} to {extracted_file}...")
            with gzip.open(downloaded_file, 'rb') as f_in:
                with open(extracted_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(downloaded_file) # Clean up the .gz file

if __name__ == "__main__":
    main()