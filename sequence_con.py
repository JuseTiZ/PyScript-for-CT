# -*- coding: utf-8 -*-
# sequence_con
# Verson: 1.0
# Date: 2023.1.14
# This is used to concatenate sequences.


import os
import time
import re


IQpartition = '#nexus\nbegin sets;\n'
total_length = 0
total_spe_seq = {}


def add(ind, char):

	ind = ind + char + '\n'


total_num = len(os.listdir('./'))
compl_num = 0
for align in os.listdir('./'):


	with open(align, 'r') as ali:

		tmp_len = 0
		tmp_species = []
		for line in ali:
			if line.startswith('>') and line.strip() != '>':
				spe_name = line.split('@')[0]

				tmp_species.append(spe_name)

				if spe_name not in total_spe_seq.keys():
					total_spe_seq[spe_name] = '-'*total_length

			elif line.strip() == '>' or line.strip() == '':
				continue

			else:
				if len(tmp_species) == 1:
					tmp_len += len(line.strip())

				total_spe_seq[spe_name] += line.strip('>').strip()


		for spe in total_spe_seq.keys():
			if spe not in tmp_species:
				total_spe_seq[spe] += '-'*tmp_len

		charsetid = align.split('.')[0]
		IQpartition += f"\tcharset {charsetid}={total_length+1}-{total_length+tmp_len};\n"

		total_length += tmp_len
	compl_num += 1
	print(f"The progress is {compl_num}/{total_num}...")


os.mkdir("con_res")
with open("con_res/sequence_con.log", 'w') as log:

	log.write("Species\tLength\n")
	for spe in total_spe_seq.keys():

		if len(total_spe_seq[spe]) == total_length:
			log.write(f"{spe[1:]}\t{len(total_spe_seq[spe])}AA\t+\n")
		else:
			log.write(f"{spe[1:]}\t{len(total_spe_seq[spe])}AA\t-\n")

	print("See running log in con_res/sequence_con.log")

with open("con_res/concatenation_ortho.fasta", 'w') as f:

	for spe in total_spe_seq:
		f.write(spe + '\n' + total_spe_seq[spe] + '\n')

with open("con_res/IQ_partition.txt", 'w') as f:

	f.write(IQpartition)
	f.write("end;")


print('Finished, see output at con_res.')