# ref2spename.py
# Author: Juse with ChatGPT

from Bio import SeqIO
import re
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

def modify_header(record):

    new_id = record.description.replace(' ', '_')
    match = re.search(r".*\[([^]]*)\]", new_id)

    if match:
        species = match.group(1).replace(' ', '_')
        rest = new_id[:match.start(1)-1]
        new_id = species + '@' + rest

    record.id = new_id.strip('_')
    record.description = ""
    return record

def process_fasta_file(input_file, output_file):

    records = SeqIO.parse(input_file, "fasta")
    new_records = (modify_header(record) for record in records)
    SeqIO.write(new_records, output_file, "fasta")

process_fasta_file(input_file, output_file)
