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
from os import getenv


src_dir = getenv('__SRC_PATH')

def get_cmd_options(args):
	''' Parse command line for options and return a dict.

		using getopt for compatibility

	'''
	
	usage = (
				'usage: %s [-h | [ --tree tree_file ] \n'+\
				'				[ --hmmer_db pfam.hmm ]\n'+\
				'				[ --outdir outdir ] input_aln.phy'
			) % sys.argv[0]
	
	try:
		optlist, args = getopt.getopt(args, 'ht:d:o:',
							['help', 'tree=', 'hmmer_db=',
							'outdir='])
	except getopt.GetoptError as err:
		print >>sys.stderr, 'Error: %s' % err
		sys.exit(usage)
	
	options = dict()
	
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

	if len(args) > 0:
		if exists(args[0]):
			options['aln_fn'] = args[0]
		else:
			print >>sys.stderr, '%s: file %s not found' % (sys.argv[0], args[0])
	else:
		print >>sys.stderr, '%s: alignment file not specified' % sys.argv[0]
	
	print 'running with options:'
	[ sys.stdout.write('\t%s: %s\n'%(opt, val))
				for opt, val in sorted(options.iteritems()) ]
		
	return options
	
def main(options):
	print 'in main()'
	infRoot = src_dir + '/simulate/infer_root.sh'
	if exists(infRoot):
		print 'will run: ' +  infRoot
	else:
		print infRoot + ' missing'


if __name__ == '__main__':
	options = get_cmd_options(sys.argv[1:])
	main(options)


