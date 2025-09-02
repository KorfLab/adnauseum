
class NameNormalizer:
	"""Converts names to standard nomenclature."""
	def __init__(self, file):
		self.names = {}
		with open(file) as fp:
			for line in fp:
				names = line.split()
				pref = names[0]
				for alias in names: self.names[alias] = pref

	def pref_gene_name(self, gene):
		# try simple lookup first
		if gene in self.names: return self.names[gene]

		# try removing prefix
		if ':' in gene:
			prefix, txt = gene.split(':')
			if txt in self.names: return self.names[txt]

		# failure mode: flag with stars
		return f'*{gene}*'
