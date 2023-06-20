# free-ratio-omega
# Author: Juse

import sys
import re
import os

spefile = sys.argv[1]
mlcfiledir = sys.argv[2]


species = []
with open(spefile, 'r') as f:
    for line in f:
        if line.strip() != '':
             species.append(line.strip())
species[:] = sorted(species)

with open('free-ratio.result', 'w') as op:

    head = '\t'.join(species)
    op.write(f'File\t{head}\n')

    for mlc in os.listdir(mlcfiledir):
        op.write(mlc+'\t')
        mlcpath = f'{mlcfiledir}/{mlc}'
        with open(mlcpath, 'r') as m:
            file_content = m.read()
            for spe in species:
                search = fr'{spe} #(\d+(?:\.\d+)?)'
                omega = re.search(search, file_content).group(1)
                op.write(omega + '\t')
        op.write('\n')

