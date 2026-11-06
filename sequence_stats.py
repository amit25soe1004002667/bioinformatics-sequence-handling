#!/usr/bin/env python3
"""Calculate basic nucleotide statistics for records in FASTA files."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Iterable

from Bio import SeqIO

BASES = ("A", "C", "G", "T")


def summarize_sequence(sequence: str) -> dict[str, object]:
    """Return length, GC percentage, and A/C/G/T counts for one sequence."""
    normalized = sequence.upper().replace(" ", "").replace("\n", "")
    counts = {base: normalized.count(base) for base in BASES}
    length = len(normalized)
    gc_count = counts["G"] + counts["C"]
    return {
        "length": length,
        "gc_percent": round((gc_count / length) * 100, 2) if length else 0.0,
        "A": counts["A"],
        "C": counts["C"],
        "G": counts["G"],
        "T": counts["T"],
        "other": length - sum(counts.values()),
    }


def analyze_fasta(paths: Iterable[Path]) -> list[dict[str, object]]:
    """Parse all input FASTA files and calculate one row per sequence record."""
    rows: list[dict[str, object]] = []
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(f"Input FASTA file not found: {path}")
        records = list(SeqIO.parse(str(path), "fasta"))
        if not records:
            raise ValueError(f"No FASTA records found in: {path}")
        for record in records:
            stats = summarize_sequence(str(record.seq))
            rows.append({
                "source_file": path.name,
                "sequence_id": record.id,
                "description": record.description,
                **stats,
            })
    return rows


def write_csv(rows: list[dict[str, object]], output: Path) -> None:
    """Write sequence statistics to a CSV file."""
    fieldnames = [
        "source_file", "sequence_id", "description", "length",
        "gc_percent", "A", "C", "G", "T", "other",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calculate length, GC content, and nucleotide composition from FASTA."
    )
    parser.add_argument(
        "fasta", nargs="+", type=Path,
        help="One or more FASTA files (all files must be in FASTA format).",
    )
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("results/sequence_stats.csv"),
        help="Output CSV path (default: results/sequence_stats.csv).",
    )
    args = parser.parse_args()

    try:
        rows = analyze_fasta(args.fasta)
        write_csv(rows, args.output)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Analyzed {len(rows)} sequence(s). Results saved to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())