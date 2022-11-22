import argparse

parser = argparse.ArgumentParser(description = "Modify a fasta file's id name.")
parser.add_argument("-m", "--mod", type = str, choices = ['pre','suf','sim'], help = "What do u what to do about id? 'pre' means add a prefix. 'suf' means add a suffix. 'sim' means simplify id.")
parser.add_argument("-f", "--file", type = str, help = "The path to the fasta file.")
parser.add_argument("-s", "--string", type = str, help = "The prefix or suffix you want to add, use with --mod.")
parser.add_argument("-o", "--output", type = str, help = "The output file.")
args = parser.parse_args()

file = args.file
with open(args.output,'w') as output:
    with open(file) as fasta:
        if args.mod == 'sim':
            for line in fasta:
                if line.startswith(">"):
                    seqid = line.split()[0]
                    output.write(seqid + '\n')
                    continue
                output.write(line)
        if args.mod == 'pre':
            prefix = args.string
            for line in fasta:
                if line.startswith(">"):
                    seqid = line.split()[0][1:]
                    new_seqid = ">" + prefix + seqid
                    output.write(new_seqid + '\n')
                    continue
                output.write(line)
        if args.mod == 'suf':
            suffix = args.string
            for line in fasta:
                if line.startswith(">"):
                    seqid = line.split()[0][1:]
                    new_seqid = ">" + seqid + suffix
                    output.write(new_seqid + '\n')
                    continue
                output.write(line)

print("Done!")