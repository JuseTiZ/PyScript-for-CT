# generate_clade-defs.py
# Author: Juse

import sys
import os

header = "Clade Name\tClade Definition\tSection\tLetter\tComponents\tShow\tComments\n"
annofile = open(sys.argv[1], 'r')
outpfile = open(sys.argv[2], 'w')

group_spe = {}
all_spe = []

for line in annofile:

    spe = line.split()[0]
    if spe not in all_spe:
        all_spe.append(spe)
    group = line.split()[1]

    if group not in group_spe:
        group_spe[group] = [spe]
    else:
        group_spe[group].append(spe)

content = ''

for group, spes in group_spe.items():

    if len(spes) == 1:
        content += f'{group}\t{spes[0]}\tNone\t\t0\t\t\n'
    else:
        definition = '+'.join(spes)
        content += f'{group}\t{definition}\tNone\t\t1\t\t\n'

species = '+'.join(all_spe)
content += f'All\t{species}\tNone\t\t0\t\t\n'

outpfile.write(header)
outpfile.write(content)

print('Done!')