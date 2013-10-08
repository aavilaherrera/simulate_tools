#!/usr/bin/python
''' fasta_to_phy.py -- Converts fasta to strict phylip

No ID mangling (truncate only)
Strict Phylip: 8 chars + 2 spaces + sequence on one line
Pipe friendly

'''

import sys
import re

def ReadFasta(fh):
	ali = list() # list of tuples
	header = ''
	seq = ''

	for line in fh:
		line = line.rstrip('\n\r')
		if line == '':
			continue
		if line.startswith('>'):
			if header != '':
				ali += [(header, re.sub("\s+","",seq))]
				seq = ''
			header = line[1:].split()[0] # split id line on whitespace
			continue
		seq += line
	ali += [(header, re.sub("\s+","",seq))] # remove whitespace from seqs
	return ali

def WritePhy(fh, ali):
	nseqs = len(ali)
	seqlen = len(ali[0][1]) # letters of first sequence
	print >>fh, ' %d %d' % (nseqs, seqlen)
	for h,s in ali:
		print >>fh, h[:8].ljust(8) + '  ' + s # pad and add 2 spaces


if __name__ == "__main__":
	if(len(sys.argv) > 1):
		print >>sys.stderr, "usage: %s < fasta > phy"
		sys.exit(1)
	WritePhy(sys.stdout, ReadFasta(sys.stdin))
