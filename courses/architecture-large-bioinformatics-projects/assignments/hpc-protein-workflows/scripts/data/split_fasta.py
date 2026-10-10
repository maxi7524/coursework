import argparse
import os
import random
import glob

def get_sequence_count(file_path):
    """Counts the number of sequences in a FASTA file."""
    count = 0
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith(">"): count += 1
    return count

def split_and_sample(input_path, base_output_dir, n_test, n_per_file):
    """Splits a single FASTA file into a test set and multiple parts."""
    # Extract sample name and create a specific subdirectory for it
    sample_name = os.path.basename(input_path).replace("_flat.fasta", "").replace(".fasta", "").replace(".fa", "")
    sample_output_dir = os.path.join(base_output_dir, sample_name)
    os.makedirs(sample_output_dir, exist_ok=True)

    total_seqs = get_sequence_count(input_path)
    print(f"Processing '{sample_name}': {total_seqs} sequences found.")

    # Randomly sampling indices for the test set
    ## If n_test is None it takes by default: $total_seqs \mod n_per_file$
    if n_test is None:
        n_test = total_seqs % n_per_file

    test_indices = set(random.sample(range(total_seqs), min(n_test, total_seqs)))
    
    test_path = os.path.join(sample_output_dir, f"{sample_name}_test.fasta")
    
    current_chunk_idx = 0
    current_chunk_count = 0
    current_chunk_file = None
    
    with open(input_path, 'r') as f_in, open(test_path, 'w') as f_test:
        # Iterate through all samples in files
        seq_idx = 0
        while True:
            header = f_in.readline()
            seq = f_in.readline()
            if not header or not seq: break
            
            ## If sample indice is in test set indces write to it
            if seq_idx in test_indices:
                f_test.write(header + seq)
            ## If indice is not int test set, add to to other probe 
            else:
                ### Opening a new part file if the current one is full
                if current_chunk_file is None or current_chunk_count >= n_per_file:
                    if current_chunk_file: current_chunk_file.close()
                    
                    chunk_name = f"{sample_name}_part_{current_chunk_idx}.fasta"
                    current_chunk_file = open(os.path.join(sample_output_dir, chunk_name), 'w')
                    current_chunk_idx += 1
                    current_chunk_count = 0
                
                current_chunk_file.write(header + seq)
                current_chunk_count += 1
            
            seq_idx += 1
            
    if current_chunk_file: current_chunk_file.close()
    print(f"Finished '{sample_name}': Created {current_chunk_idx} parts + test set in {sample_output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split multiple FASTA files into parts with random test set sampling.")
    parser.add_argument("-i", "--input", nargs='+', required=True, help="Input FASTA file(s) or pattern (e.g. data/*.fasta)")
    parser.add_argument("-d", "--dir", required=True, help="Base directory for splits")
    parser.add_argument("--test_n", type=int, default=None, help="Number of sequences for testing per file")
    parser.add_argument("--split_n", type=int, default=1000, help="Number of sequences per part file")
    
    args = parser.parse_args()

    # Expand wildcards and collect all valid files
    input_files = []
    for pattern in args.input:
        input_files.extend(glob.glob(pattern))

    if not input_files:
        print("Error: No input files found.")
    else:
        for file_path in input_files:
            if os.path.isfile(file_path):
                split_and_sample(file_path, args.dir, args.test_n, args.split_n)