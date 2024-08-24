import argparse

def process_go_annotations(raw_file, out_file):
    with open(raw_file, "r") as infile, open(out_file, "w") as outfile:
        for line in infile:
            string = line.split("\t")
            gene = string[0]
            go_terms = string[1].strip().split(",")
            for goid in go_terms:
                output = gene + '\t' + goid + '\n'
                outfile.write(output)

def main():
    parser = argparse.ArgumentParser(description="Process a Trinotate output GO annotation file to create a one-to-one relationship between genes and GO terms.")
    
    parser.add_argument('-r', '--raw_file', type=str, help='Path to the Trinotate output raw GO annotation file.')
    parser.add_argument('-o', '--out_file', type=str, help='Path to the output file where each gene and GO term will have a one-to-one relationship.')
    
    args = parser.parse_args()
    
    process_go_annotations(args.raw_file, args.out_file)

if __name__ == "__main__":
    main()