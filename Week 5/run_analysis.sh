#!/usr/bin/env bash

set -euo pipefail
export LC_ALL=C

# Make sure the script runs from the project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Starting reproducible albumin analysis..."

# 1. Create directories

mkdir -p data output


# 2. Download albumin protein sequences from UniProt

echo "Downloading albumin sequences from UniProt..."

curl -fsSL "https://rest.uniprot.org/uniprotkb/P02769.fasta" \
  -o data/bos_taurus_albumin.fasta

curl -fsSL "https://rest.uniprot.org/uniprotkb/P14639.fasta" \
  -o data/ovis_aries_albumin.fasta

curl -fsSL "https://rest.uniprot.org/uniprotkb/P08835.fasta" \
  -o data/sus_scrofa_albumin.fasta

curl -fsSL "https://rest.uniprot.org/uniprotkb/P35747.fasta" \
  -o data/equus_caballus_albumin.fasta

curl -fsSL "https://rest.uniprot.org/uniprotkb/P02768.fasta" \
  -o data/homo_sapiens_albumin.fasta

curl -fsSL "https://rest.uniprot.org/uniprotkb/P07724.fasta" \
  -o data/mus_musculus_albumin.fasta


# 3. Combine sequences into one FASTA file

echo "Combining sequences..."

cat \
  data/bos_taurus_albumin.fasta \
  data/ovis_aries_albumin.fasta \
  data/sus_scrofa_albumin.fasta \
  data/equus_caballus_albumin.fasta \
  data/homo_sapiens_albumin.fasta \
  data/mus_musculus_albumin.fasta \
  > data/albumin_sequences.fasta


# 4. Multiple sequence alignment with MAFFT

echo "Running MAFFT..."

mafft \
  --auto \
  --thread 1 \
  data/albumin_sequences.fasta \
  > output/albumin_alignment.fasta


# 5. Generate alignment statistics with EMBOSS

echo "Generating alignment statistics..."

infoalign \
  -sequence output/albumin_alignment.fasta \
  -outfile output/alignment_stats.txt


# 6. Generate SHA256 checksums

echo "Generating SHA256 checksums..."

sha256sum \
  data/bos_taurus_albumin.fasta \
  data/ovis_aries_albumin.fasta \
  data/sus_scrofa_albumin.fasta \
  data/equus_caballus_albumin.fasta \
  data/homo_sapiens_albumin.fasta \
  data/mus_musculus_albumin.fasta \
  data/albumin_sequences.fasta \
  output/albumin_alignment.fasta \
  output/alignment_stats.txt \
  > CHECKSUMS.txt


echo ""
echo "Analysis complete!"
echo "Outputs:"
echo "  output/albumin_alignment.fasta"
echo "  output/alignment_stats.txt"
echo "Checksums:"
echo "  CHECKSUMS.txt"
