#!/usr/bin/python
''' fasta to phylip no seqid mangling (only truncation)

'''

import sys

def rdfa(fh):
	ali = dict()
	header = ''
	seq = ''

	for line in fh:
		line = line.rstrip('\n\r')
		if line == '':
			continue
		if line.startswith('>'):
			if header != '':
				ali[header] = seq
				seq = ''
			header = line[1:].split(' ', 1)[0]
			continue
		seq += line.replace(' ', '')
	ali[header] = seq
	return ali

def prntphy(fh, ali):
	nseqs = len(ali)
	seqlen = len(ali.itervalues().next())
	print >>fh, ' %d %d' % (nseqs, seqlen)
	for h,s in ali.iteritems():
		print >>fh, h[:8].ljust(8) + '  ' + s


if __name__ == "__main__":
	prntphy(sys.stdout, rdfa(sys.stdin))
