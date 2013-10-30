#!/bin/bash

export __SRC_PATH="/home/aram/dev-src/simulate_tools"
export __REVOLVER="/home/aram/bin/revolver"

ALN='/home/aram/projects/customVifInts/processed_alignments/A3G.phy'
TRE='/home/aram/projects/customVifInts/trees/A3G.tre'

python ${__SRC_PATH}/src/simulate_alignment.py --num_sims 2 --outdir ./ --tree ${TRE} ${@} test_job ${ALN}




