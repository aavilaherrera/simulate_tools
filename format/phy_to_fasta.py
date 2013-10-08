#!/usr/bin/python
''' phy_to_fasta.py -- no name mangling

'''

import sys

def phy_to_fasta(fh):
	cnt = 0
	for line in fh:
		if cnt == 0:
			cnt += 1
			continue
		line = line.rstrip('\n\r')
		if line == '':
			continue
		print '>' + line[:10]
		print line[10:]

if __name__ == '__main__':
	phy_to_fasta(sys.stdin)

