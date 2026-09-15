# Week 4 - mimicDetector

## Dataset selection and preparation

For my analysis, I selected *Cryptosporidium parvum* as the pathogen and *Homo sapiens* as the host. I selected *Eimeria tenella* as the negative control because it is also an Apicomplexan parasite related to *C. parvum*, but it is not a human pathogen.

I downloaded the *C. parvum* Iowa II reference proteome (UP000006726) and the *E. tenella* proteome (UP000030747) from UniProt in FASTA format.

I created the directories required by mimicDetector:

```bash
mkdir -p ~/mimic_data/host/structures
mkdir -p ~/mimic_data/C_parvum/structures
mkdir -p ~/mimic_data/controls
```

The downloaded FASTA files were copied to the corresponding directories and renamed:

```bash
cp /mnt/c/Users/amc0369/Downloads/uniprotkb_proteome_UP000006726_2026_09_15.fasta.gz \
~/mimic_data/C_parvum/C_parvum.fasta.gz

cp /mnt/c/Users/amc0369/Downloads/uniprotkb_proteome_UP000030747_2026_09_15.fasta.gz \
~/mimic_data/controls/E_tenella.fasta.gz

gunzip ~/mimic_data/C_parvum/C_parvum.fasta.gz
gunzip ~/mimic_data/controls/E_tenella.fasta.gz
```

I checked the number of protein sequences in each FASTA file:

```bash
grep -c "^>" ~/mimic_data/C_parvum/C_parvum.fasta
grep -c "^>" ~/mimic_data/controls/E_tenella/E_tenella.fasta
```

The *C. parvum* proteome contained **3,805 proteins**, while the *E. tenella* proteome contained **8,595 proteins**.

I also checked the FASTA headers:

```bash
grep "^>" ~/mimic_data/C_parvum/C_parvum.fasta | head -n 3
grep "^>" ~/mimic_data/controls/E_tenella.fasta | head -n 3
```

The proteins downloaded from UniProt use headers such as:

```text
>tr|A3FPL9|A3FPL9_CRYPI
>sp|A3FPN7|FEN1_CRYPI
```

I checked the mimicDetector code to make sure this format could be used. The program extracts the UniProt accession from the FASTA header when needed, so I kept the original UniProt headers.

---

## Human proteome

For the host, I downloaded the *Homo sapiens* reference proteome **UP000005640** from UniProt.

The downloaded file contained **147,503 protein sequences**.

I checked how many entries were reviewed (Swiss-Prot) and unreviewed (TrEMBL):

```bash
grep -c "^>sp|" ~/mimic_data/host/H_sapiens.fasta
grep -c "^>tr|" ~/mimic_data/host/H_sapiens.fasta
```

The file contained:

- **20,416 reviewed proteins**
- **127,087 unreviewed proteins**

Because the complete human dataset was very large, I decided to use only the reviewed proteins for the analysis.

I created a Python script using Biopython to keep only sequences with Swiss-Prot (`sp|`) headers.

```python
from Bio import SeqIO

input_file = "/home/amc0369/mimic_data/host/H_sapiens.fasta"
output_file = "/home/amc0369/mimic_data/host/H_sapiens_reviewed.fasta"

records = (
    record
    for record in SeqIO.parse(input_file, "fasta")
    if record.description.startswith("sp|")
)

count = SeqIO.write(records, output_file, "fasta")

print(f"Proteins written: {count}")
```

I ran the script using:

```bash
python ~/mimicDetector/filter_human_reviewed.py
```

The output was:

```text
Proteins written: 20416
```

I checked the new FASTA file:

```bash
grep -c "^>" ~/mimic_data/host/H_sapiens_reviewed.fasta
grep "^>" ~/mimic_data/host/H_sapiens_reviewed.fasta | head -n 3
```

The final human FASTA contained **20,416 reviewed proteins**.

---

## Checking the structure requirement

mimicDetector also requires protein structures for the pathogen and host because it uses POPScomp to calculate solvent accessibility.

I first checked how the structures were organized in the test dataset provided by mimicDetector:

```bash
head -n 3 ~/mimicDetector/test_data/host/host.fasta
ls ~/mimicDetector/test_data/host/structures | head
```

The FASTA uses the UniProt accession as the protein identifier. For example:

```text
>Q8NGX8
```

The corresponding structure is named:

```text
Q8NGX8.pdb.gz
```

This showed that the protein structure filenames need to correspond to the UniProt protein accessions.

---

## Checking how mimicDetector handles missing structures

I also checked the mimicDetector source code to understand what happens when a protein in the FASTA does not have a corresponding structure.

I located the QSASA filtering function in:

```text
mimicDetector/scripts/psychoscope.py
```

For host proteins, mimicDetector checks whether a POPS file corresponding to the protein is available.

If a structure is not available, the host QSASA value is assigned:

```python
h_region_avg = "NaN"
```

Later, mimicDetector removes candidates with missing QSASA values:

```python
qsasa_df_filtered = all_qsasa_df[
    (all_qsasa_df['h_avg'] != 'NaN') &
    (all_qsasa_df['q_avg'] != 'NaN')
]
```

For pathogen proteins, the QSASA calculation loops through the available pathogen structure files.

Therefore, proteins can be present in the FASTA even if a structure is not available. However, mimicry candidates without structural information for both the pathogen and host proteins will not pass the QSASA filtering step.

---

## Current datasets

At this point, the FASTA datasets are prepared:

| Dataset | Species | Proteins |
|---|---|---:|
| Pathogen | *Cryptosporidium parvum* Iowa II | 3,805 |
| Host | *Homo sapiens* reviewed proteins | 20,416 |
| Negative control | *Eimeria tenella* | 8,595 |

The directory structure is:

```text
mimic_data/
├── C_parvum/
│   ├── C_parvum.fasta
│   └── structures/
├── controls/
│   └── E_tenella.fasta
└── host/
    ├── H_sapiens.fasta
    ├── H_sapiens_reviewed.fasta
    └── structures/
```

## Next steps

The next steps are:

1. Obtain protein structures for *C. parvum*.
2. Obtain protein structures for the reviewed *H. sapiens* proteins.
3. Make sure the structure filenames correspond to the UniProt accessions.
4. Run mimicDetector using the real dataset.
5. Check and summarize the final mimicry candidates.
6. Perform the target-decoy FDR process required for the assignment.
