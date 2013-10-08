#!/bin/bash
# simulate all proteins in processed_alignments

ALI_DIR="./processed_alignments"

PARALLEL='yes'

#echo ${ALI_DIR}
#echo ${TRE_DIR}
#echo ${PARALLEL}

SCRIPTS="/home/aram/projects/coevo_bin"

if [ $# -gt 0 ]; then
	ALILIST=${@}
else
	ALILIST=$(ls ${ALI_DIR}/*.phy)
fi

# parallel version:
if [ "${PARALLEL}" == 'yes' ];
then
	ARGLIST=""
	for ALI in ${ALILIST};
	do
		JOB=$(basename ${ALI%.phy})
		ARGLIST="${ARGLIST} ${JOB} ./ 1000"
	done
	
	#echo ${ARGLIST}
	parallel -j 5 -l 13 -n 3 ${SCRIPTS}/do_revolver.sh -- ${ARGLIST}
	exit
fi


# serial version:
echo "serial version broken"
for ALI in $(ls ${ALI_DIR}/*.phy);
do
	echo sim ${ALI}
	JOB=$(basename ${ALI%.phy})
	${SCRIPTS}/do_revolver.sh ${ALI} ./ 1000
done


