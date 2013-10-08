#!/usr/bin/python
''' fasta_to_psicov.py -- Converts fasta to PSICOV

Strips ID line
PSICOV: one sequence per line, no whitespace
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

def PrintPSICOV(fh, ali):
	for h,s in ali:
		print >>fh, s

if __name__ == "__main__":
	if(len(sys.argv) > 1):
		print >>sys.stderr, "usage: %s < fasta > psicov" % sys.argv[0]
		sys.exit(1)
	PrintPSICOV(sys.stdout, ReadFasta(sys.stdin))
