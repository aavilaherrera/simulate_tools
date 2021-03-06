#!/bin/bash
# Just a test script to make sure everything works

# Input, output, and job_name are fixed, but you can still
# pass extra options like '--skip_hmmer' or '--help' when calling
 
### This is now included in ../runSimAli.sh helper script ###
# #alias revolver=java -cp /path/to/revolver/ revolver
# export __REVOLVER="revolver"
# export __SRC_PATH="/home/aram/dev-src/simulate_tools"
#############################################################


#TESTDIR="${__SRC_PATH}/test"

TESTDIR=`pwd`

ALN="${TESTDIR}/A3G.phy"
TRE="${TESTDIR}/A3G.tre"
OUTDIR="${TESTDIR}"

#python ${__SRC_PATH}/src/simulate_alignment.py --num_sims 5 --outdir ${OUTDIR} --tree ${TRE} ${@} test_job ${ALN}
bash ../runSimAli.sh --num_sims 5 --outdir ${OUTDIR} --tree ${TRE} ${@} test_job ${ALN}
