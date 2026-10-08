import argparse
import csv
import sys
import os 
from collections import Counter
from prettytable import PrettyTable

def calculate_stats(counts, label):
    """Calculates percentages and GC content based on nucleotide counts."""
    

    # Absolute numbers
    g = counts.get('G', 0)
    c = counts.get('C', 0)
    a = counts.get('A', 0)
    t = counts.get('T', 0)
    n = counts.get('N', 0)

    total_len = g + c + a + t + n
    if total_len == 0:
        return {
            'id': label, 'gc_perc': 0, 'G': 0, 'C': 0, 'T': 0, 'A': 0, 'N': 0,
            'G_perc': 0, 'C_perc': 0, 'T_perc': 0, 'A_perc': 0, 'N_perc': 0, 'len': 0
        }

    # GC content: (G+C) / (G+C+A+T) * 100
    gc_denom = (g + c + a + t)
    gc_percent = round((g + c) / gc_denom * 100, 2) if gc_denom > 0 else 0

    # Frequencies
    g_freq = round(g / total_len * 100, 2)
    c_freq = round(c / total_len * 100, 2)
    a_freq = round(a / total_len * 100, 2)
    t_freq = round(t / total_len * 100, 2)
    n_freq = round(n / total_len * 100, 2)

    return {
        'id': label,
        'gc_perc': gc_percent,
        'G': g, 'C': c, 'T': t, 'A': a, 'N': n,
        'G_perc': g_freq, 'C_perc': c_freq, 'T_perc': t_freq, 'A_perc': a_freq, 'N_perc': n_freq,
        'len': total_len
    }

def main():
    parser = argparse.ArgumentParser(description="FASTA Genome Statistics Analyzer.")
    parser.add_argument("genome_file", help="Path to the genome file (FASTA)")
    parser.add_argument("output_csv", help="Path to the output CSV file")
    args = parser.parse_args()

    # absolute paths
    input_path = os.path.abspath(args.genome_file)
    output_path = os.path.abspath(args.output_csv)


    # creating output dir
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    results = []
    global_counts = Counter()
    current_chr_counts = Counter()
    current_chr_id = None

    headers = ["chr_id/total", "GC%", "G", "C", "T", "A", "N", "G%", "C%", "T%", "A%", "N%", "len"]

    try:
        with open(input_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.lstrip()
                if not line:
                    continue

                if line.startswith(">"):
                    # If not the first chromosome, save previous chromosome stats
                    if current_chr_id is not None:
                        stats = calculate_stats(current_chr_counts, current_chr_id)
                        results.append(stats)
                    
                    # Reset for new chromosome
                    current_chr_id = line[1:].split()[0]  # Get ID (up to first space)
                    current_chr_counts = Counter()
                    print(f"Processing: {current_chr_id}...", file=sys.stderr)
                else:
                    # Update counts (convert to uppercase for consistency)
                    counts = Counter(line.upper())
                    current_chr_counts.update(counts)
                    global_counts.update(counts)

            # Add the last chromosome after loop ends
            if current_chr_id:
                results.append(calculate_stats(current_chr_counts, current_chr_id))

        # Statistics for the full genome
        total_stats = calculate_stats(global_counts, "total")
        results.append(total_stats)

        # Save to CSV
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                'id', 'gc_perc', 'G', 'C', 'T', 'A', 'N', 
                'G_perc', 'C_perc', 'T_perc', 'A_perc', 'N_perc', 'len'
            ])
            # Write specific header required by instructions
            csvfile.write("chr_id/total,GC%,G,C,T,A,N,G%,C%,T%,A%,N%,len\n")
            for res in results:
                writer.writerow(res)

        # Display in PrettyTable
        table = PrettyTable()
        table.field_names = headers
        for res in results:
            table.add_row(res.values())
        
        print("\nAnalysis Summary:")
        print(table)

    except FileNotFoundError:
        print(f"Error: File '{input_path}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()