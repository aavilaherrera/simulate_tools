#!/usr/bin/env python

import sys
from os.path import exists
from os import mkdir, popen

def gen_str(opts):
	''' makes the revolver parameter_input.xml file

	'''
	
	xml_string = \
'''<?xml version="1.0" encoding="UTF-8" ?>
<configdata  xsi:schemaLocation="http://www.cibiv.at/Revolver ./input_schema.xsd" xmlns="http://www.cibiv.at/Revolver" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" >
	<config>
		<!-- hmmbuild/hmmpress output goes here -->
		<hmmdb path="%s"/>
		<hmmfetch location="%s"/>
	</config>
	<model>
		<substitution name="WAG"/>
	</model>
	<!-- raxml output tree -->
	<tree path="%s" alpha="%s" categories="%s" scalingFactor="%s"/>
	<root>
		<inputSequence>
			<!-- ancescon output goes here -->
			<fasta file="%s"/>
			<!-- hmmscan output goes here -->
			<hmmer file="%s"/>
		</inputSequence>
	</root>
	<output>
		<dir path="%s" separateFastaFiles="false" trueAlignment="false" include="leaf"/>
	</output>
</configdata>
''' % (
		opts["hmmfile"],
		opts["hmmfetch"],
		opts["treefile"],
		opts["alpha"],
		opts["ncats"],
		opts["scale_factor"],
		opts["rtseqfile"],
		opts["rtanofile"],
		opts["outdir"] # sim sequence output
	)
	return xml_string

def parse_options(args, jobname):
	options = {	"alpha" : "1.0",
				"ncats" : "9",
				"scale_factor" : "1.0",

				#"workdir" : "."#,
				#"treefile" : jobname+'.tre',
				#"hmmfile" : jobname+'.hmm',
				#"rtseqfile" : jobname+'.root',
				#"rtanofile" : jobname+'.scan'
	}

	arg_opts = dict([ arg.split('=')[:2] for arg in args if '=' in arg])
	for opt_k in arg_opts:
		options[opt_k] = str(arg_opts[opt_k])

	if 'workdir' not in options:
		sys.exit('Error: workdir not specified')
	
	if 'rtseqfile' not in options:
		options['rtseqfile'] = '%s/tmp-%s/rtSqNoGap.fa' % (options['workdir'], jobname)
	if 'rtanofile' not in options:
		options['rtanofile'] = '%s/tmp-%s/rootSeq.scan' % (options['workdir'], jobname)
	if 'hmmfile' not in options:
		options['hmmfile'] = '%s/%s.hmm' % (options['workdir'], jobname)
	if 'outdir' not in options:
		options['outdir'] = '%s/revolver-%s' % (options['workdir'], jobname)
	
	if 'hmmfetch' not in options:
		options['hmmfetch'] = popen('which hmmfetch').read().strip()
	
	if 'treefile' not in options:
		sys.exit('Error: treefile not specified')
	if options['hmmfetch'] == '':
		sys.exit('Error: hmmfetch not installed')
	
	return options

if __name__ == "__main__":
	if len(sys.argv) < 2:
		sys.exit(
'''usage: %s jobname [options]
	alpha=float
	ncats=int
	scale_factor=float
	treefile=str
	rtseqfile=str
	rtanofile=str
	hmmfile=str
	workdir=str
''' % sys.argv[0])
	

	jobname = sys.argv[1]
	print >>sys.stderr, "making revolver xml (No INDELs) for %s" % jobname
	options = parse_options(sys.argv[2:], jobname)

	if not exists(options['workdir']):
		mkdir(options['workdir'])
	if not exists(options['outdir']):
		mkdir(options['outdir'])

	xml_string = gen_str(options)
	print xml_string
	

	
