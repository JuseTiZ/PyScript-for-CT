# -*- coding: utf-8 -*-
# free-ratio_calcu
# Author: Juse

import sys
import os

args = sys.argv[1:]
if len(args) == 0:
	print("Usage: python free-ratio_calcu.py treefile seqdir outputDir")
	sys.exit()
try:
	treefile = os.path.abspath(args[0])
	seqdir = os.path.abspath(args[1])
	outputDir = os.path.abspath(args[2])
except:
	print("Please check your command.")
	sys.exit()

paml_seq = []
for paml in os.listdir(seqdir):
	paml_seq.append(f"{seqdir}/{paml}")

for seqid in paml_seq:
	outid = f"{seqid.split('/')[-1]}.mlc"
	with open("codeml.ctl", "w") as f:
		f.write(f'''
seqfile = {seqid}
treefile = {treefile}
outfile = {outputDir}/{outid}

noisy = 9
verbose = 1
runmode = 0

seqtype = 1
CodonFreq = 2
model = 1
NSsites = 0
icode = 0
Mgene = 0

fix_kappa = 0
kappa = 2

fix_omega = 0
omega = 1

fix_alpha = 1
ncatG = 8

getSE = 0
RateAncestor = 0
Small_Diff = .5e-6
cleandata = 1
			''')
	os.system("codeml")