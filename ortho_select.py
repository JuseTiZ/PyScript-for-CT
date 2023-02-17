# -*- coding: utf-8 -*-
# ortho_select
# Verson: 1.0
# This is used to select orthogroup from output of orthofinder.

import argparse
import os
import time

def get_args():

	global args
	parser = argparse.ArgumentParser(description = "This is used to select orthogroup from output of orthofinder.")
	parser.add_argument("-l", "--least", type = int, help = "Least number of species concluding.")
	parser.add_argument("-b", "--big", default = 20, type = int, help = "Orthogroup considered as a big ortho when a species have more than xx sequences. default = 20")
	parser.add_argument("-f", "--file", type = str, help = "The path to the orthofinder og file.")
	parser.add_argument("-o", "--output", type = str, help = "The output path of dir.")
	args = parser.parse_args()
	return args


def mkdir():

	global outputDir
	outputDir = os.path.abspath(args.output)
	try:
		os.mkdir(f'{outputDir}/orthogroup_small')
		os.mkdir(f'{outputDir}/orthogroup_big')
	except:
		print("Please check the outputdir.")


def select_seq(seq):

	species_seq = {}
	with open(seq, "r") as s:
		for line in s:
			if line.startswith(">"):
				species = line.split("_")[0][1:]
				if species in species_seq.keys():
					species_seq[species] += 1
				else:
					species_seq[species] = 1
	if len(species_seq.keys()) < args.least:
		print(f"{seq}'s num of species is less than {args.least} and so abondoned.")
	else:
		if all(i <= args.big for i in species_seq.values()):
			os.system(f"cp {seq} {outputDir}/orthogroup_small/")
		else:
			os.system(f"cp {seq} {outputDir}/orthogroup_big/")


def run_select():

	inputdir = os.path.abspath(args.file)
	for i in os.listdir(inputdir):
		select_seq(f"{inputdir}/{i}")


def main():

	arges = get_args()
	mkdir()
	run_select()


if __name__ == "__main__":

	t0 = time.time()
	main()
	print(f'Total time used: {time.time() - t0}s\nFinished! See output at {outputDir}')