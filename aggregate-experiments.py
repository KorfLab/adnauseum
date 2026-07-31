import argparse
import os
import sys
import statistics
import numpy

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('--header', action='store_true')
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

drop = []
for gene, ratios in data.items():
	if len(ratios) < len(arg.files):
		drop.append(gene)
		continue

for gene in drop:
	data.pop(gene)

if arg.header:
	print('gene', end='')
	for path in arg.files:
		(head, tail) = os.path.split(path)
		print('\t', tail.replace('.txt', ''), sep='', end='')
	print()

for gene, ratios in data.items():
	print(gene, end='')
	for ratio in ratios:
		print('\t', ratio, sep='', end='')
	print()
