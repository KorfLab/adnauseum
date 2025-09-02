adnauseum
=========

- `genes.tsv` provides aliases for worm gene names
- `favorites.tsv` is the names of some favorite GSE experiments
- `raw` contains raw data files (mostly TSV) from GEO
- `proc` contains processed files (gene, value)

To turn the raw files into processed files:

```bash
python3 column-extractor.py proc
```

A processed file looks like the following:

```
2L52.1  1.9472
rga-9   7.10205
pot-3   5.93749
nas-6   2.67548
rabr-2  0.6405567
*6R55.2*        0.0
sri-20  0.0
spe-10  2.5607
*AC3.12*        2.52482
ugt-49  10.9008
abu-1   0.336976
pqn-2   0.0
AC3.5   49.14538
```

The first column is the gene name, and the second is the expression value.

Some gene names are bracketed with astrisks. These names were not converted
properly. There may be good reasons for this.

- The name cooresponds to a pseudogene
- The name corresponds to a known RNA gene (snoRNA)
- The name corresponds to an ill-defined RNA (e.g. miRNA, lncRNA, etc)
- The name has been updated and is no longer used

For the time being, skip over all of the genes with asterisks.

The expression values may or may not be normalized to gene length.
