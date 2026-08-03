import argparse
import gzip
import os
import sys
import statistics
import math

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('--normalize', '-n', action='store_true')
parser.add_argument('--filter', '-f',  nargs=2, default=(0,0), type=int)
parser.add_argument('--ratio', action='store_true')
parser.add_argument('--entropy', action='store_true')
parser.add_argument('--pairwise', action='store_true')
arg = parser.parse_args()

if arg.ratio and arg.filter == (0,0): raise ZeroDivisionError("set filter to calculate variance ratio")

def calculate_distribution(vals):
	pseudocount = []
	for v in vals: pseudocount.append(v + 1)
	s = sum(pseudocount)
	distribution = []
	for pseudo in pseudocount: distribution.append(pseudo / s)
	return(distribution)

def entropy(vals):
	distribution = calculate_distribution(vals)
	h = 0
	for prob in distribution:
		h -= prob * math.log2(prob)
	return(h)

def mean_pairwise(vals):
	distribution = calculate_distribution(vals)
	distances = []
	for i in range(1, len(distribution) - 1):
		distances.append(abs(distribution[i] - distribution[i - 1]))
	return(statistics.mean(distances))

def variance_ratio(vals):
	return(statistics.variance(vals) / statistics.mean(vals))

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

filtered = {}
for gene, vals in data.items():
	min_count = arg.filter[0]
	min_n = arg.filter[1]
	n = 0
	for val in vals:
		if val >= min_count: n += 1
	if n >= min_n:
		filtered[gene] = vals

for gene, vals in filtered.items():
	print(f'{gene:15s}', end='')
	for val in vals:
		print('\t', int(val), sep='', end='')
	if arg.ratio:
		print('\t', round(variance_ratio(vals), ndigits=5), end='')
	if arg.entropy:
		print('\t', round(entropy(vals), ndigits=5), end='')
	if arg.pairwise:
		print('\t', round(mean_pairwise(vals), ndigits=5), end='')
	print()
