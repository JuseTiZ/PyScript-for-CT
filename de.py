import sys

raw_file = open(sys.argv[1],"r")
out_up_file = open(sys.argv[2],"w")
out_down_file = open(sys.argv[3],"w")

for line in raw_file:
	string = line.split("\t")
	if string[0] == 'sampleA':
		continue
	if len(string) == 11:
		if abs(float(string[6])) >= 2.0 and float(string[-1]) <= 0.05:
			if float(string[6]) > 0:
				out_up_file.write(string[0] + '\n')
			else:
				out_down_file.write(string[0] + '\n')
	else:
		if abs(float(string[3])) >= 2.0 and float(string[-1]) <= 0.05:
			if float(string[3]) > 0:
				out_up_file.write(string[0] + '\n')
			else:
				out_down_file.write(string[0] + '\n')