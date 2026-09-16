from Bio import SeqIO
import requests
import os
import time

fasta_file = "/home/amc0369/mimic_data/C_parvum/C_parvum.fasta"
output_dir = "/home/amc0369/mimic_data/C_parvum/structures"

os.makedirs(output_dir, exist_ok=True)

available = 0
missing = 0
failed = 0

missing_accessions = []
failed_accessions = []

for i, record in enumerate(SeqIO.parse(fasta_file, "fasta"), start=1):

    # UniProt FASTA header:
    # tr|A3FPL9|A3FPL9_CRYPI
    accession = record.id.split("|")[1]

    output_file = os.path.join(output_dir, f"{accession}.pdb")

    # Skip structures that were already downloaded
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        print(f"[{i}] {accession}: already downloaded")
        available += 1
        continue

    api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{accession}"

    try:
        response = requests.get(api_url, timeout=30)

        if response.status_code == 404:
            print(f"[{i}] {accession}: no AlphaFold model")
            missing += 1
            missing_accessions.append(accession)
            continue

        response.raise_for_status()

        data = response.json()

        if not data:
            print(f"[{i}] {accession}: no AlphaFold model")
            missing += 1
            missing_accessions.append(accession)
            continue

        pdb_url = data[0]["pdbUrl"]

        pdb_response = requests.get(pdb_url, timeout=60)
        pdb_response.raise_for_status()

        with open(output_file, "wb") as f:
            f.write(pdb_response.content)

        print(f"[{i}] {accession}: downloaded")
        available += 1

    except Exception as e:
        print(f"[{i}] {accession}: ERROR - {e}")
        failed += 1
        failed_accessions.append(accession)

    time.sleep(0.1)

with open(os.path.join(output_dir, "missing_alphafold.txt"), "w") as f:
    for accession in missing_accessions:
        f.write(accession + "\n")

with open(os.path.join(output_dir, "failed_downloads.txt"), "w") as f:
    for accession in failed_accessions:
        f.write(accession + "\n")


print("\nFinished")
print(f"Structures downloaded/available: {available}")
print(f"No AlphaFold model: {missing}")
print(f"Failed requests: {failed}")
