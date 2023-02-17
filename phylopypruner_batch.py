# -*- coding: utf-8 -*-
# phylopypruner_batch
# Verson: 1.0
# This is used to call phylopypruner and run for batch to avoid recursionerror.
# Usage: python3 phylopypruner_batch.py numberofbatch inputdir outputdir.

import sys
import os
import time

def help_info():

	print("This is used to call phylopypruner and run for batch to avoid recursionerror.\n\tUsage: python phylopypruner_batch.py numberofbatch cpunum mintax inputdir outputdir." + 
		"\n\tThe parameter can be changed for private use.\n\tWhen dividing batches, it is normal to see ls write error, so don't worry.")

def getArgs():

	global batchnum
	global cpunum
	global mintax
	global inputDir
	global outputDir


	args = sys.argv[1:]
	if len(args) == 0:
		help_info()
		sys.exit()
	try:
		batchnum = args[0]
		cpunum = args[1]
		mintax = args[2]
		inputDir = os.path.abspath(args[3])
		outputDir = os.path.abspath(args[4])
		print(f"The path of inputDir is {inputDir}\nThe outputpath is set to {outputDir}\nThe number of batch is set to {batchnum}")
	except:
		print("Please check your command.")
		help_info()
		sys.exit()

def mkdir():

	try:
		os.mkdir(f'{outputDir}/phylopypruner_batch')
		os.mkdir(f'{outputDir}/phylopypruner_batch/batchfile')
		os.mkdir(f'{outputDir}/phylopypruner_batch/alignfile')
	except:
		print("It looks like the command has already been run, phylopypruner_batch.py will continue to check if omission exists.")


def cpinput():

	global a
	os.mkdir(f'{outputDir}/phylopypruner_batch/tmp_sequence_tree')
	dir_tmp = f'{outputDir}/phylopypruner_batch/tmp_sequence_tree'
	batchdir = f'{outputDir}/phylopypruner_batch/batchfile'
	os.system(f'for i in `ls {inputDir}/*treefile`;' + ' do id=${i%%.treefile};' + f' cp $i {dir_tmp}; cp $id.fasta {dir_tmp}; done')
	a = 0
	while len(os.listdir(dir_tmp)) != 0:
		a += 1
		os.mkdir(f'{batchdir}/batch_{a}')
		os.system(f'for i in `ls -r {dir_tmp}/*treefile | head -n {batchnum}`;' + ' do id=${i%%.treefile};' + f' mv $i {batchdir}/batch_{a}; mv $id.fasta {batchdir}/batch_{a}; done')
	print(f"It has been divided into {a} batches.")
	os.rmdir(dir_tmp)


def runphylo():

	print("Starting to run phylopypruner for each patch.")
	batchdir = f'{outputDir}/phylopypruner_batch/batchfile'
	b = 0
	for batch in os.listdir(batchdir):
		print(f"Processing with {batch}...")
		os.system(f"sed -i 's/@/_/g' {batchdir}/{batch}/*")
		os.system(f'python3 /data/zongjin/py/OTU_replace.py {batchdir}/{batch} /data/zongjin/data/analysis2/orp_pep/OrthoFinder/Results_Nov28/species.txt')
		os.system(f'phylopypruner --dir {batchdir}/{batch} --min-len 100 --trim-lb 5 --threads {cpunum} \
--min-support 0.75 --prune MI --min-taxa {mintax} \
--trim-freq-paralogs 4 --trim-divergent 1.25 \
--jackknife --min-pdist 1e-8  > {batchdir}/{batch}/{batch}.phylo.log 2>&1')
		b += 1
		print(f"The progress is {b}/{a}...")


def cpoutput():

	os.system(f'cp {outputDir}/phylopypruner_batch/batchfile/*/phylopypruner_output/output_alignments/*fasta {outputDir}/phylopypruner_batch/alignfile')


def main():

	getArgs()
	mkdir()
	cpinput()
	runphylo()
	cpoutput()

if __name__ == "__main__":

	t0 = time.time()
	main()
	print(f'Total time used: {time.time() - t0}s\nFinished! See output at {outputDir}/phylopypruner_batch')