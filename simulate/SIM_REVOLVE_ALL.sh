#!/bin/bash
# simulate all proteins in processed_alignments

usage(){
	echo "usage: $0 revolver_input.xml num_sims T|F" >> /dev/stderr
	echo "             mask with original gaps?--^" >> /dev/stderr
	exit 1
}

if [ "$#" != 3 ]; then
	usage
fi

if [ -z "${REVOLVER}" ]; then
	echo "export REVOLVER=\"/path/to/revolver_executable\""
	exit 2
fi

if [ -z "${__SRC_PATH}" ]; then
	echo "export __SRC_PATH=\"/path/to/simulate_tools\""
	exit 3
fi

RXML="${1}"
NSIMS="${2}"
GAPS="${3}"
REVDIR="$(dirname ${RXML})"


for REP in {1..${NSIMS}}; do
	${REVOLVER} ${RXML}
	if [ "${GAPS}" == "F" ]; then
		mv ${REVDIR}/out.fa ${REVDIR}/sim${REP}.fa
	else
		python ${__SRC_PATH}/simulate/apply_gaps.py phy2fa < ${REVDIR}/out.fa\
													> ${REVDIR}/sim${REP}.fa
	fi
done

	
