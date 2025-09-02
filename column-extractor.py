import argparse
import pandas as pd

def readexcel(file, headers, genecol, l4col):
	l4cols = l4col.split(';')
	print(l4cols)
	#df = pd.read_excel(file)

def readfile(file, ftype, fend, headers, genecol, l4col):
	l4cols = l4col.split(';')
	print(l4cols)
	print(l4col)

def tx2gene(uid):
	f = uid.split('.')
	if   len(f) < 2: return ''
	elif len(f) == 2: clone, gene = f
	elif len(f) == 3: clone, gene, iso = f
	else: sys.exit(f'wtf {f}')

	if   gene[-1].isdigit(): return f'{clone}.{gene}'
	elif gene[-1].isalpha(): return f'{clone}.{gene[:-1]}'

parser = argparse.ArgumentParser()
parser.add_argument('--faves', metavar='<file>', default='favorites.tsv',
	help='file of favorite GSEs [%(default)s]')
parser.add_argument('--genes', metavar='<file>', default='genes.tsv',
	help='file of gene names and aliases [%(default)s]')
parser.add_argument('--data', metavar='<dir>', default='raw',
	help='directory of GEO raw files [%(default)s]')
parser.add_argument('outdir', help='output directory')
arg = parser.parse_args()

# preload gene names for lookup
name_table = {}
with open(arg.genes) as fp:
	for line in fp:
		names = line.split()
		pref = names[0]
		for alias in names: name_table[alias] = pref



with open(arg.faves) as fp:
	header = next(fp)
	for line in fp:
		f = line.split('\t')
		if len(f) == 9: f.pop()
		gse, ok, ftype, fend, hl, gene, l4, file = f
		if ftype == 'Excel': data = readexcel(file, hl, gene, l4)
		else:                data = readfile(file, ftype, fend, hl, gene, l4)
		# do something to check data

"""


if arg.build:
	for filename in glob.glob(f'{arg.build}/*'):
		with open(filename) as fp: gene = json.load(fp)
		ids = set()
		for db in gene:
			if 'display_id' in db: ids.add(db['display_id'])
			if 'primary_id' in db: ids.add(db['primary_id'])
		wbid = None
		for uid in ids:
			if uid.startswith('WBGene'):
				wbid = uid
				break
		if wbid not in names: names[wbid] = []
		for uid in ids:
			if uid != wbid: names[wbid].append(uid)
	with open(arg.index, 'w') as fp:
		print(json.dumps(names, indent=2), file=fp)
else:
	with open(arg.index) as fp: names = json.load(fp)

lookup = {}
for wbid in names:
	for xid in names[wbid]:
		if xid not in lookup: lookup[xid] = []
		lookup[xid].append(wbid)
	lookup[wbid] = [wbid] # just in case

if arg.file == '-': fp = sys.stdin
else: fp = open(arg.file)

missing = set()
multiple = set()
for line in fp:
	line = line.rstrip()
	f = line.split(maxsplit=1)
	if len(f) == 1:
		uid = line
		stuff = None
	else: uid, stuff = f

	if uid not in lookup:
		uid = tx2gene(uid) # try transcript ID instead
		if uid not in lookup:
			missing.add(uid)
			continue

	if len(lookup[uid]) > 1:
		multiple.add(uid)
		continue
	if stuff is None:
		print(lookup[uid])
	else:
		print(lookup[uid][0], stuff, sep='\t')


print('missing:', missing, file=sys.stderr)
print('multiple:', multiple, file=sys.stderr)

"""
