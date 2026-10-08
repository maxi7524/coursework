import os
import re
import pandas as pd

# ----------------------------------------------------------------------
# Helper functions for parsing files and logs
# ----------------------------------------------------------------------

def load_t2t_stats(csv_path):
    """Loads actual data from T2T_stats.csv and formats the table."""
    if not os.path.exists(csv_path):
        return "_Error: T2T_stats.csv not found._"
    df = pd.read_csv(csv_path)
    return df.to_markdown(index=False)


def parse_runtime_from_log(log_path):
    """Parses the performance table (Method | Runtime | ORFs) directly from the log file."""
    if not os.path.exists(log_path):
        return None
    
    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extracting lines matching the pattern: Method | Runtime | ORFs Found
    pattern = r"^\s*(BioPython|Pure Python|EMBOSS)\s*\|\s*([\d.]+)\s*\|\s*(\d+)"
    matches = re.findall(pattern, content, re.MULTILINE)
    
    if not matches:
        return None
        
    data = []
    for match in matches:
        data.append({
            "Method": match[0].strip(),
            "Runtime (sec)": float(match[1]),
            "ORFs Found": int(match[2])
        })
    return pd.DataFrame(data)


def parse_mapping_metrics(log_path, chr_name):
    """Parses the final mapping efficiency summary from the log file."""
    if not os.path.exists(log_path):
        return {
            "Chromosome": chr_name, "ORFs": "Calculating...", 
            "Mapped": "Calculating...", "Mapping Rate": "Calculating...", 
            "Unique Matches": "Calculating..."
        }
        
    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    orfs = re.search(r"orfs:\s*(\d+)", content)
    mapped = re.search(r"mapped:\s*(\d+)", content)
    rate = re.search(r"mapping_rate:\s*([\d.]+)%", content)
    unique = re.search(r"unique_reference_matches:\s*(\d+)", content)
    
    # If the script is still calculating and hasn't outputted the summary at the end of the log
    if not orfs:
        return {
            "Chromosome": chr_name, "ORFs": "Calculating...", 
            "Mapped": "Calculating...", "Mapping Rate": "Calculating...", 
            "Unique Matches": "Calculating..."
        }
        
    return {
        "Chromosome": chr_name,
        "ORFs": int(orfs.group(1)),
        "Mapped": int(mapped.group(1)),
        "Mapping Rate": f"{rate.group(1)}%",
        "Unique Matches": int(unique.group(1))
    }


# ----------------------------------------------------------------------
# Main function generating the .md report
# ----------------------------------------------------------------------

def build_report():
    t2t_csv = "data/results/T2T_stats.csv"
    log_chrm = "orf_map_chrM.log"
    log_chr1 = "orf_map_chr1.log"
    output_path = "genome_analysis_report.md"
    
    # Report header
    report = "# Genome Analysis Report\n\n"
    
    # Section 1: Genome characteristics
    report += "## 1. Genome Structural Characteristics\n\n"
    report += "The primary objective of this task was to analyze sequence topology of the human genome utilizing the T2T-CHM13 v2.0 assembly dataset.\n\n"
    report += "### Chromosome Statistics Table\n\n"
    report += load_t2t_stats(t2t_csv) + "\n\n"
    report += "> Chromosome Statistics Table is sorted in descending length order \n\n"
    
    report += "### Analysis\n"
    report += "- The human genome assembly has a total length of 3,117,292,070 bp with a global GC content of 40.75%, matching the reference literature data.\n"
    report += "- The mitochondrial genome (chrM) has a verified length of 16,569 bp and a GC content of 44.37%.\n"
    report += "- The highest regional GC content is located on chr19 (47.66%), which directly correlates with the highest chromosomal concentration of protein-coding genes.\n\n"
    
    # Section 2: Algorithm performance (Table 1 and Table 2)
    report += "## 2. 6-Frame ORF Finding Performance\n\n"
    report += "Three architectural approaches (BioPython, EMBOSS, and Pure Python) were benchmarked using different genetic code tables for nuclear (`chr1`) and mitochondrial (`chrM`) DNA sequences.\n\n"
    report += "### Method Runtimes for chrM\n\n"
    df_chrm_time = parse_runtime_from_log(log_chrm)
    if df_chrm_time is not None:
        report += df_chrm_time.to_markdown(index=False) + "\n\n"
    else:
        report += "_Error: No runtime data in orf_map_chrM.log_\n\n"
   
        
    report += "### Method Runtimes for chr1\n\n"
    df_chr1_time = parse_runtime_from_log(log_chr1)
    if df_chr1_time is not None:
        report += df_chr1_time.to_markdown(index=False) + "\n\n"
    else:
        report += "_Data calculation in progress or log file missing._\n\n"

    report += "### Analysis\n"
    report += "- BioPython may be slower than Pure Python because of additional W/R operations.\n"
    report += "- EMBOSS getorf yields a different number of ORFs because it defines an ORF simply as the region between two STOP codons. Meanwhile, BioPython and Pure Python duplicate these fragments by identifying multiple overlapping ORFs that initiate from different START codons but terminate at the same STOP codon.\n\n"
        
    # Section 3: Mapping and biological discrepancies (Table 3)
    report += "## 3. CDS Reference Mapping and Biological Discrepancies\n\n"
    report += "The calculated 6-frame open reading frames were cross-referenced against official UniProt human proteome reference files (`chm13.draft_v1.1.gene_annotation.protein.fasta`).\n\n"
    report += "### Reference Mapping Rate Table\n\n"
    
    metrics_chrm = parse_mapping_metrics(log_chrm, "chrM")
    metrics_chr1 = parse_mapping_metrics(log_chr1, "chr1")
    
    df_mapping = pd.DataFrame([metrics_chrm, metrics_chr1])
    report += df_mapping.to_markdown(index=False) + "\n\n"
    
    report += "### Biological Mechanism of Mapping Discrepancies\n"
    report += "- **Nuclear Genome (chr1):** Observed prediction mismatches are caused by the eukaryotic intronic gene structure and alternative splicing mechanisms. Raw 6-frame translation identifies hypothetical continuous open reading frames across genomic DNA, whereas physiological translation utilizes mature mRNA from which introns have been systematically removed.\n"
    report += "- **Mitochondrial Genome (chrM):** Mismatches are caused by post-transcriptional modifications. Eukaryotic mitochondrial transcripts are processed from polycistronic RNA units according to the tRNA punctuation model ([Ojala et al., 1981](https://pubmed.ncbi.nlm.nih.gov/7219536/)). Furthermore, functional termination codons (UAA) in several mitochondrial transcripts are not encoded in the genomic DNA sequence but are introduced post-transcriptionally via mRNA polyadenylation ([Anderson et al., 1981](https://pubmed.ncbi.nlm.nih.gov/7219534/)).\n"

    # Saving the report to a file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Raport został pomyślnie zapisany w: {output_path}")


if __name__ == "__main__":
    build_report()