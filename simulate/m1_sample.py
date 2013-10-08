#!/usr/bin/python
''' makes a first order markov chain from an alignment
	samples from the chain

''' 

import sys

import numpy as np
from numpy.random import multinomial

from itertools import izip
#from itertools import compress
def compress(data, selectors):
	''' http://docs.python.org/2/library/itertools.html#itertools.compress
		New in version 2.7

	'''
	
	return (d for d, s in izip(data, selectors) if s)


def rdphy(fh):
	''' reads phyllip '''
	return [ line[10:].strip() for line in fh.readlines()[1:] ]

def transpose(lines):
	''' returns columns '''
	return [ ''.join((seq[i] for seq in lines)) for i in xrange(len(lines[0])) ]

def mk_trans(columns):
	''' makes transition probabilities '''
	trans = [ None for i in xrange(len(columns)) ]
	trans[0] = probs( tuple(('^', c) for c in columns[0]) )
	for i, col in enumerate(columns[1:], 1):
		trans[i] = probs(zip(columns[i-1], col)) 
	return trans

def probs(obs_vector):
	''' makes probability distributions '''
	return dict([ (o, (obs_vector.count(o) / float(len(obs_vector)))) for o in set(obs_vector) ])

def emit(pdist, sel_frAA):
	''' emit next aa, given sel_frAA '''
	toAA_list, prb_list = zip(*((toAA, prb) for (frAA, toAA), prb in pdist.iteritems() if frAA == sel_frAA))
	samp = np.random.multinomial(1, np.array(prb_list)/sum(prb_list), size=1)
	return compress(toAA_list, samp[0]).next()

def mk_cons(trans):
	prev = ''
	prev += emit(trans[0], '^')
	for i, pdist in enumerate(trans[1:], 1):
		prev += emit(pdist, prev[i-1])
	return prev

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print >>sys.stderr, 'usage: %s ali.phy > m1_sample.fa' % sys.argv[0]
		sys.exit(1)
	fn = sys.argv[1]
	fh = open(fn, 'r')
	ali = rdphy(fh)
	cols = transpose(ali)
	trans = mk_trans(cols)
	seq = mk_cons(trans)
	print '>m1_smp_rt'
	print seq















