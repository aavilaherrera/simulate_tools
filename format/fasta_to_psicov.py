#!/usr/bin/python
''' fasta to psicov: removes seqid

'''

import sys
import re

def rdfa(fh):
	ali = list()
	header = ''
	seq = ''

	for line in fh:
		line = line.rstrip('\n\r')
		if line == '':
			continue
		if line.startswith('>'):
			if header != '':
				ali += [ seq ]
				seq = ''
			header = line[1:].split(' ', 1)[0]
			continue
		seq += re.sub('\s+', '', line)
	ali += [ seq ]
	return ali

def prntpsicov(fh, ali):
	for s in ali:
		print >>fh, s

if __name__ == "__main__":
	prntpsicov(sys.stdout, rdfa(sys.stdin))
