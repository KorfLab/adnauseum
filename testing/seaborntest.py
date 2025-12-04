
import seaborn as sns
import sys
import gzip

filename = sys.argv[1]
fp = gzip.open(filename, 'rt')


sns.set_theme()
"""
EXAMPLE
tips = sns.load_dataset("tips")

fig = sns.relplot(
	data=tips,
	x="total_bill", y="tip", col="time",
	hue="smoker", style="smoker", size="size"
)

fig.savefig('example')
"""

