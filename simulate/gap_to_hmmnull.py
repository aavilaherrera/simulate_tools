#!/usr/bin/env python
''' gap_to_hmmnull.py -- fills gaps in a sequence with amino acids sampled
						from hmmer null distribution

'''

import sys
from numpy.random import multinomial
from numpy import exp, array
from random import shuffle

def rd_one_fa(fn):
	fh = open(fn, 'r')
	seq = ''.join(''.join(fh.readlines()[1:]).split('>')[0].split())
	return seq

def read_compo(fn):
	fh = open(fn, 'r')
	aadef_line = []
	compo_line = []
	for line in fh:
		line = line.strip()
		if line.startswith('HMM'):
			aadef_line = line.split()[1:]
		if line.startswith('COMPO'):
			compo_line = map(float,line.split()[1:])
			return (aadef_line, compo_line)

def generate_seq((aadef_line, compo_line), seq_len):
	compo_line = exp(-1*array(compo_line))
	samples = multinomial(seq_len, compo_line)
	seq = list(''.join([ aa * numX for aa, numX in  zip(aadef_line,samples) ]))
	shuffle(seq)
	return ''.join(seq)

def patch(seq, (aadef_line, compo_line)):
	ngaps = seq.count('-')
	rseq = generate_seq((aadef_line, compo_line), ngaps)
	rseq_it = ( rchr for rchr in list(rseq))
	
	seq_new = list()
	for char in list(seq):
		if char == '-':
			char = rseq_it.next()
		seq_new.append(char)
	seq_new = ''.join(seq_new)
	return seq_new

if __name__ == "__main__":
	if len(sys.argv) != 3:
		sys.exit("usage: %s root.fa derp.hmm > derp.fa")
	fafn = sys.argv[1]
	hmmfn = sys.argv[2]
	seq = rd_one_fa(fafn)
	aadef_line, compo_line = read_compo(hmmfn)
	seq_new = patch(seq, (aadef_line, compo_line))
	print ">root_patched"
	print seq_new


