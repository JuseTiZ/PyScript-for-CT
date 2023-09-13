import sys
import re
import os
import time

og_file = open(sys.argv[1],"r")
fa_dir = os.path.abspath(sys.argv[2])
sli_len = int(sys.argv[3])
gap_len = int(sys.argv[4])
cpu_num = sys.argv[5]
code_model = sys.argv[6]
###code model:
#1-Standard Code                         2-Vertebrate Mitochondrial Code
#3-Yeast Mitochondrial Code                      4-Mold, Protozoan, and Coelenterate Mitochondrial Code and the Mycoplasma/Spiroplasma Code
#5-Invertebrate Mitochondrial Code                       6-Ciliate, Dasycladacean and Hexamita Nuclear Code
#9-Echinoderm and Flatworm Mitochondrial Code                    10-Euplotid Nuclear Code
#11-Bacterial, Archaeal and Plant Plastid Code                   12-Alternative Yeast Nuclear Code
#13-Ascidian Mitochondrial Code                          14-Alternative Flatworm Mitochondrial Code
#16-Chlorophycean Mitochondrial Code                     21-Trematode Mitochondrial Code
#22-Scenedesmus obliquus Mitochondrial Code                      23-Thraustochytrium Mitochondrial Code
#24-Rhabdopleuridae Mitochondrial Code                   25-Candidate Division SR1 and Gracilibacteria Code
#26-Pachysolen tannophilus Nuclear Code                          27-Karyorelict Nuclear Code
#28-Condylostoma Nuclear Code                    29-Mesodinium Nuclear Code
#30-Peritrich Nuclear Code                       31-Blastocrithidia Nuclear Code
###

time_start = time.strftime('%Y%m%d-%H%M%S')
os.mkdir(f'SWworkdir_{time_start}')

ogall = []

for line in og_file:
	oglist = [line.split('\t')[0], line.split('\t')[1].strip()]
	ogall.append(oglist)


def readfa(fasta):

	id_seq = {}
	with open(fasta, 'r') as fa:
		for line in fa:
			if line.startswith(">"):
				idofseq = line.split()[0][1:]
				id_seq[idofseq] = ''
			else:
				id_seq[idofseq] += line.strip()
	return id_seq


def fa2axt(oglist, fasta, name):

	axtname = '-'.join(oglist)
	with open(f'{name}', 'w') as axt:
		axt.write(f"{axtname}\n")
		for spe in oglist:
			axt.write(fasta[spe] + '\n')


def sliding(fasta, oglist, sli_len, gap_len, dire):

	fa = readfa(fasta)
	fa_len = len(list(fa.values())[0])

	posi = 1
	while (posi-1)*gap_len + sli_len <= fa_len-1:
		os.mkdir(f"{dire}/posi_{posi}")
		ini_fa = {}
		sta_po = (posi-1)*gap_len
		end_po = sta_po + sli_len
		for spe in oglist:
			ini_fa[spe] = fa[spe][sta_po:end_po]
		fa2axt(oglist, ini_fa, f"{dire}/posi_{posi}/sliding_{posi}.axt")
		posi += 1
	if (posi-1)*3 + sli_len > fa_len-1:
		os.mkdir(f"{dire}/posi_{posi}")
		ini_fa = {}
		sta_po = (posi-1)*gap_len
		end_po = sta_po + sli_len
		for spe in oglist:
			ini_fa[spe] = fa[spe][sta_po:]
		fa2axt(oglist, ini_fa, f"{dire}/posi_{posi}/sliding_{posi}.axt")


for oglist in ogall:

	ogname = '-'.join(oglist)
	outputdir = f'SWworkdir_{time_start}/{ogname}'
	os.mkdir(outputdir)
	
	for gene in os.listdir(fa_dir):

		genename = gene.split('.')[0]
		os.mkdir(f'{outputdir}/{genename}')
		sliding(f'{fa_dir}/{gene}', oglist, sli_len, gap_len, f'{outputdir}/{genename}')

print("Sliding window completed...\nRunning Kaks_cal...")
	
os.system(f'for i in `ls SWworkdir_{time_start}/*/*/*/*axt`;do echo "KaKs -i $i -o $i.kaks -c {code_model}" >> sliding_window.command; done')
os.system(f'cat sliding_window.command | parallel --no-notice -j {cpu_num}')
os.system('rm sliding_window.command')
print("Kaks_cal done\nMerging result...")


def readkaks(kaksfile):

	with open(kaksfile, 'r') as kf:
		for line in kf:
			if line.startswith("Sequence"):
				continue
			dN = line.split('\t')[2]
			dS = line.split('\t')[3]
			omega = line.split('\t')[4]
	return {"dN": dN, "dS": dS, "omega": omega}


for oglist in ogall:

	ogname = '-'.join(oglist)
	outputdir = f'SWworkdir_{time_start}/{ogname}'
	sf_res = open(f'{outputdir}/sliding_window_{ogname}.res', 'w')
	sf_res.write('Gene\tPosition\tType\tvalue\n')

	for gene in os.listdir(outputdir):

		genesf = f'{outputdir}/{gene}'
		if os.path.isdir(genesf):
			total_num = len(os.listdir(genesf))
			
			for i in range(1, total_num + 1):

				kaksinfo = readkaks(f'{genesf}/posi_{i}/sliding_{i}.axt.kaks')
				for v in kaksinfo:
					sf_res.write(f'{gene}\t{i}\t{v}\t{kaksinfo[v]}\n')
		else:
			continue


print("Finished.")