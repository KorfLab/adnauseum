import argparse
import gzip
import os
import sys


parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('--normalize', '-n', action='store_true')
arg = parser.parse_args()

data = {}
for path in arg.files:
	with gzip.open(path, 'rt') as fp:
		for line in fp:
			gene, val = line.split()
			if gene not in data: data[gene] = []
			data[gene].append(float(val))

if arg.normalize:
	totals = [0] * len(arg.files)
	for gene, vals in data.items():
		for i, val in enumerate(vals):
			totals[i] += val
	m = min(totals)
	scale = [val/m for val in totals]
	for gene, vals in data.items():
		for i, val in enumerate(vals):
			data[gene][i] /= scale[i]

for gene, vals in data.items():
	print(f'{gene:15s}', end='')
	for val in vals:
		print('\t', int(val), sep='', end='')
	print()