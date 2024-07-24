# -*- coding: utf-8 -*-
# ortho_select
# Version: 1.0
# This is used to select orthogroup from output of orthofinder.

import argparse
import os
import time

def get_args():
    parser = argparse.ArgumentParser(description="This is used to select orthogroup from output of orthofinder.")
    parser.add_argument("-l", "--least", type=int, required=True, help="Least number of species concluding.")
    parser.add_argument("-b", "--big", default=20, type=int, help="Orthogroup considered as a big ortho when a species have more than xx sequences. default = 20")
    parser.add_argument("-f", "--file", type=str, required=True, help="The path to the orthofinder og file.")
    parser.add_argument("-o", "--output", type=str, required=True, help="The output path of dir.")
    args = parser.parse_args()
    return args

def mkdir(outputdir):
    try:
        os.mkdir(os.path.join(outputdir, 'orthogroup_small'))
        os.mkdir(os.path.join(outputdir, 'orthogroup_big'))
    except OSError as e:
        print(f"Error creating directories: {e}")
        print("Please check the outputdir.")

def select_seq(seq, outputdir, least, big):
    species_seq = {}
    with open(seq, "r") as s:
        for line in s:
            if line.startswith(">"):
                species = line.split("_")[0][1:]
                if species in species_seq:
                    species_seq[species] += 1
                else:
                    species_seq[species] = 1
    if len(species_seq) < least:
        print(f"{seq}'s num of species is less than {least} and so abandoned.")
    else:
        if all(i <= big for i in species_seq.values()):
            os.system(f"cp {seq} {os.path.join(outputdir, 'orthogroup_small')}/")
        else:
            os.system(f"cp {seq} {os.path.join(outputdir, 'orthogroup_big')}/")

def run_select(inputdir, outputdir, least, big):
    inputdir = os.path.abspath(inputdir)
    for i in os.listdir(inputdir):
        select_seq(os.path.join(inputdir, i), outputdir, least, big)

def main():
    args = get_args()
    outputdir = os.path.abspath(args.output)
    mkdir(outputdir)
    run_select(args.file, outputdir, args.least, args.big)

if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f'Total time used: {time.time() - t0}s\nFinished!')
