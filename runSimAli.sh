#!/bin/bash
# A helper script that exports necessary variables.
# Edit to suit your needs

# Aram Avila-Herrera (Aram.Avila-Herrera@ucsf.edu)
# 
# alias revolver=java -cp /path/to/revolver/ revolver
export __REVOLVER="revolver"
export __SRC_PATH="/home/aram/dev-src/simulate_tools"

python ${__SRC_PATH}/src/simulate_alignment.py ${@}
