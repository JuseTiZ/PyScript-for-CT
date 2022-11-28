import sys
raw_file = open(sys.argv[1], "r")
out_file = open(sys.argv[2], "w")

for line in raw_file:
	string = line.split("\t")
	for goid in string[1].strip().split(","):
		output = string[0] + '\t' + goid + '\n'
		out_file.write(output)