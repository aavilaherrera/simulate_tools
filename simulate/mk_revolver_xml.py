#!/usr/bin/python

import sys

def gen_str(jobname, opts):
	output_dir = opts['workdir'] + '/' + jobname
	
	xml_string = \
'''<?xml version="1.0" encoding="UTF-8" ?>
<configdata  xsi:schemaLocation="http://www.cibiv.at/Revolver ./input_schema.xsd" xmlns="http://www.cibiv.at/Revolver" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" >
	<config>
		<!-- hmmbuild/hmmpress output goes here -->
		<hmmdb path="%s"/>
		<hmmfetch location="/home/Common/opt/bin/hmmfetch"/>
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
		opts["treefile"],
		opts["alpha"],
		opts["ncats"],
		opts["scale_factor"],
		opts["rtseqfile"],
		opts["rtanofile"],
		output_dir #output dir
	)
	return xml_string

def parse_options(args, jobname):
	options = {	"alpha" : "1.0",
				"ncats" : "9",
				"scale_factor" : "1.0",

				"workdir" : "./",
				"treefile" : jobname+'.tre',
				"hmmfile" : jobname+'.hmm',
				"rtseqfile" : jobname+'.root',
				"rtanofile" : jobname+'.scan'
	}
	arg_opts = dict([ arg.split('=')[:2] for arg in args if '=' in arg])
	for opt_k in options.iterkeys():
		if opt_k in arg_opts:
			options[opt_k] = str(arg_opts[opt_k])
	return options

if __name__ == "__main__":
	if len(sys.argv) < 2:
		sys.exit(
'''usage: %s jobname [options]
	alpha=float
	ncats=int
	scale_factor=float
''' % sys.argv[0])
	

	jobname = sys.argv[1]
	print >>sys.stderr, "making revolver xml (No INDELs) for %s" % jobname
	options = parse_options(sys.argv[1:], jobname)
	xml_string = gen_str(jobname, options)
	xml_fh = open(options['workdir']+'/'+'revolver_input.%s' % jobname, 'w')
	print >>xml_fh, xml_string
	

	
