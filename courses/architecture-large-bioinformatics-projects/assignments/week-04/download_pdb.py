import os
import requests
import argparse

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
    parser = argparse.ArgumentParser(description="Download PDB derived data for lab exercises.")
    # parser.add_argument("--URLs", nargs='+', help="URLs with entries files ")
    parser.add_argument("--out", type=str, default="data/pdb", help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    # URLs for Exercise 1 (Metadata) and Exercise 2b (Sequences)
    urls = [
        "https://files.rcsb.org/pub/pdb/derived_data/index/entries.idx", # IDs, Methods, Dates, Resolution
        "https://files.rcsb.org/pub/pdb/derived_data/pdb_entry_type.txt", # To filter 'protein' only entries
        "https://files.rcsb.org/pub/pdb/derived_data/pdb_seqres.txt.gz"   # Sequences for length/AA content
    ]

    for url in urls:
        try:
            download_file(url, args.out)
        except Exception as e:
            print(f"Failed to download {url}: {e}")

if __name__ == "__main__":
    main()