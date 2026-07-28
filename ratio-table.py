import argparse
import os
import sys
import statistics
import numpy

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('--sum', '-s', action='store_true') 
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

rsum = {}
drop = []
for gene, ratios in data.items():
	if len(ratios) < len(arg.files):
		drop.append(gene)
		continue
	if arg.sum:
		rsum[gene] = sum(ratios)	

for gene in drop:
	data.pop(gene)

for gene, ratios in data.items():
	print(gene, end='')
	for ratio in ratios:
		print('\t', ratio, sep='', end='')
	if arg.sum:
		print('\t', rsum[gene], sep='', end='')
	print()

