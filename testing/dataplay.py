import seaborn as sns
import gzip
import argparse

parser = argparse.ArgumentParser(description='messing with data - GSE114951')
parser.add_argument('rep0', type=str, help='rep 0 of A')
"""parser.add_argument('rep1', type=str, help='rep 1 of A')
parser.add_argument('rep2', type=str, help='rep 2 of A')
parser.add_argument('rep3', type=str, help='rep 3 of A')
parser.add_argument('rep4', type=str, help='rep 4 of A')
parser.add_argument('rep5', type=str, help='rep 5 of A')"""
arg = parser.parse_args()

fp0 = gzip.open(arg.rep0, 'rt')
"""fp1 = gzip.open(arg.rep1, 'rt')
fp2 = gzip.open(arg.rep2, 'rt')
fp3 = gzip.open(arg.rep3, 'rt')
fp4 = gzip.open(arg.rep4, 'rt')
fp5 = gzip.open(arg.rep5, 'rt')"""

gene_exp = {}
while True:
    line = fp0.readline()
    if line == '': break
    line = line.split()
    gene_exp[line[0]] = float(line[1])

fig = sns.relplot(data=gene_exp)

fig.savefig('GSE114951_0_fig')