# -*- coding: utf-8 -*-
# OTU_replace
# Version: 1.2
# This is used to replace OTU_ to OTU@ in fasta or treefile.
# Usage: python3 OTU_replace.py dir species_list

import sys
import os
import time
import re

def help_info():
    print("This is used to replace OTU_ to OTU@ in fasta or treefile.\n\tUsage: python3 OTU_replace.py dir species_list\n\tThe file can be identified includes .fa .fasta .fas .tre .treefile")

def get_args():
    args = sys.argv[1:]
    if len(args) == 0:
        help_info()
        sys.exit(1)
    try:
        inputfiledir = os.path.abspath(args[0])
        species_list = os.path.abspath(args[1])
        return inputfiledir, species_list
    except Exception as e:
        print(f"Error: {e}")
        print("Please check the dirpath.")
        sys.exit(1)

def spe_list_get(species_list):
    spe_list = []
    try:
        with open(species_list, 'r') as s:
            for line in s:
                spe_list.append(line.strip())
        return spe_list
    except FileNotFoundError:
        print("Species list file not found.")
        sys.exit(1)

def run_replace(dir_path, spe_list):
    pattern = re.compile(r'(' + '|'.join(spe_list) + r')_')
    for filename in os.listdir(dir_path):
        if filename.endswith(('.fa', '.fasta', '.fas', '.tre', '.treefile')):
            filepath = os.path.join(dir_path, filename)
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                new_content = pattern.sub(r'\1@', content)
                with open(filepath, 'w') as f:
                    f.write(new_content)
            except IOError as e:
                print(f"Error processing file {filename}: {e}")

def main():
    inputfiledir, species_list = get_args()
    spe_list = spe_list_get(species_list)
    run_replace(inputfiledir, spe_list)

if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f'Total time used: {time.time() - t0}s\nFinished!')
