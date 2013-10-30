## simulate_tools

These scripts are mainly wrappers for various tools used to run a sequence evolution simulator.

`simulate_alignment.py` generates simulated protein alignments of a **fixed length** along a **given phylogeny**,
while **maintaining domain constraints** imposed by a given profile HMM. The inferred **root sequence**
of a given protein sequence alignment is evolved with [Revolver](http://www.cibiv.at/software/revolver/)

### Authors

Aram Avila-Herrera (Aram.Avila-Herrera at ucsf dot edu)

### Install
**Dependencies**

1. Revolver: <http://www.cibiv.at/software/revolver/>.
2. HMMER3: <http://hmmer.janelia.org/>.
3. ANCESCON: <ftp://iole.swmed.edu/pub/ANCESCON/>. Heads up, these are 32-bit binaries
4. numpy: <http://www.numpy.org/>

**revolver alias**
Alias revolver to make it easy to call from the commandline.
```bash
alias my_revolver_alias="java -cp /path/to/revolver/ revolver"
```

**simulate_tools**
Just let simulate_tools scripts know where they're located.
```bash
#!/bin/bash
# an example helper script...
export __SRC_PATH="/path/to/simulate_tools"
export __REVOLVER="my_revolver_alias"

python ${__SRC_PATH}/src/simulate_alignment.py ${@}

```

## Files
- src/simulate_alignment.py -- master python script that ties everything together
- format/* -- scripts used to go between the various miscellaneous sequence formats
- simulate/* -- scripts that help run Revolver

## Notes
- This is currently a huge mess, but surprisingly works
- ANCESCON has a weird bug that doesn't like long path names.
- Don't run multiple instances with the same job name at the same time...
- Don't edit to run Revolver in parallel, it will overwrite your output file or block.

## To do
1. add option to generate a "null" simulation (just permute columns). 
2. add revolver wrapper to repository
