import os
import argparse
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from scipy.stats import bootstrap

def parse_fasta_stats(fasta_path, group_name):
    """
    Parses FASTA file, filters non-standard AAs, and calculates basic stats.
    Includes bootstrapping for Standard Error of the Mean (SEM).
    """
    lengths = []
    aa_counter = Counter()
    to_exclude = {'U', 'X', 'Z', 'B'} # Non-standard/Ambiguous amino acids
    
    if not os.path.exists(fasta_path):
        return None

    with open(fasta_path, 'r') as f:
        seq = ""
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq:
                    lengths.append(len(seq))
                    filtered_seq = "".join([aa for aa in seq if aa not in to_exclude and aa.isalpha()])
                    aa_counter.update(filtered_seq)
                seq = ""
            else:
                seq += line
        if seq:
            lengths.append(len(seq))
            filtered_seq = "".join([aa for aa in seq if aa not in to_exclude and aa.isalpha()])
            aa_counter.update(filtered_seq)
            
    # Bootstrap for SEM (Lab 4, Task 2)
    std_err = 0
    if len(lengths) > 1:
        sample = np.random.choice(lengths, min(len(lengths), 5000), replace=False)
        try:
            res = bootstrap((sample,), np.mean, n_resamples=500, random_state=42)
            std_err = res.standard_error
        except:
            std_err = np.std(lengths) / np.sqrt(len(lengths))

    return {
        "Group": group_name,
        "Lengths": lengths,
        "Mean_Length": np.mean(lengths) if lengths else 0,
        "Median_Length": np.median(lengths) if lengths else 0,
        "Std_Err": std_err,
        "AA_Counts": aa_counter
    }


def process_group_data(files, names):
    """Helper to process multiple files and return combined AA dataframe and stats list."""
    all_stats = []
    aa_records = []
    for f, name in zip(files, names):
        s = parse_fasta_stats(f, name)
        if s:
            all_stats.append(s)
            total_aa = sum(s["AA_Counts"].values())
            for aa, count in s["AA_Counts"].items():
                aa_records.append({
                    "Group": name,
                    "AA": aa,
                    "Percentage": (count / total_aa * 100) if total_aa > 0 else 0
                })
    return pd.DataFrame(aa_records), all_stats


def export_aa_tables(stats_list, output_dir, filename):
    """Calculates AA percentages with SE and saves to CSV (Lab 4/5 requirement)."""
    rows = []
    standard_aas = "ACDEFGHIKLMNPQRSTVWY"
    for entry in stats_list:
        group = entry["Group"]
        total_aa = sum(entry["AA_Counts"].values())
        # Sample size is the number of proteins in this group
        n_proteins = len(entry["Lengths"]) 
        
        for aa in standard_aas:
            count = entry["AA_Counts"].get(aa, 0)
            mean_pct = (count / total_aa * 100) if total_aa > 0 else 0
            # Analytical Standard Error for proportions
            p = mean_pct / 100
            se_pct = (np.sqrt(p * (1 - p) / n_proteins) * 100) if n_proteins > 0 else 0
            
            rows.append({
                "Group": group,
                "AminoAcid": aa,
                "Percentage": round(mean_pct, 2),
                "StdErr": round(se_pct, 3)
            })
    pd.DataFrame(rows).to_csv(os.path.join(output_dir, filename), index=False)

def save_stats_to_csv(stats_list, output_path):
    """Saves summary statistics to a CSV file for report generation."""
    data = []
    for s in stats_list:
        data.append({
            "Group": s["Group"],
            "Mean_Length": round(s["Mean_Length"], 2),
            "SE": round(s["Std_Err"], 2),
            "Median_Length": int(s["Median_Length"]),
            "Sample_Size": len(s["Lengths"])
        })
    pd.DataFrame(data).to_csv(output_path, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["species", "kingdoms", "compare_pdb"], required=True)
    parser.add_argument("--input_files", nargs="+", required=True)
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--out_plots", required=True)
    parser.add_argument("--out_tables", required=True)
    parser.add_argument("--out_hists", required=False)
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        conf = yaml.safe_load(f)

    os.makedirs(args.out_plots, exist_ok=True)
    os.makedirs(args.out_tables, exist_ok=True)

    if args.mode == "species":
        # 1. Species Analysis (Lab 5, Ex 3a)
        names = [os.path.basename(f).replace(".fasta", "") for f in args.input_files]
        df_aa, stats = process_group_data(args.input_files, names)
        
        ## Get kingdom mapping from config 
        tax_map = conf['params'].get('taxonomy_mapping', {})
        
        plt.figure(figsize=(14, 8))

        ## Map each protein to its kingdom using the config taxonomy.
        data_list = []
        for s in stats:
            species_name = s["Group"]
            kingdom = tax_map.get(species_name, "Unknown")
            for l in s["Lengths"]:
                data_list.append({
                    "Species": species_name, 
                    "Length": l, 
                    "Kingdom": kingdom
                })
        
        len_df = pd.DataFrame(data_list)

        ## Create boxplot colored by kingdom (hue) with log scale for length.
        sns.boxplot(data=len_df, x="Species", y="Length", hue="Kingdom", dodge=False)
        plt.xticks(rotation=45) 
        plt.yscale('log')
        plt.title("Protein Length Distribution across Species (Grouped by Kingdom)")
        plt.tight_layout()
        
        plt.savefig(os.path.join(args.out_plots, "length_comparison_species.png"))

        # # WITHOUT SPECIES LABELS
        # # Plot Length Distribution (Boxplot with Log Scale)
        # plt.figure(figsize=(12, 6))
        # len_df = pd.DataFrame([{"Group": s["Group"], "Length": l} for s in stats for l in s["Lengths"]])
        # sns.boxplot(data=len_df, x="Group", y="Length")
        # plt.yscale('log')
        # plt.title("Protein Length Distribution across Species (Log Scale)")
        # plt.savefig(os.path.join(args.out_plots, "length_comparison_species.png"))
        
        # AA Barplot for comparison (E.coli, Human, Yeast)
        target_sp = ["E_coli", "Human", "Yeast"]
        subset_aa = df_aa[df_aa['Group'].isin(target_sp)]
        plt.figure(figsize=(14, 7))
        sns.barplot(data=subset_aa, x="AA", y="Percentage", hue="Group")
        plt.title("Amino Acid Content Comparison: E.coli vs Human vs Yeast")
        plt.savefig(os.path.join(args.out_plots, "aa_content_E_coli_Human_Yeast.png"))
        
        save_stats_to_csv(stats, os.path.join(args.out_tables, "species_stats.csv"))
        export_aa_tables(stats, args.out_tables, "aa_species_stats.csv")

        # Generate histograms for each species (Lab 5, Ex 3d)
        for s in stats:
            plt.figure(figsize=(8, 5))
            
        ## Plot histogram with Kernel Density Estimate (KDE) for length distribution.
            sns.histplot(s["Lengths"], bins=50, kde=True)
            
        ## Add vertical lines for Mean (red) and Median (green) to show distribution skew.
            plt.axvline(s["Mean_Length"], color='red', linestyle='dashed', label=f'Mean: {s["Mean_Length"]:.1f}')
            plt.axvline(s["Median_Length"], color='green', linestyle='dashed', label=f'Median: {s["Median_Length"]:.1f}')
            
            plt.title(f"Protein Length Histogram: {s['Group']}")
            plt.xlabel("Length (AA)")
            plt.legend()
            plt.tight_layout()
            
        ## Save individual histograms using species name.
            plt.savefig(os.path.join(args.out_hists, f"hist_{s['Group']}.png"))
            plt.close()

        


    elif args.mode == "kingdoms":
        # 2. Kingdom Analysis (Lab 4, Ex 3c)
        names = [os.path.basename(f).replace(".fasta", "") for f in args.input_files]
        df_aa, stats = process_group_data(args.input_files, names)
        
        # --- DODANO: Wykres długości dla królestw ---
        plt.figure(figsize=(12, 6))
        len_df = pd.DataFrame([{"Group": s["Group"], "Length": l} for s in stats for l in s["Lengths"]])
        sns.boxplot(data=len_df, x="Group", y="Length")
        plt.yscale('log')
        plt.title("Protein Length Distribution across Kingdoms (Log Scale)")
        plt.savefig(os.path.join(args.out_plots, "length_comparison_kingdoms.png"))
        
        # Istniejący wykres AA
        plt.figure(figsize=(14, 7))
        sns.barplot(data=df_aa, x="AA", y="Percentage", hue="Group")
        plt.title("Average AA Content: Kingdoms")
        plt.savefig(os.path.join(args.out_plots, "aa_content_kingdoms.png"))
        
        save_stats_to_csv(stats, os.path.join(args.out_tables, "kingdom_stats.csv"))
        export_aa_tables(stats, args.out_tables, "aa_kingdoms_stats.csv")

        

    elif args.mode == "compare_pdb":
        # 3. PDB vs UniProt Comparison (Lab 4, Task 1)
        # Assuming first file is PDB, rest are UniProt kingdoms
        pdb_file = args.input_files[0]
        uniprot_files = args.input_files[1:]
        
        pdb_stats = parse_fasta_stats(pdb_file, "PDB")
        _, uni_stats_list = process_group_data(uniprot_files, ["UniProt"] * len(uniprot_files))
        
        # Merge UniProt lengths for comparison
        all_uni_lengths = []
        combined_uni_aa = Counter()
        for s in uni_stats_list:
            all_uni_lengths.extend(s["Lengths"])
            combined_uni_aa.update(s["AA_Counts"])
            
        

        # Boxplot Comparison
        plt.figure(figsize=(10, 6))
        comp_df = pd.DataFrame({
            "Database": ["PDB"] * len(pdb_stats["Lengths"]) + ["UniProt"] * len(all_uni_lengths),
            "Length": pdb_stats["Lengths"] + all_uni_lengths
        })
        sns.boxplot(data=comp_df, x="Database", y="Length")
        plt.yscale('log')
        plt.title("Protein Length Comparison: PDB vs UniProt")
        plt.savefig(os.path.join(args.out_plots, "length_comparison_pdb_vs_uniprot.png"))
        
        # AA comparison 
        ## data for plot
        aa_comp_records = []
        # pdb data
        total_pdb_aa = sum(pdb_stats["AA_Counts"].values())
        for aa, count in pdb_stats["AA_Counts"].items():
            aa_comp_records.append({
                "Database": "PDB",
                "AA": aa,
                "Percentage": (count / total_pdb_aa * 100) if total_pdb_aa > 0 else 0
            })
        ## joined kingdom data
        uni_aa_counts = Counter()
        for s in uni_stats_list:
            uni_aa_counts.update(s["AA_Counts"])
            
        total_uni_aa = sum(uni_aa_counts.values())
        for aa, count in uni_aa_counts.items():
            aa_comp_records.append({
                "Database": "UniProt",
                "AA": aa,
                "Percentage": (count / total_uni_aa * 100) if total_uni_aa > 0 else 0
            })
        ## merging results
        df_aa_comp = pd.DataFrame(aa_comp_records)

        

        ## drawing plot 
        plt.figure(figsize=(14, 7))
        sns.barplot(data=df_aa_comp, x="AA", y="Percentage", hue="Database")
        plt.title("Amino Acid Content Comparison: PDB vs UniProt")
        plt.savefig(os.path.join(args.out_plots, "aa_content_pdb_vs_uniprot.png"))

        # Summary CSV
        uni_summary = {
            "Group": "UniProt",
            "Lengths": all_uni_lengths,
            "Mean_Length": np.mean(all_uni_lengths) if all_uni_lengths else 0,
            "Median_Length": np.median(all_uni_lengths) if all_uni_lengths else 0,
            "Std_Err": np.std(all_uni_lengths) / np.sqrt(len(all_uni_lengths)) if all_uni_lengths else 0,
            "AA_Counts": combined_uni_aa
        }
        save_stats_to_csv([pdb_stats, uni_summary], os.path.join(args.out_tables, "comparison_pdb_uniprot.csv"))
        export_aa_tables([pdb_stats, uni_summary], args.out_tables, "aa_pdb_vs_uniprot.csv")

    print(f"Done. Mode: {args.mode}")

if __name__ == "__main__":
    main()