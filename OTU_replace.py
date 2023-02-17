# -*- coding: utf-8 -*-
# OTU_replace
# Verson: 1.1
# This is used to replace OTU_ to OTU@ in fasta or treefile.
# Usage: python3 OTU_replace.py dir species_list

import sys
import os
import time


def help_info():

	print("This is used to replace OTU_ to OTU@ in fasta or treefile.\n\tUsage: python3 OTU_replace.py dir species_list\n\tThe file can be indentified includes .fa .fasta .fas .tre .treefile")

def getArgs():

	global inputfiledir
	global species_list

	args = sys.argv[1:]
	if len(args) == 0:
		help_info()
		sys.exit()
	try:
		inputfiledir = os.path.abspath(args[0])
		species_list = os.path.abspath(args[1])
	except:
		print("Please check the dirpath.")


def spe_list_get():

	global spe_list
	spe_list = []
	with open(species_list, 'r') as s:
		for line in s:
			spe_list.append(line.strip())


def run_replace(dir_path):

	for spe in spe_list:
		os.system(f"sed -i 's/{spe}_/{spe}@/g' *.fa*")
		os.system(f"sed -i 's/{spe}_/{spe}@/g' *.tre*")

def main():

	getArgs()
	spe_list_get()
	run_replace(inputfiledir)


if __name__ == "__main__":

	t0 = time.time()
	main()
	print(f'Total time used: {time.time() - t0}s\nFinished!')