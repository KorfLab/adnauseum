import math
import random
import sys

def read_expression(file):
	t = {}
	with open(file) as fp:
		for line in fp:
			gene, val = line.split()
			t[gene] = float(val)
	return t

def make_histograms(d1, d2, pseudo=0, skip_missing=True):
	p = {}
	q = {}
	for k in d1.keys() | d2.keys():
		if k in d1 and k in d2:
			p[k] = d1[k] + pseudo
			q[k] = d2[k] + pseudo
		else:
			if skip_missing: continue
			p[k] = d1[k] + pseudo if k in d1 else pseudo
			q[k] = d2[k] + pseudo if k in d2 else pseudo
	ptotal = sum(p.values())
	qtotal = sum(q.values())
	for k in p:
		p[k] /= ptotal
		q[k] /= qtotal
	return p, q

def dkl(d1, d2, pseudo=0, skip_missing=True, check_values=True):
	"""K-L divergence between dictionaries"""
	if check_values:
		p, q = make_histograms(d1, d2, pseudo=pseudo, skip_missing=skip_missing)
	else:
		p, q = d1, d2

	h = 0
	for k in p.keys():
		h += p[k] * math.log2(p[k]/q[k])
	
	return h

def dtc(d1, d2, pseudo=0, skip_missing=True, make_histogram=True):
	if make_histogram:
		p, q = make_histograms(d1, d2, pseudo=pseudo, skip_missing=skip_missing)
	else:
		p, q = d1, d2
	d = 0
	for k in p.keys():
		d += abs(p[k] - q[k])
	return d

def dtx(d1, d2, pseudo=0, skip_missing=True, make_histogram=True):
	if make_histogram:
		p, q = make_histograms(d1, d2, pseudo=pseudo, skip_missing=skip_missing)
	else:
		p, q = d1, d2
	d = 0
	for k in p.keys():
		d += abs(p[k] - q[k]) * max(p[k]/q[k], q[k]/p[k])
	return d

def dty(d1, d2, pseudo=0, skip_missing=True, make_histogram=True):
	if make_histogram:
		p, q = make_histograms(d1, d2, pseudo=pseudo, skip_missing=skip_missing)
	else:
		p, q = d1, d2
	d = 0
	for k in p.keys():
		d += abs(p[k] - q[k]) * abs(math.log(p[k]/q[k]))
	return d

