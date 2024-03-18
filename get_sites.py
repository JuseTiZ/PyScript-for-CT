from Bio import SeqIO
import os
import argparse
import gzip
import subprocess

def get_args():
    parser = argparse.ArgumentParser(description="Use to extract AT/CG(nonCpG) & CpG sites.")
    
    parser.add_argument("-g", "--genome", required=True, help="The path of genome sequence file.")
    parser.add_argument("-c", "--chr", required=True, help="The target chromosome to extract.")
    parser.add_argument("--onlycpg", action="store_true", help="Only extract CpG sites.")
    parser.add_argument("--merge", action="store_true", help="Use bedtools to merge bed files.")
    parser.add_argument("--gzip", action="store_true", help="Use gzip to compress output.")
    parser.add_argument("-n", "--name", help="The name of output file.")
    parser.add_argument("-p", "--path", help="The path of output file.", default='./')
    
    args = parser.parse_args()
    if not args.name:
        args.name = os.path.splitext(os.path.basename(args.genome))[0]
    
    return args

def process_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error when executing command: {command}\n{result.stderr.decode()}")

def main():
    args = get_args()

    with gzip.open(args.genome, "rt") if args.genome.endswith(".gz") else open(args.genome, "r") as genome_file:
        chr_num = "chr" + args.chr.replace("chr", "")
        cpg_bed_name = os.path.join(args.path, f"{args.name}_{chr_num}_CpGsites.bed.tmp")
        atcg_bed_name = os.path.join(args.path, f"{args.name}_{chr_num}_ATnonCpGsites.bed.tmp")
        
        with open(cpg_bed_name, "w") as cpg_bed, open(atcg_bed_name, "w") as atcg_bed:
            for record in SeqIO.parse(genome_file, "fasta"):
                if record.id != args.chr:
                    continue
                seq = str(record.seq).upper()

                for i, nuc in enumerate(seq):
                    if nuc == "N":
                        continue
                    if nuc in ["A", "T"] and not args.onlycpg:
                        atcg_bed.write(f"{chr_num}\t{i}\t{i+1}\n")
                    elif nuc in ["C", "G"]:
                        if (nuc == "C" and i + 1 < len(seq) and seq[i + 1] == "G") or (nuc == "G" and i > 0 and seq[i - 1] == "C"):
                            cpg_bed.write(f"{chr_num}\t{i}\t{i+1}\n")
                        elif not args.onlycpg:
                            atcg_bed.write(f"{chr_num}\t{i}\t{i+1}\n")
        
        for bed_file in [cpg_bed_name, atcg_bed_name] if not args.onlycpg else [cpg_bed_name]:
            outfile = bed_file.replace(".tmp", "")
            if args.merge:
                command = f"bedtools merge -i {bed_file} > {outfile} && rm {bed_file}"
            else:
                command = f"mv {bed_file} {outfile}"
            process_command(command)
            if args.gzip:
                process_command(f"gzip -f {outfile}")
        
        if args.onlycpg:
            os.remove(atcg_bed_name)

if __name__ == "__main__":
    main()
