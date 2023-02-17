# -*- coding: utf-8 -*-
# trim_filter
# Verson: 1.0
# This is used to filter alignment to build genetree.

import re
import argparse
import os

def get_args():

	global args
	parser = argparse.ArgumentParser(description = "This is used to filter alignment to build genetree, run in the directory.")
	parser.add_argument("-s", "--seq", default = 80, type = int, help = "Deletes original seqs shorter than this length, default = 80.")
	parser.add_argument("-a", "--align", default = 80, type = int, help = "Minimum length of a trimmed alignment in amino acids, default = 80.")
	parser.add_argument("-t", "--tax", type = int, help = "Specify minimum number of taxa, namely Minimum number of OTUs to keep an OG. Required!")
	args = parser.parse_args()
	return args


def remove_n(string, char):

	return len(re.sub(char, '', string))


def filter():

	min_tax_num = args.tax
	min_len_file = args.seq
	min_len_alig = args.align
	for trims in os.listdir("./"):
		os.system(f'echo "Processing file {trims}......" >> trim_filter.log')
		# 得到该比对的各个信息
		id_seq = {}
		with open(trims, 'r') as f:
			for line in f:
				if line.startswith(">"):
					seq_name = line.strip()
				else:
					# 制作映射字典
					try:
						id_seq[seq_name] += line
					except:
						id_seq[seq_name] = line

		os.system(f'rm {trims}')
		# 判断序列原始长度是否达标
		if remove_n(list(id_seq.values())[0], '\n') < min_len_file:
			os.system(f'echo "{trims} length is less than {min_len_file}AA and be removed." >> trim_filter.log')
			continue

		os.system(f'echo "{trims} length is enough for next filter." >> trim_filter.log')
		# 筛选合格序列
		newid_seq = {}
		for i in id_seq.keys():
			if remove_n(id_seq[i], '[-\n]') >= min_len_alig:
				newid_seq[i] = id_seq[i]
			else:
				os.system(f'echo "{trims} {i[1:]} is shorter than {min_len_alig}AA and be removed." >> trim_filter.log')
		# 判断物种数量是否合格
		species_list = []
		for i in newid_seq.keys():
			species = i.split('@')[0][1:]
			# 统计物种名单
			if species not in species_list:
				species_list.append(species)
		if len(species_list) < min_tax_num:
			os.system(f'echo "{trims} tax is less than {min_tax_num} and be removed." >> trim_filter.log')
			continue
		# 重新再建比对
		with open(trims, 'w') as f:
			for i in newid_seq.keys():
				f.write(i + '\n')
				f.write(newid_seq[i])
		os.system(f'echo "{trims} has been saved and filtered." >> trim_filter.log')


def main():

	get_args()
	try:
		filter()
	except:
		print("Please check the position you are.")


if __name__ == "__main__":

	print("Running...")
	main()
	print(f'Finished! See running log in trim_filter.log')