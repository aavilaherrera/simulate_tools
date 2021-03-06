#!/bin/bash
# simulate all proteins in processed_alignments

usage(){
	echo "usage: $0 revolver_input.xml orig_aln num_sims T|F" >> /dev/stderr
	echo "             mask with original gaps?--^" >> /dev/stderr
	exit 1
}

if [ "$#" != 4 ]; then
	usage
fi

if [ -z "${__REVOLVER}" ]; then
	echo "export __REVOLVER=\"your revolver alias\""
	exit 2
fi

if [ -z "${__SRC_PATH}" ]; then
	echo "export __SRC_PATH=\"/path/to/simulate_tools\""
	exit 3
fi

RXML="${1}"

if [ ! -f "$RXML" ]; then
	echo "revolver xml not found" >> /dev/stderr
	echo "i am in $(pwd)" >> /dev/stderr
	echo "    looking for ${RXML}" >> /dev/stderr
	exit 4
fi

OGALN="${2}"
NSIMS="${3}"
GAPS="${4}"
REVDIR="$(dirname ${RXML})"


for (( REP = 1; REP <= ${NSIMS}; REP++)); do
	${__REVOLVER} ${RXML}
	if [ "${GAPS}" == "F" ]; then
		mv ${REVDIR}/out.fa ${REVDIR}/sim${REP}.fa
	else
		python ${__SRC_PATH}/simulate/apply_gap.py phy2fa ${OGALN} < ${REVDIR}/out.fa\
													> ${REVDIR}/sim${REP}.fa
	fi
done

	
