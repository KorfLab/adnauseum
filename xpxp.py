import json
import math
import sys
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.cluster.hierarchy import linkage, dendrogram
import antbox

def screen_name(d, wbgene):
	for name in d[wbgene]:
		if '-' in name: return name
	for name in d[wbgene]:
		if '.' in name: return name
	return wbgene

def count_type(d):
	ints = 0
	floats = 0
	for gene, val in d.items():
		if math.isclose(0, val % 1): ints += 1
		else: floats += 1
	if   ints == len(d): return int
	elif floats > 0.99 * len(d): return float
	else: return None

def read_expression(file):
	t = {}
	with open(file) as fp:
		for line in fp:
			gene, val = line.split()
			t[gene] = float(val)
	return t

# get gene lengths and synonyms (hard-coded)
gene_len = {}
with open('worm_genes.txt') as fp:
	header = next(fp)
	for line in fp:
		gene, size = line.split()
		gene_len[gene] = int(size)
gene_names = {}
with open('worm_genes.json') as fp:
	gene_names = json.load(fp) # might use it later

# read all of the gene expression files, normalizing as needed
all_exp = {}
for file in sys.argv[1:]:
	expression = read_expression(file)
	ct = count_type(expression)
	if ct is None:
		print('skipping file with mixed ints, floats', file)
		continue # wtf, why do these even exist?
	elif ct == float:
		all_exp[file] = expression
	elif ct == int: # raw counts --> normalize by gene length
		for gene in expression:
			expression[gene] /= gene_len[gene]
		all_exp[file] = expression

# find genes that are in all files
fave_gene = set()
for gene in all_exp[list(all_exp.keys())[0]]:
	missing = False
	for file in all_exp:
		if gene not in all_exp[file]:
			missing = True
			break
	if missing: continue
	fave_gene.add(gene)
print('found', len(fave_gene), 'genes across all files')

# create fav expression subset
fav_exp = {}
for file in all_exp:
	exp = {}
	for gene, val in all_exp[file].items():
		if gene in fave_gene:
			exp[gene] = val
	exp = dict(sorted(exp.items(), key=lambda x: x[1], reverse=True))
	fav_exp[file] = exp

# turn expressions into probability distributions
for file in fav_exp:
	total = sum(fav_exp[file].values())
	for gene in fav_exp[file]:
		fav_exp[file][gene] /= total

# save files for debugging
for file in fav_exp:
	out = f'{file}.debug'
	with open(out, 'w') as fp:
		for gene, val in fav_exp[file].items():
			print(screen_name(gene_names, gene), val, file=fp)

#sys.exit()

funcs = antbox.dkl, antbox.dtc, antbox.dtx, antbox.dty
fnames = 'dkl', 'dtc', 'dtx', 'dty'

for func, fname in zip(funcs, fnames):

	# create pairwise distances
	files = list(fav_exp.keys())
	condmat = []
	for i in range(len(files)):
		for j in range(i + 1, len(files)):
			condmat.append(func(fav_exp[files[i]], fav_exp[files[j]]))
	
	# cluster and plot
	labels = []
	for file in files:
		f = file.split('/')
		labels.append(f[-1])
	
	plt.figure(figsize=(12,8))
	plt.title(f'RNA-Seq {fname} Clustering')
	Z = linkage(condmat, method='weighted')
	dn = dendrogram(Z, labels=labels, orientation='left')
	plt.savefig(f'{fname}.png')
	plt.close()
