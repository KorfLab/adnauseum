import glob
import json
import re
import statistics
import sys

import adnauseum

# read all gene expression data
data = {}
for file in glob.glob('proc/*'):
	m = re.match(r'proc/(GSE\d+)\.(\d+)', file)
	gse = m.group(1)
	rep = m.group(2)
	if gse not in data: data[gse] = {}
	data[gse][rep] = adnauseum.read_expression_file(file)

# normliaze counts (downward) among replicates
for gse, d in data.items():
	if len(d) < 2: continue
	total = {}
	for rep in d:
		total[rep] = sum([x for g, x in d[rep].items()])
	low = min(total.values())
	norm = {}
	for rep in d: norm[rep] = total[rep] / low
	for rep in d:
		for g, x in d[rep].items():
			d[rep][g] = x/norm[rep]

# which is the most reliable gene?
qc = {}
for gse, d in data.items():
	gene_count = {}
	if len(d) < 6: continue # testing
	for rep in d:
		for g, x in d[rep].items():
			if g not in gene_count: gene_count[g] = []
			gene_count[g].append(x)
	for g, a in gene_count.items():
		if g not in qc: qc[g] = {}
		if gse not in qc[g]: qc[g][gse] = a

kill = [gene for gene in qc if len(qc[gene]) != 3]
for gene in kill: del qc[gene]
print(json.dumps(qc, indent=2))