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
from os.path import exists, basename
from os import getenv, mkdir, makedirs, system, getcwd

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
				'				[ --skip_revxml ]\n'+\
				'				[ --outdir outdir ] job_name input_aln.phy'
			) % sys.argv[0]
	
	try:
		optlist, args = getopt.getopt(args, 'ht:d:o:n:',
							['help', 'tree=', 'hmmer_db=',
							'skip_anc', 'skip_hmmer', 'skip_revxml',
							'outdir=', 'num_sims='])
	except getopt.GetoptError as err:
		print >>sys.stderr, 'Error: %s' % err
		sys.exit(usage)
	
	options = dict()

	# set defaults
	options['skip_anc'] = False
	options['skip_hmmer'] = False
	options['skip_revxml']= False
	options['outdir'] = getcwd()
	options['hmmer_db'] = ''
	options['num_sims'] = 10


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
		if opt in ('--skip_revxml'):
			options['skip_revxml'] = True
		if opt in ('-n', '--num_sims'):
			options['num_sims'] = int(val)

	if len(args) != 2:
		print >>sys.stderr, 'Error: wrong number of args'
		sys.exit(usage)
	if not exists(args[1]):
		sys.exit('Error: %s does not exist' % args[1])

	options['job_name'] = args[0]
	options['aln_fn'] = args[1]

	print 'running with options:'
	[ sys.stdout.write('\t%s: %s\n'%(opt, str(val)))
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

	rtSeq_fn = tmpdir+'/rootSeq.fa'

	numSeqs = PhyCheckNumSeqs(aln_fn)
	#numSeqs = 1000

	if numSeqs > 1052:
		#sys.exit("Error: alignment \'%s\' too big for Revolver" % aln_fn)
		print "Warning: alignment \'%s\' too big for Revolver." % aln_fn
		print "Warning: Make sure N in java -XssNm is >= 16."
	if numSeqs > 250:
		print 'Warning: alignment too big for ancescon'
		print '\tsampling from 1st order markov chain'
		system('python %s/simulate/m1_sample.py %s > %s' % (src_dir, aln_fn, rtSeq_fn))
	else:
		# first format phy for ANCESCON
		ancphy = tmpdir + '/%s.ancphy' % job_name
		anctre = tmpdir + '/%s.anctre' % job_name
		
		print "%s: inferring root sequence" % basename(sys.argv[0])
		system('bash %s/format/phy_to_ancphy.sh < %s > %s' % (src_dir, aln_fn, ancphy))
		system('bash %s/format/tre_to_anctre.sh < %s > %s' % (src_dir, tre_fn, anctre))

		print "\n\n%s: ==DANGER: what seems to be a horrible overflow in ANCESCON requires short filepaths==" % basename(sys.argv[0])
		print "%s: creating symlinks in your home directory to attempt to circumvent this" % basename(sys.argv[0])
		ln1_stat = system('ln -s %s ~/TMPLNK-%s' % (ancphy, basename(ancphy)))
		ln2_stat = system('ln -s %s ~/TMPLNK-%s' % (anctre, basename(anctre)))

		system('bash %s/simulate/infer_root.sh %s %s > %s' % (src_dir, '~/TMPLNK-'+basename(ancphy), '~/TMPLNK-'+basename(anctre), rtSeq_fn))
		
		if ln1_stat == 0 and ln2_stat == 0:
			print "\n%s: ==DANGER: deleting symlinks" % basename(sys.argv[0])
			system('rm ~/TMPLNK-%s' % basename(ancphy))
			system('rm ~/TMPLNK-%s' % basename(anctre))

	return rtSeq_fn

def annotate_root(job_name, outdir, tmpdir, aln_fn, hmmer_db):
	''' annotates root sequence with profile hmm

		builds hmm from alignment if hmmer_db is empty.
		patches gaps with multinomial sample from hmm background.

	'''

	rtSeq_fn = tmpdir+'/rootSeq.fa'
	rtAno_fn = tmpdir+'/rootSeq.scan'
	rtSqNG_fn = tmpdir+'/rtSqNoGaps.fa'

	if hmmer_db == '':
		# build hmm from aln
		print "%s: building hmm from alignment" % basename(sys.argv[0])
		hmmer_db = '%s/%s.hmm' % (outdir, job_name)
		system('%s/format/phytosto.pl < %s | hmmbuild -n %s %s /dev/stdin' %
								(src_dir, aln_fn, job_name, hmmer_db))
	system('hmmpress -f %s' % hmmer_db)
	# annotate
	print "%s: annotating root sequence and patching gaps" % basename(sys.argv[0])
	system('hmmscan --notextw %s %s > %s' % (hmmer_db, rtSeq_fn, rtAno_fn))
	# patch gaps
	system('python %s/simulate/gap_to_hmmnull.py %s %s > %s' %
								(src_dir, rtSeq_fn, hmmer_db, rtSqNG_fn))

	return rtSqNG_fn

def generate_revolver_xml(job_name, outdir, tmpdir, tre_fn, hmmer_db):
	''' generates revolver xml in outdir/rev-job_name/job_name.xml

	'''
	
	rtSqNG_fn = tmpdir+'/rtSqNoGaps.fa'
	rtAno_fn = tmpdir+'/rootSeq.scan'
	revdir = outdir+'/revolver-%s'%(job_name)

	if not exists(revdir):
		print "%s: making %s" % (basename(sys.argv[0]), revdir)
		makedirs(revdir)

	#this global option should have defaults
	if hmmer_db == '':
		hmmer_db = '%s/%s.hmm' % (outdir, job_name)

	print "%s: making revolver xml input file" % basename(sys.argv[0])
	system(('python %s/simulate/mk_revolver_xml.py %s treefile=%s ' +
			'rtseqfile=%s rtanofile=%s hmmfile=%s workdir=%s > %s') %
			(src_dir, job_name, tre_fn, rtSqNG_fn, rtAno_fn, hmmer_db, outdir, revdir+'/'+job_name+'.xml'))
	return revdir

def run_revolver(job_name, outdir, aln_fn, num_sims):
	revdir = outdir+'/revolver-%s'%(job_name)
	revxml = revdir+'/%s.xml' % job_name
	
	print "%s: revolving now..." % basename(sys.argv[0]) 
	exit_status = system('bash %s/simulate/SIM_REVOLVE_ALL.sh %s %s %d AddBackOrigGaps' % (src_dir, revxml, aln_fn, num_sims))
	if exit_status == 0:
		print "%s: results in %s" % (basename(sys.argv[0]), revdir)
	
def main(options):
	''' makes tmpdir, infers root, degaps, runs revolver, regaps

	'''

	# make tmpdir
	tmpdir = options['outdir'] + '/' + 'tmp-' + options['job_name']
	if not exists(tmpdir):
		print "%s: Making %s" % (basename(sys.argv[0]), tmpdir)
		mkdir(tmpdir)
	
	# infer root
	if not options['skip_anc']:
		infer_the_root(options['job_name'], tmpdir, options['aln_fn'], options['tree'])

	# hmmer
	if not options['skip_hmmer']:
		annotate_root(options['job_name'], options['outdir'], tmpdir, 
						options['aln_fn'], options['hmmer_db'])

	# revxml
	if not options['skip_revxml']:
		generate_revolver_xml(options['job_name'], options['outdir'], tmpdir,
									options['tree'], options['hmmer_db'])
	
	# revolver
	run_revolver(options['job_name'], options['outdir'], options['aln_fn'], options['num_sims'])

if __name__ == '__main__':
	options = get_cmd_options(sys.argv[1:])
	main(options)


