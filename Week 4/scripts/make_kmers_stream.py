from Bio import SeqIO

input_fasta = "/home/amc0369/mimic_data/C_parvum/C_parvum.fasta"
output_fasta = "/home/amc0369/mimic_results/Cparvum_human/C_parvum/C_parvum-12mers.fasta"

k = 12

with open(output_fasta, "w") as out:
    for record in SeqIO.parse(input_fasta, "fasta"):
        seq = str(record.seq)

        for i in range(len(seq) - k + 1):
            kmer = seq[i:i+k]
            out.write(f">{record.id}/{i}:{i+k}\n{kmer}\n")

print("Finished:", output_fasta)
