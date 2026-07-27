import argparse
import os
import sys
import statistics

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
arg = parser.parse_args()

data = {}
n = 0
for path in arg.files:
	with open(path, 'rt') as fp:
		for line in fp:
			f = line.split()
			gene = f[0]
			ratio = f[-1]
			seen = 0
			if gene in data: seen += len(data[gene])
			if seen < n: continue
			if gene not in data: data[gene] = []
			data[gene].append(float(ratio))
	n += 1

for gene, ratios in data.items():
	if len(ratios) < len(arg.files): continue
	s = sum(ratios)
	print(gene, ratios, s)

