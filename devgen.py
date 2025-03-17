import random

gene_size = (1, 2,)              # to debug length normalizing
gene_expr = (1, 10)        # to debug overweighting
read_count = (10, 20, 40, 80) # to debug raw vs. normalized
methods = ('raw', 'fpkm', 'cpm')


for rc in read_count:
	gid = 0
	sampler = []
	for gs in gene_size:
		for gx in gene_expr:
			sampler.extend([gid] * gs * gx)
			gid += 1
	print(sampler)
	reads = random.choices(sampler, k=rc)
	print(reads)
	
			
		


"""
RAW   int     total counts per gene, not normalized in any way
CPM   float   counts per gene per million reads, normalizes sequencing depth
FPKM  float   normalizes for gene length and sequencing depth
MoR   float   median of (ratio of expression levels per gene)
"""