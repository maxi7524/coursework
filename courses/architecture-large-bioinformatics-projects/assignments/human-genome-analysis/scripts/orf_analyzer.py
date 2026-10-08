#!/usr/bin/env python3

from pathlib import Path
import argparse
import subprocess
import tempfile
import csv
import time
import gzip
import shutil
import re
import sys
from Bio import SeqIO
from Bio.Seq import Seq

# --- GENETIC CODES ---

STANDARD_CODE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L", "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*", "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L", "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q", "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M", "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K", "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V", "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E", "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}

MITO_CODE = STANDARD_CODE.copy()
MITO_CODE.update({
    "TGA": "W",
    "ATA": "M",
    "AGA": "*",
    "AGG": "*",
})


# --- HELPERS ---

def open_maybe_gzip(path: Path):
    """Open .fa or .fa.gz file in text mode."""
    if path.suffix == ".gz":
        return gzip.open(path, "rt")
    else:
        return open(path, "rt")


def read_all_fasta_records(path: Path):
    """Read all records from a FASTA file supporting gzip."""
    records = []
    with open_maybe_gzip(path) as handle:
        for record in SeqIO.parse(handle, "fasta"):
            records.append((record.id, str(record.seq).upper()))
    return records


def make_plain_fasta_if_needed(input_path: Path, tmpdir: Path):
    """Decompress gzipped FASTA to a temporary file if needed for EMBOSS."""
    if input_path.suffix != ".gz":
        return input_path

    plain_path = tmpdir / input_path.with_suffix("").name
    with gzip.open(input_path, "rt") as fin, open(plain_path, "w") as fout:
        shutil.copyfileobj(fin, fout)
    return plain_path


def get_stop_codons(genetic_code: int):
    """Return stop codons based on genetic code ID."""
    if genetic_code == 1:
        return {"TAA", "TAG", "TGA"}
    elif genetic_code == 2:
        return {"TAA", "TAG", "AGA", "AGG"}


# --- PURE PYTHON LOGIC ---

def revcomp(seq):
    """Return reverse complement sequence."""
    table = str.maketrans("ACGTN", "TGCAN")
    return seq.translate(table)[::-1]


def translate_pure(seq, code):
    """Translate DNA to Amino Acids using pure python dictionary."""
    aa = []
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i : i + 3]
        aa.append(code.get(codon, "X"))
    return "".join(aa)


def find_orfs_pure_frame(seq, seq_id, strand, frame, code, min_aa):
    """Find ORFs in a single frame using pure Python logic."""
    stop_codons = {codon for codon, aa in code.items() if aa == "*"}
    start_codons = {"ATG"}
    orfs = []
    i = frame

    while i <= len(seq) - 3:
        codon = seq[i : i + 3]
        if codon in start_codons:
            j = i
            while j <= len(seq) - 3:
                stop = seq[j : j + 3]
                if stop in stop_codons:
                    nt_seq = seq[i : j + 3]
                    protein = translate_pure(nt_seq, code).rstrip("*")
                    if len(protein) >= min_aa:
                        orfs.append({
                            "seq_id": seq_id, "method": "pure", "strand": strand,
                            "frame": frame + 1, "start": i + 1, "end": j + 3,
                            "length_nt": len(nt_seq), "length_aa": len(protein), "protein": protein,
                        })
                    break
                j += 3
        i += 3
    return orfs


def run_pure_python(records, genetic_code, min_aa):
    """Process all records using the pure Python method."""
    code = STANDARD_CODE if genetic_code == 1 else MITO_CODE
    all_orfs = []
    for seq_id, seq in records:
        for frame in range(3):
            all_orfs.extend(find_orfs_pure_frame(seq, seq_id, "+", frame, code, min_aa))
        rc = revcomp(seq)
        for frame in range(3):
            all_orfs.extend(find_orfs_pure_frame(rc, seq_id, "-", frame, code, min_aa))
    return all_orfs


# --- BIOPYTHON LOGIC ---

def find_orfs_biopython_frame(seq, seq_id, strand, frame, genetic_code, min_aa):
    """Find ORFs in a single frame using BioPython translation."""
    stop_codons = get_stop_codons(genetic_code)
    start_codons = {"ATG"}
    orfs = []
    i = frame

    while i <= len(seq) - 3:
        codon = seq[i : i + 3]
        if codon in start_codons:
            j = i
            while j <= len(seq) - 3:
                stop = seq[j : j + 3]
                if stop in stop_codons:
                    nt_seq = seq[i : j + 3]
                    protein = str(Seq(nt_seq).translate(table=genetic_code)).rstrip("*")
                    if len(protein) >= min_aa:
                        orfs.append({
                            "seq_id": seq_id, "method": "biopython", "strand": strand,
                            "frame": frame + 1, "start": i + 1, "end": j + 3,
                            "length_nt": len(nt_seq), "length_aa": len(protein), "protein": protein,
                        })
                    break
                j += 3
        i += 3
    return orfs


def run_biopython(records, genetic_code, min_aa):
    """Process all records using the BioPython method."""
    all_orfs = []
    for seq_id, seq in records:
        for frame in range(3):
            all_orfs.extend(find_orfs_biopython_frame(seq, seq_id, "+", frame, genetic_code, min_aa))
        rc = str(Seq(seq).reverse_complement())
        for frame in range(3):
            all_orfs.extend(find_orfs_biopython_frame(rc, seq_id, "-", frame, genetic_code, min_aa))
    return all_orfs


# --- EMBOSS WRAPPER LOGIC ---

import os

def run_getorf(input_fasta: Path, output_faa: Path, genetic_code: int, min_aa: int):
    """Wraps EMBOSS getorf tool and captures stderr for explicit debugging."""
    minsize_nt = min_aa * 3
    cmd = [
        "getorf", "-sequence", str(input_fasta), "-outseq", str(output_faa),
        "-table", str(genetic_code), "-minsize", str(minsize_nt), "-find", "1",
    ]
    
    # Explicitly configure environment variables for EMBOSS inside the subprocess
    env = os.environ.copy()
    bio_env_path = "/home/ms488923/micromamba/envs/bio_env"
    
    env["EMBOSS_DATA"] = f"{bio_env_path}/share/EMBOSS/data"
    env["EMBOSS_ACDROOT"] = f"{bio_env_path}/share/EMBOSS/acd"
    
    # Ensure the environment bin directory is present in PATH
    if f"{bio_env_path}/bin" not in env.get("PATH", ""):
        env["PATH"] = f"{bio_env_path}/bin:{env.get('PATH', '')}"

    try:
        # Pass the explicit environment dictionary to ensure EMBOSS finds its translation tables (EGC.*)
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, env=env)
        return True
    except FileNotFoundError:
        print("\n[ERROR] EMBOSS 'getorf' is not installed or not in PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] EMBOSS 'getorf' failed execution.")
        print(f"[EMBOSS STDERR]: {e.stderr}\n")
        return False


def parse_one_emboss_record(header: str, seq_lines: list[str]):
    """Parse metadata and sequence from a single EMBOSS record."""
    protein = "".join(seq_lines).replace("*", "")
    length_aa = len(protein)
    seq_id = header.split()[0]

    strand, frame, start, end = "NA", "NA", "NA", "NA"
    coord_match = re.search(r"\[(.+?)\]", header)
    if coord_match:
        coord_text = coord_match.group(1)
        strand = "-" if "complement" in coord_text else "+"
        nums = re.findall(r"\d+", coord_text)
        if len(nums) >= 2:
            start = int(nums[0])
            end = int(nums[1])

    return {
        "seq_id": seq_id, "method": "emboss", "strand": strand, "frame": frame,
        "start": start, "end": end, "length_nt": length_aa * 3, "length_aa": length_aa, "protein": protein,
    }


def parse_emboss_fasta(faa_path: Path):
    """Parse full output FASTA generated by EMBOSS getorf."""
    orfs = []
    current_header = None
    seq_lines = []

    with open(faa_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_header is not None:
                    orfs.append(parse_one_emboss_record(current_header, seq_lines))
                current_header = line[1:]
                seq_lines = []
            else:
                seq_lines.append(line)

    if current_header is not None:
        orfs.append(parse_one_emboss_record(current_header, seq_lines))
    return orfs


# --- OUTPUT WRITER ---

def write_combined_csv(orfs, output_path: Path):
    """Write all generated ORFs from all methods into a single CSV file."""
    columns = ["seq_id", "method", "strand", "frame", "start", "end", "length_nt", "length_aa", "protein"]
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(orfs)


# --- MAIN PIPELINE ---

def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive 6-frame ORF Discovery Tool (Comparison Mode)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-I", "--input", required=True, type=Path, help="Path to Input .fasta or .fasta.gz file")
    parser.add_argument("-O", "--output", required=True, type=Path, help="Path to aggregated output .csv file")
    parser.add_argument(
        "--genetic-code", required=True, type=int, choices=[1, 2],
        help="1 = Standard universal code, 2 = Vertebrate mitochondrial code"
    )
    parser.add_argument("--min-aa", type=int, default=100, help="Minimum amino acid length for ORF filtering")

    args = parser.parse_args()

    # Load all records for Python-based loops
    records = read_all_fasta_records(args.input)
    print(f"Loaded {len(records)} record(s) from {args.input.name}")

    all_discovered_orfs = []

    # 1. Run BioPython
    print("Running BioPython discovery...")
    start = time.perf_counter()
    bio_orfs = run_biopython(records, args.genetic_code, args.min_aa)
    time_bio = time.perf_counter() - start
    all_discovered_orfs.extend(bio_orfs)

    # 2. Run Pure Python
    print("Running Pure Python discovery...")
    start = time.perf_counter()
    pure_orfs = run_pure_python(records, args.genetic_code, args.min_aa)
    time_pure = time.perf_counter() - start
    all_discovered_orfs.extend(pure_orfs)

    # 3. Run EMBOSS
    print("Running EMBOSS getorf discovery...")
    start = time.perf_counter()
    emboss_orfs = []
    
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        emboss_input = make_plain_fasta_if_needed(args.input, tmpdir)
        emboss_output = tmpdir / "getorf_output.faa"
        
        # Call with explicit error-catching and text decoding logic
        if run_getorf(emboss_input, emboss_output, args.genetic_code, args.min_aa):
            if emboss_output.exists():
                emboss_orfs = parse_emboss_fasta(emboss_output)
                all_discovered_orfs.extend(emboss_orfs)
                time_emboss = time.perf_counter() - start
        else:
            time_emboss = 0.0

    # Write all data to the designated CSV
    write_combined_csv(all_discovered_orfs, args.output)

    # CLI summary printout
    print("\n" + "="*50)
    print(f"{'Method':<15} | {'Runtime (sec)':<15} | {'ORFs Found':<10}")
    print("-"*50)
    print(f"{'BioPython':<15} | {time_bio:<15.3f} | {len(bio_orfs):<10}")
    print(f"{'Pure Python':<15} | {time_pure:<15.3f} | {len(pure_orfs):<10}")
    print(f"{'EMBOSS':<15} | {time_emboss:<15.3f} | {len(emboss_orfs):<10}")
    print("="*50)
    print(f"Success! All results compiled into: {args.output}\n")


if __name__ == "__main__":
    main()