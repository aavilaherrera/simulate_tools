#!/usr/bin/python
''' read og for gap pattern -- specify type
	read sim -- same type
	lookup pattern for each sim seq
	print in same order

'''

import sys
import re

def rdfa(fh):
	''' caps, plmDI, dcaDI

	'''
	header = ""
	seq = ""
	gap_patterns = dict()
	for line in fh:
		line = line.rstrip('\n\r')
		if line.startswith('>'):
			if header != "":
				gap_patterns[header] = re.sub('\s+','', seq)
#			header = line.split()[0][1:] #CORRECT WAY....
			header = re.sub('--', ' --', line[1:]).split()[0] # hack to fix key error introduced by 2sim_to_fa_dir.py
			seq = ""
		else:
			seq += line
	gap_patterns[header] = re.sub('\s+', '', seq)
	return gap_patterns

def rdphy(fh):
	''' vi

	'''

	return dict(((line.strip().split()) for line in fh.readlines()[1:]))

def rdpsicov(fh):
	''' psicov

	'''

	return dict(((i, line.strip()) for i,line in enumerate(fh.readlines())))

def mk_mask(gap_pattern):
	for h,s in gap_pattern.iteritems():
		gap_pattern[h] = [ i for i,c in enumerate(s) if c == '-' ]
	return gap_pattern

def apply_mask(gap_idxs, seq):
	gseq = list(seq)
	for i in gap_idxs:
		gseq[i] = '-'
	return ''.join(gseq)

def fxfa(fh, gap_pattern):
	''' caps, plmDI, dcaDI
	
	'''

	header = ""
	hline = ""
	seq = ""
	for line in fh:
		line = line.rstrip('\n\r')
		if line.startswith('>'):
			if header != "":
				print hline
				print apply_mask(gap_pattern[header], re.sub('\s+', '',seq))
			header = line.split()[0][1:]
			header = re.sub('\d+$', '', header) # hack to fix key error with CAPS sim headers
			hline = line
			seq = ""
		else:
				seq += line
	print hline
	print apply_mask(gap_pattern[header], re.sub('\s+', '',seq))

def fxpsicov(fh, gap_pattern):
	''' psicov

	'''

	for i,line in enumerate(fh):
		print apply_mask(gap_pattern[i], re.sub('\s+', '', line))

def fxphy(fh, gap_pattern):
	''' vi

	'''

	for i, line in enumerate(fh):
		if i == 0:
			print line.rstrip('\n\r')
			continue
		head = line[:10]
		seq = line[10:]
		gseq = apply_mask(gap_pattern[head.strip()], re.sub('\s+', '', seq))
		print head+gseq

if __name__ == "__main__":
	usage = '%s fmt aln < sim > sim_gapped' % sys.argv[0]
	if len(sys.argv) < 3:
		print >>sys.stderr, usage
		sys.exit(1)

	fmt = sys.argv[1]
	aln_fn = sys.argv[2]
	aln_fh = open(aln_fn, 'r')
#	print >>sys.stderr, 'sim format is: %s' % fmt
	if fmt == 'psicov':
		gap_pattern = mk_mask(rdpsicov(aln_fh))
		fxpsicov(sys.stdin, gap_pattern)
	elif fmt == 'vi':
		gap_pattern = mk_mask(rdphy(aln_fh))
		fxphy(sys.stdin, gap_pattern)
	else:
		gap_pattern = mk_mask(rdfa(aln_fh))
		fxfa(sys.stdin, gap_pattern)
	

