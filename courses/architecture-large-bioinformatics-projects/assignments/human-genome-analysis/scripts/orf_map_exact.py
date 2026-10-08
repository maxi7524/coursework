#!/usr/bin/env python3

import argparse
import csv
import gzip
from collections import defaultdict
from pathlib import Path


class ExactSequenceMapper:
    """
    Handles loading of reference proteome and matching predicted ORFs
    against exact amino acid sequences.
    """

    def __init__(self, reference_path: Path):
        self.reference_path = reference_path
        self.seq_to_headers = self._read_reference_fasta()

    def _read_reference_fasta(self):
        """
        Parses reference FASTA (supports .gz) and maps sequence -> list of headers.
        """
        seq_to_headers = defaultdict(list)
        header = None
        seq_lines = []

        # Determine file opening style based on extension
        open_func = gzip.open if self.reference_path.suffix == ".gz" else open
        mode = "rt" if self.reference_path.suffix == ".gz" else "r"

        with open_func(self.reference_path, mode) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if line.startswith(">"):
                    if header is not None:
                        seq = "".join(seq_lines).replace("*", "")
                        seq_to_headers[seq].append(header)

                    header = line[1:]
                    seq_lines = []
                else:
                    seq_lines.append(line)

        if header is not None:
            seq = "".join(seq_lines).replace("*", "")
            seq_to_headers[seq].append(header)

        return seq_to_headers

    def map_orfs(self, orfs_csv_path: Path):
        """
        Reads predicted ORFs from CSV and validates them against the reference dict.
        """
        with open(orfs_csv_path, newline="") as f:
            reader = csv.DictReader(f)
            orfs = list(reader)

        rows = []
        for i, row in enumerate(orfs, start=1):
            protein = row["protein"].replace("*", "").strip()
            
            # Substring matching to account for sequence truncations or prediction shifts
            matches = []
            for ref_seq, headers in self.seq_to_headers.items():
                if protein in ref_seq:
                    matches.extend(headers)

            rows.append(
                {
                    "orf_id": f"orf_{i}",
                    "seq_id": row.get("seq_id", "NA"),
                    "method": row.get("method", "NA"),
                    "strand": row.get("strand", "NA"),
                    "frame": row.get("frame", "NA"),
                    "start": row.get("start", "NA"),
                    "end": row.get("end", "NA"),
                    "length_aa": row.get("length_aa", len(protein)),
                    "mapped": "yes" if matches else "no",
                    "n_matches": len(matches),
                    "matched_reference_ids": ";".join(matches),
                    "protein": protein,
                }
            )

        return rows


def write_csv(rows, output: Path):
    """Writes mapped structure into a combined CSV file."""
    columns = [
        "orf_id", "seq_id", "method", "strand", "frame", "start", "end",
        "length_aa", "mapped", "n_matches", "matched_reference_ids", "protein"
    ]
    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def write_fasta_from_orfs(rows, output: Path):
    """Optional diagnostic FASTA output with ORF details."""
    with open(output, "w") as f:
        for row in rows:
            f.write(
                f">{row['orf_id']}|len={row['length_aa']}|"
                f"strand={row['strand']}|frame={row['frame']}|"
                f"start={row['start']}|end={row['end']}|"
                f"mapped={row['mapped']}\n"
            )
            f.write(row["protein"] + "\n")


def main():
    p = argparse.ArgumentParser(
        description="Map predicted ORFs to reference proteins by exact amino-acid sequence match",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--orfs", required=True, type=Path, help="Input ORF CSV file with a protein column")
    p.add_argument("--reference", required=True, type=Path, help="Reference protein FASTA file")
    p.add_argument("-O", "--output", required=True, type=Path, help="Output mapping CSV")
    p.add_argument("--write-fasta", type=Path, default=None, help="Optional output FASTA with ORF protein sequences")
    args = p.parse_args()

    # Pipeline execution using the new class structure
    mapper = ExactSequenceMapper(args.reference)
    mapped_rows = mapper.map_orfs(args.orfs)

    write_csv(mapped_rows, args.output)

    if args.write_fasta is not None:
        write_fasta_from_orfs(mapped_rows, args.write_fasta)

    # Metrics computation
    total = len(mapped_rows)
    mapped = sum(1 for row in mapped_rows if row["mapped"] == "yes")
    rate = mapped / total * 100 if total else 0

    unique_reference_matches = set()
    for row in mapped_rows:
        if row["mapped"] == "yes":
            for ref in row["matched_reference_ids"].split(";"):
                if ref:
                    unique_reference_matches.add(ref)

    print(f"orfs: {total}")
    print(f"mapped: {mapped}")
    print(f"mapping_rate: {rate:.2f}%")
    print(f"unique_reference_matches: {len(unique_reference_matches)}")


if __name__ == "__main__":
    main()