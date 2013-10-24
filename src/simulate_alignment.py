#!/usr/bin/env python
''' simulate_alignment.py -- Generate a hypothetical protein alignment.

	Learns parameters from a given protein alignment and uses them
	to simulate hypothetical alignment of *the same length*.

	*Be careful with gaps*

'''

__author__ = 'Aram.Avila-Herrera'
__email__ = 'Aram.Avila-Herrera@ucsf.edu'

import sys
import getopt
from os.path import basename, exists
from os import getenv, mkdir
from subprocess import *

src_dir = getenv('__SRC_PATH')

def get_cmd_options(args):
	''' Parse command line for options and return a dict.

		using getopt for compatibility

	'''
	
	usage = (
				'usage: %s [-h | [ --tree tree_file ] \n'+\
				'				[ --hmmer_db pfam.hmm ]\n'+\
				'				[ --skip_anc ]\n'+\
				'				[ --skip_hmmer ]\n'+\
				'				[ --outdir outdir ] job_name input_aln.phy'
			) % sys.argv[0]
	
	try:
		optlist, args = getopt.getopt(args, 'ht:d:o:',
							['help', 'tree=', 'hmmer_db=',
							'outdir='])
	except getopt.GetoptError as err:
		print >>sys.stderr, 'Error: %s' % err
		sys.exit(usage)
	
	options = dict()

	# set defaults
	options['skip_anc'] = False
	options['skip_hmmer'] = False
	options['outdir'] = './'
	options['hmmer_db'] = ''


	# read command line options
	for opt, val in optlist:
		if opt in ('-h', '--help'):
			sys.exit(usage)
		if opt in ('-o', '--outdir'):
			options['outdir'] = val
		if opt in ('-d', '--hmmer_db'):
			options['hmmer_db'] = val
		if opt in ('t', '--tree'):
			options['tree'] = val
		if opt in ('--skip_anc'):
			options['skip_anc'] = True
		if opt in ('--skip_hmmer'):
			options['skip_hmmer'] = True

	if len(args) != 2:
		print >>sys.stderr, 'Error: wrong number of args'
		sys.exit(usage)
	if not exists(args[1]):
		sys.exit('Error: %s does not exist' % args[1])

	options['job_name'] = args[0]
	options['aln_fn'] = args[1]

	print 'running with options:'
	[ sys.stdout.write('\t%s: %s\n'%(opt, val))
				for opt, val in sorted(options.iteritems()) ]
		
	return options

def PhyCheckNumSeqs(phy_fn):
	''' get number of sequences from phy header

		breaks if phy_fn doesn't exist or isn't a proper phylip file

	'''

	phy_fh = open(phy_fn, 'r')
	numSeqs = phy_fh.readlines()[0].strip().split()[0] # get num seqs from header
	return int(numSeqs)

def infer_the_root(job_name, tmpdir, aln_fn, tre_fn):
	''' infer root sequence and write as fasta to tmpdir/rootSeq.fa

		check number of sequences in aln_fn and run ANCESCON
		or sample from 1st order markov chain

		file formatting required for ANCESCON
	
	'''

	numSeqs = PhyCheckNumSeqs(aln_fn)
	#numSeqs = 1000
	
	if numSeqs > 1052:
		sys.exit("alignment \'%s\' too big for Revolver" % aln_fn)
	if numSeqs > 250:
		print 'alignment too big for ancescon'
		print 'sampling from 1st order markov chain'
		rootSeq = Popen(['python', src_dir+'/simulate/m1_sample.py', aln_fn], stdout=PIPE).communicate()[0]

	else:
		# first format phy for ANCESCON
		ancphy = tmpdir + '/%s.ancphy' % job_name
		anctre = tmpdir + '/%s.anctre' % job_name
		
		fmt_seq = Popen(['bash', src_dir+'/format/phy_to_ancphy.sh'], stdin=open(aln_fn), stdout=PIPE).communicate()[0]
		fmt_tre = Popen(['bash', src_dir+'/format/tre_to_anctre.sh'], stdin=open(tre_fn), stdout=PIPE).communicate()[0]

		ancphy_fh = open(ancphy, 'w')
		print >>ancphy_fh, fmt_seq
		ancphy_fh.close()

		anctre_fh = open(anctre, 'w')
		print >>anctre_fh, fmt_tre
		anctre_fh.close()

		rootSeq = Popen(['bash', src_dir+'/simulate/infer_root.sh', ancphy, anctre], stdout=PIPE).communicate()[0]
	
	rootSeq_fh = open(tmpdir +'/rootSeq.fa', 'w')
	print >>rootSeq_fh, rootSeq
	rootSeq_fh.close()
	
	return

def annotate_root(job_name, hmmer_db, tmpdir):
	if hmmer_db == '':
		return 'le empty'
	else:
		return 'le not empty'

def main(options):
	''' makes tmpdir, infers root, degaps, runs revolver, regaps

	'''

	print 'in main()'

	# make tmpdir
	tmpdir = options['outdir'] + '/' + 'tmp-' + options['job_name']
	if not exists(tmpdir):
		mkdir(tmpdir)
	
	if not options['skip_anc']:
		infer_the_root(options['job_name'], tmpdir, options['aln_fn'], options['tree'])

	if not options['skip_hmmer']:
		annotate_root(options['job_name'], options['hmmer_db'], tmpdir)
	
if __name__ == '__main__':
	options = get_cmd_options(sys.argv[1:])
	main(options)


