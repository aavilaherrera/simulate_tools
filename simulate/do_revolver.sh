#!/bin/bash
# run:
#	hmmbuild
#	hmmpress
#	ancestral
#	hmmscan
#	gap_to_hmmnull.py
#	revolver
# on:
#	protein.phy
#	protein.tre
#
# SCRIPTS:
SCRIPTS="/home/aram/projects/coevo_bin"

#############
# Usage
USG="Usage: $0 jobname [work dir] [num sims]"

if [ $# -lt 1 ]; then
	echo ${USG} > /dev/stderr
	exit 1
fi

#############
# jobname 
JOB=${1}

# directories
if [ "${2}" == "" ]; then
	WDIR="./"
else
	WDIR="${2}"
fi

ALIDIR="${WDIR}/processed_alignments"
TREDIR="${WDIR}/trees"
SIMDIR="${WDIR}/sims"
ANCDIR="${WDIR}/ancescon"
OUTDIR="${SIMDIR}/${JOB}"

for DIR in ${ALIDIR} ${TREDIR} ${SIMDIR} ${ANCDIR} ${OUTDIR}; do
	mkdir -p ${DIR}
done


# files
ALI=${ALIDIR}/${JOB}.phy
TRE=${TREDIR}/${JOB}.tre
ANCALI=${ANCDIR}/${JOB}.ancphy
ANCTRE=${ANCDIR}/${JOB}.anctre
HMM=${SIMDIR}/${JOB}.hmm
RTSQG=${SIMDIR}/${JOB}.rtgp
RTSEQ=${SIMDIR}/${JOB}.root
RTANO=${SIMDIR}/${JOB}.scan

# params
if [ "${3}" == "" ]; then
	NSIMS=1000
else
	NSIMS="${3}"
fi

#############
# ancestral
echo "preparing to infer root"

if [ $(wc -l < ${ALI}) -gt 1052 ]; then
	echo "TOO MANY SEQUENCES! ABORTING!" > /dev/stderr
	echo "TOO MANY SEQUENCES! ABORTING!"
	exit 1
fi

if [ $(wc -l < ${ALI}) -gt 250 ]; then
	echo "* too many seqs -> sampling from markov chain"
	${SCRIPTS}/m1_sample.py ${ALI} > ${RTSQG}

else
	echo "* inferring root"
	if [ ! -f ${ANCALI} ]; then
	${SCRIPTS}/phy_to_anc.sh < ${ALI} > ${ANCALI}
	fi

	if [ ! -f ${ANCTRE} ]; then
		${SCRIPTS}/tre_to_anctre.sh < ${TRE} > ${ANCTRE}
	fi

	${SCRIPTS}/infer_root.sh ${ANCALI} ${ANCTRE} > ${RTSQG}
fi

#############
# HMMER

echo "hmmering"
if [ ! -f "${HMM}" ]; then
	hmmbuild -n ${JOB} ${HMM} <(phytosto.pl < ${ALI})
	hmmpress -f ${HMM}
fi

hmmscan --notextw ${HMM} ${RTSQG} > ${RTANO}

#############
# patch root sequence
echo "patching"
${SCRIPTS}/gap_to_hmmnull.py ${RTSQG} ${HMM}  > ${RTSEQ}

#############
# revolver
echo "evolving"
${SCRIPTS}/mk_revolver_xml.py ${JOB} treefile=${TRE} hmmfile=${HMM}\
									rtseqfile=${RTSEQ} rtanofile=${RTANO}\
									workdir=${SIMDIR}
for ((SIM=1; SIM <= NSIMS; SIM++)); do
	echo -e "\t${JOB}: ${SIM}"
	revolver ${SIMDIR}/revolver_input.${JOB}
	${SCRIPTS}/fasta_to_phy.py < ${OUTDIR}/out.fa > ${OUTDIR}/${JOB}.sim${SIM}
done


