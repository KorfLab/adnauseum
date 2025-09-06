import gzip
import json
from statistics import mean, stdev
import sys

if len(sys.argv) != 2: sys.exit('usage: gg.py <json>')

with gzip.open(sys.argv[1], 'rt') as fp:
	data = json.load(fp)

# normalize down (again) across samples
gse_counts = {}
for gene, gse in data.items():
	for gseid, exps in gse.items():
		if gseid not in gse_counts: gse_counts[gseid] = 0
		for exp in exps: gse_counts[gseid] += exp
low = min(gse_counts.values())
gse_norm = {}
for gseid, x in gse_counts.items():
	gse_norm[gseid] = x / low

# something
for gene, gse in data.items():
	fits = []
	for gseid, exps in gse.items():
		m = mean(exps)
		exp = m**0.5      # expected std dev
		obs = stdev(exps) # observed std dev
		fit = obs / exp if exp != 0 else 0
		fit /= gse_norm[gseid]
		fits.append(fit)
	print(gene, end='')
	for fit in fits: print(f'\t{fit:.1f}', end='')
	print()


# are there RNA-seq PCR blooms that randomly pick a gene an overrepresent it?
# some RNA preps appear more variable than others
# what exactly is the math of limmavoom?
# 114951 much better behaved than 116367 115096