# -*- coding: utf-8 -*-
# sequence_con
# Verson: 1.1
# Date: 2023.1.14
# This script concatenates sequences and generates an IQ-TREE2 partition file.

import os

IQpartition = '#nexus\nbegin sets;\n'
total_length = 0
total_spe_seq = {}


total_num = len(os.listdir('./'))
compl_num = 0
aligns = os.listdir('./')
aligns.sort()

#对当前文件夹里所有文件逐个读取
for align in aligns:

	with open(align, 'r') as ali:

		#初始化当前文件信息
		tmp_len = 0
		tmp_species = []
		for line in ali:
			if line.startswith('>') and line.strip() != '>':
                #如果物种名以下划线分割则替换为_
				spe_name = line.split('@')[0].strip()

				tmp_species.append(spe_name)

				#到当前比对才出现的物种之前的序列都以gap表示
				if spe_name not in total_spe_seq.keys():
					total_spe_seq[spe_name] = '-'*total_length

			#跳过空序列
			elif line.strip() == '>' or line.strip() == '':
				continue

			#将第一个序列的长度读取以作为该多序列比对的长度
			else:
				if len(tmp_species) == 1:
					tmp_len += len(line.strip())

				total_spe_seq[spe_name] += line.strip('>').strip()

		#对不在该文件出现但在之前出现过的物种以gap作为其序列进行补充
		for spe in total_spe_seq.keys():
			if spe not in tmp_species:
				total_spe_seq[spe] += '-'*tmp_len
		#添加分区信息
		charsetid = align.split('.')[0]
		IQpartition += f"\tcharset {charsetid}={total_length+1}-{total_length+tmp_len};\n"

		total_length += tmp_len
	compl_num += 1
	print(f"The progress is {compl_num}/{total_num}...")


os.mkdir("con_res")
#生成物种log
with open("con_res/sequence_con.log", 'w') as log:

	log.write("Species\tLength\n")
	for spe in total_spe_seq.keys():

		if len(total_spe_seq[spe]) == total_length:
			log.write(f"{spe[1:]}\t{len(total_spe_seq[spe])}AA\t+\n")
		else:
			log.write(f"{spe[1:]}\t{len(total_spe_seq[spe])}AA\t-\n")

	print("See running log in con_res/sequence_con.log")
#生成串联文件
with open("con_res/concatenation_ortho.fasta", 'w') as f:

	for spe in total_spe_seq:
		f.write(spe + '\n' + total_spe_seq[spe] + '\n')
#生成分区文件
with open("con_res/IQ_partition.txt", 'w') as f:

	f.write(IQpartition)
	f.write("end;")


print('Finished, see output at con_res.')
