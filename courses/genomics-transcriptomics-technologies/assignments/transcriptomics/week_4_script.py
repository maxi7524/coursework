import os
import subprocess
import sys

# --- CONFIGURATION ---
SAMPLE_NAME = "yeast_sample"
THREADS = 4

PROJECT_DIR = "Project1"
GENOME_DIR = os.path.join(PROJECT_DIR, "genome")
FASTQ_DIR = os.path.join(PROJECT_DIR, "fastq")
FASTP_DIR = os.path.join(PROJECT_DIR, "fastp")
FASTQC_DIR = os.path.join(PROJECT_DIR, "fastqc")
BAM_DIR = os.path.join(PROJECT_DIR, "bam")
COUNTS_DIR = os.path.join(PROJECT_DIR, "counts")

# Files and paths
R1_RAW = "data/yeast_sample/deltadis32_replicate1.fastq.gz"
R2_RAW = "data/yeast_sample/deltadis32_replicate2.fastq.gz"
GENOME_FASTA = "data/genome/Schizosaccharomyces_pombe_all_chromosomes.fa"
ANNOTATION_GFF = "data/genome/Schizosaccharomyces_pombe_all_chromosomes.gff3"

# Create necessary directory structure
for d in [GENOME_DIR, FASTQ_DIR, FASTP_DIR, FASTQC_DIR, BAM_DIR, COUNTS_DIR]:
    os.makedirs(d, exist_ok=True)

def run_command(step_name, command, output_to_check=None):
    """
    Runs the command only if the specified output file does not exist.
    Stops the script immediately if the command fails.
    """
    if output_to_check and os.path.exists(output_to_check):
        print(f"--- Skipping: {step_name} (Output already exists) ---")
        return

    print(f"--- Running: {step_name} ---")
    print(f"Command: {command}")
    
    # check=False is used manually to handle exit via sys.exit(1)
    result = subprocess.run(command, shell=True)
    
    if result.returncode != 0:
        print(f"ERROR in step '{step_name}'. Exiting pipeline.")
        sys.exit(1)

# --- 1. Quality Control (Raw Data) ---
run_command("FastQC (raw data)", 
            f"fastqc {R1_RAW} {R2_RAW} -o {FASTQC_DIR}", 
            os.path.join(FASTQC_DIR, "deltadis32_replicate1_fastqc.html"))

# --- 2. Subsampling ---
# Extracting 2 million reads (8 million lines) to speed up the process
run_command("Subsampling (2M reads)", 
            f"gzcat {R1_RAW} | head -n 8000000 > {FASTQ_DIR}/sub_R1.fastq && "
            f"gzcat {R2_RAW} | head -n 8000000 > {FASTQ_DIR}/sub_R2.fastq",
            f"{FASTQ_DIR}/sub_R1.fastq")

# --- 3. Filtering and Trimming (fastp) ---
run_command("Filtering fastp",
            f"fastp -i {FASTQ_DIR}/sub_R1.fastq -I {FASTQ_DIR}/sub_R2.fastq "
            f"-o {FASTP_DIR}/trimmed_R1.fastq -O {FASTP_DIR}/trimmed_R2.fastq "
            f"--html {FASTP_DIR}/report.html --json {FASTP_DIR}/report.json",
            f"{FASTP_DIR}/trimmed_R1.fastq")

# --- 4. Quality Control (Filtered Data) ---
run_command("FastQC (filtered data)", 
            f"fastqc {FASTP_DIR}/trimmed_R1.fastq {FASTP_DIR}/trimmed_R2.fastq -o {FASTQC_DIR}", 
            os.path.join(FASTQC_DIR, "trimmed_R1_fastqc.html"))

# --- 5. Building STAR Genome Index ---
# Note: Using genomeParameters.txt to verify successful indexing
run_command("Building STAR index",
            f"STAR --runMode genomeGenerate --genomeDir {GENOME_DIR} "
            f"--genomeFastaFiles {GENOME_FASTA} --sjdbGTFfile {ANNOTATION_GFF} "
            f"--sjdbGTFfeatureExon exon --sjdbGTFtagExonParentTranscript Parent "
            f"--genomeSAindexNbases 8 --runThreadN {THREADS}",
            os.path.join(GENOME_DIR, "genomeParameters.txt"))

# --- 6. Read Mapping (STAR) ---
run_command("STAR mapping",
            f"STAR --genomeDir {GENOME_DIR} --readFilesIn {FASTP_DIR}/trimmed_R1.fastq {FASTP_DIR}/trimmed_R2.fastq "
            f"--alignIntronMax 1000 --outSAMtype BAM Unsorted "
            f"--outFileNamePrefix {BAM_DIR}/{SAMPLE_NAME}_ --runThreadN {THREADS}",
            f"{BAM_DIR}/{SAMPLE_NAME}_Aligned.out.bam")

# --- 7. BAM Sorting and Indexing (samtools) ---
run_command("BAM sorting and indexing",
            f"samtools sort {BAM_DIR}/{SAMPLE_NAME}_Aligned.out.bam -o {BAM_DIR}/{SAMPLE_NAME}_sorted.bam && "
            f"samtools index {BAM_DIR}/{SAMPLE_NAME}_sorted.bam",
            f"{BAM_DIR}/{SAMPLE_NAME}_sorted.bam")

# --- 8. Gene Expression Quantification (htseq-count) ---
run_command("Read counting (htseq-count)",
            f"htseq-count -f bam -t gene -i ID -s reverse "
            f"{BAM_DIR}/{SAMPLE_NAME}_sorted.bam {ANNOTATION_GFF} > {COUNTS_DIR}/{SAMPLE_NAME}_counts.txt",
            f"{COUNTS_DIR}/{SAMPLE_NAME}_counts.txt")

# --- 9. Post-processing Gene Names ---
# Removes 'gene-' prefix from IDs if it exists
input_counts = f"{COUNTS_DIR}/{SAMPLE_NAME}_counts.txt"
output_counts = f"{COUNTS_DIR}/{SAMPLE_NAME}_final_counts.txt"

if not os.path.exists(output_counts) and os.path.exists(input_counts):
    print("--- Running: Cleaning gene names ---")
    with open(input_counts, 'r') as fin, open(output_counts, 'w') as fout:
        for line in fin:
            fout.write(line.replace('gene-', ''))
else:
    print("--- Skipping: Cleaning gene names (Output already exists) ---")

# --- 10. Generating BigWig for Visualization (deepTools) ---
run_command("Generating BigWig (deeptools)",
            f"bamCoverage -b {BAM_DIR}/{SAMPLE_NAME}_sorted.bam -o {BAM_DIR}/{SAMPLE_NAME}.bw",
            f"{BAM_DIR}/{SAMPLE_NAME}.bw")

print("\n--- PIPELINE COMPLETED SUCCESSFULLY ---")