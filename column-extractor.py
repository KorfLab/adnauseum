import argparse
import gzip
import os
import sys

import wormnames

def readexcel(file, headers, genecol, l4col):
	pass

def readfile(file, ftype, headers, genecol, l4col, nn):
	if not file.endswith('.gz'): sys.exit(f'expecting gzip >>{file}<<')

	l4columns = l4col.split(';')          # human version
	col0 = [int(x) -1 for x in l4columns] # computer version
	gen0 = int(genecol) -1                # computer version
	sep = '\t' if ftype == 'TSV' else ','
	genes = []
	values = [ [] for _ in range(len(col0))]
	with gzip.open(file, 'rt') as fp:
		for _ in range(headers): line = next(fp)
		for line in fp:
			col = line.split(sep)
			genes.append(nn.pref_gene_name(col[gen0]))
			for i, val in enumerate(col0):
				try:
					f = float(col[val])
					values[i].append(float(col[val]))
				except:
					print(line)
					sys.exit(f'wtf >>{col[val]}<<')

	for exp in values: yield {k: v for k, v in zip(genes, exp)}


parser = argparse.ArgumentParser()
parser.add_argument('--faves', metavar='<file>', default='favorites.tsv',
	help='file of favorite GSEs [%(default)s]')
parser.add_argument('--genes', metavar='<file>', default='genes.tsv',
	help='file of gene names and aliases [%(default)s]')
parser.add_argument('--data', metavar='<dir>', default='raw',
	help='directory of GEO raw files [%(default)s]')
parser.add_argument('outdir', help='output directory')
arg = parser.parse_args()

nn = wormnames.NameNormalizer(arg.genes)

os.system(f'mkdir -p {arg.outdir}')
with open(arg.faves) as fp:
	header = next(fp)
	for line in fp:
		f = line.rstrip().split('\t')
		if len(f) == 8: f.pop()
		gse, ok, ftype, hl, gene, l4, file = f
		hl = int(hl)
		if ftype == 'Excel':
			#dataset = readexcel(f'{arg.data}/{file}', hl, gene, l4)
			continue
		else:
			dataset = readfile(f'{arg.data}/{file}', ftype, hl, gene, l4, nn)
		for i, data in enumerate(dataset):
			with open(f'{arg.outdir}/{gse}.{i}', 'w') as ofp:
				for gene, val in data.items():
					print(gene, val, sep='\t', file=ofp)
