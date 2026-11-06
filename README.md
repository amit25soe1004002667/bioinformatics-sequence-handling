# Bioinformatics Sequence Handling

A reusable Python command-line tool that parses FASTA files and reports basic DNA sequence properties.

## Features
- Parses FASTA records with **Biopython** (`Bio.SeqIO`).
- Calculates sequence length and GC percentage.
- Counts A, C, G, and T separately.
- Reports ambiguous/non-ACGT symbols in an `other` column.
- Accepts one or multiple FASTA files in the same run.
- Writes one CSV row per sequence record.

## Project structure
```text
bioinformatics-sequence-handling/
├── data/sample_sequences.fasta
├── results/sequence_stats.csv
├── tests/test_sequence_stats.py
├── sequence_stats.py
├── requirements.txt
└── README.md
```

## Requirements
- Python 3.9+
- Biopython

Install:
```bash
python -m pip install -r requirements.txt
```

## Run
Analyze one FASTA file:
```bash
python sequence_stats.py data/sample_sequences.fasta
```

Analyze multiple FASTA files:
```bash
python sequence_stats.py data/sample_sequences.fasta data/another_file.fasta
```

Choose an output path:
```bash
python sequence_stats.py data/sample_sequences.fasta --output results/my_report.csv
```

Default output: `results/sequence_stats.csv`.

## Example output
| sequence_id | length | gc_percent | A | C | G | T | other |
|---|---:|---:|---:|---:|---:|---:|---:|
| seq1 | 10 | 40.00 | 3 | 2 | 2 | 3 | 0 |
| seq2 | 10 | 100.00 | 0 | 5 | 5 | 0 | 0 |
| seq3 | 8 | 25.00 | 1 | 1 | 1 | 1 | 4 |

GC percentage is `(G + C) / sequence length × 100`. Ambiguous symbols such as `N` are included in total length and reported under `other`, not counted as A/C/G/T.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Internship task mapping
- FASTA parsed with a script: `Bio.SeqIO.parse`
- Sequence length: `length`
- GC content: `gc_percent`
- Nucleotide composition: `A`, `C`, `G`, `T`
- Batch processing: pass multiple FASTA paths as command-line arguments