#!/usr/bin/python
''' PhyToFasta.py -- Converts phy to fasta

No ID mangling
No Comment
Fasta: >ID line followed by sequence line
Pipe friendly

'''

import sys

def PhyToFasta(fh):
	line_counter = 0
	for line in fh:
		if line_counter == 0:
			line_counter += 1
			continue
		line = line.rstrip('\n\r')
		if line == '':
			continue
		print '>' + line[:10].strip() # remove whitespace
		print line[10:]

if __name__ == '__main__':
	if(len(sys.argv) > 1):
		print >>sys.stderr, "usage: %s < phy > fasta" % sys.argv[0]
		sys.exit(1)
	PhyToFasta(sys.stdin)

