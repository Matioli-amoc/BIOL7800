import sys
import yaml

sys.path.insert(0, "/home/amc0369/mimicDetector/scripts")

from psychoscope import MimicDetectionI

config_file = "/home/amc0369/mimic_results/Cparvum_human/config.yaml"

host_blast = (
    "/home/amc0369/mimic_results/Cparvum_human/C_parvum/"
    "C_parvum.Cparvum_human.12mers_b2_e01.12mers_blastp.out"
)

control_blast = (
    "/home/amc0369/mimic_results/Cparvum_human/C_parvum/"
    "C_parvum.E_tenella.12mers_blastp.out"
)

with open(config_file, "r") as f:
    config = yaml.safe_load(f)

config["patho_name"] = "C_parvum"

mdI = MimicDetectionI(**config)

print("Starting host-control filtering...")

filtered_file = mdI.filter_blast_bitscore(
    host_blast,
    control_blast,
    chunk=True
)

print("Filtering finished.")
print("Filtered file:", filtered_file)

print("Merging overlapping k-mers...")
merge_dict = mdI.merge_ranges(filtered_file)

print("Number of pathogen-host protein pairs:", len(merge_dict))

import csv

output_file = (
    "/home/amc0369/mimic_results/Cparvum_human/"
    "results_to_save/protein_pairs.tsv"
)

with open(output_file, "w", newline="") as out:
    writer = csv.writer(out, delimiter="\t")

    writer.writerow([
        "pathogen_protein",
        "host_protein",
        "pathogen_regions",
        "host_regions",
        "num_alignments"
    ])

    for pair, data in merge_dict.items():
        pathogen, host = pair.rsplit(".", 1)

        writer.writerow([
            pathogen,
            host,
            data["query"],
            data["host"],
            data["num_aln"]
        ])

print("Protein pairs saved to:", output_file)
