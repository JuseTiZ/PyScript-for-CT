import sys

fasta = open(sys.argv[1],"r")
output = open(sys.argv[2],"w")

id_seq = {}
gene_id = {}
gene_longest = {}

for line in fasta:
	if line.startswith(">"):
		contig_id = line.split()[0][1:]
		contig_gene = line.split("_i")[0][1:]
		if contig_gene in gene_id.keys():
			gene_id[contig_gene].append(contig_id)
		else:
			gene_id[contig_gene] = []
			gene_id[contig_gene].append(contig_id)
	else:
		if contig_id in id_seq.keys():
			id_seq[contig_id] += line
		else:
			id_seq[contig_id] = line


for gene in gene_id.keys():
	contigs = []
	for contig in gene_id[gene]:
		contigs.append(id_seq[contig])
	longest_contig = max(contigs, key = len)
	gene_longest[gene] = longest_contig

for gene in gene_longest.keys():
	output.write(">" + gene + '\n')
	output.write(gene_longest[gene])

print("Done")