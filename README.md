## simulate_tools

These scripts are mainly wrappers for various tools used to run a sequence evolution simulator.

`simulate_alignment.py` generates simulated protein alignments of a **fixed length** along a **given phylogeny**,
while **maintaining domain constraints** imposed by a given profile HMM. The intention is to simulate a sequence
alignment that *looks like* a **given observed alignment**. A starting sequence (either inferred ancestral or 
randomly generated using the given alignment) is evolved with [Revolver](http://www.cibiv.at/software/revolver/)

Currently, the gapping pattern of the current alignment is overlayed onto the generated alignments.

### Authors

Aram Avila-Herrera (Aram.Avila-Herrera at ucsf dot edu)

### Install
**Dependencies**

1. Revolver: <http://www.cibiv.at/software/revolver/>
2. HMMER3: <http://hmmer.janelia.org/> (Make sure `hmmfetch` is in your path)
	- **NOTE:** Revolver requires version: [Easel h3.0rc2 (March 2010)](http://hmmer.janelia.org/software/archive)
3. ANCESCON: <ftp://iole.swmed.edu/pub/ANCESCON/> Heads up, these are 32-bit binaries
4. numpy: <http://www.numpy.org/>

**revolver alias**: Alias revolver to make it easy to call from the commandline.

```bash
alias my_revolver_alias="java -cp /path/to/revolver/ revolver"
# Increase java's stack size for large alignments
# alias my_revolver_alias="java -Xss16m -cp /path/to/revolver/ revolver"
```

**simulate_tools**: Let `simulate_tools` scripts know where they're located by editing
the `__SRC_PATH` and `__REVOLVER` variables in the `runSimAli.sh` helper script.

```bash
export __SRC_PATH="/path/to/simulate_tools"
export __REVOLVER="my_revolver_alias"

python ${__SRC_PATH}/src/simulate_alignment.py ${@}
```

## Files
- src/simulate_alignment.py -- master python script that ties everything together
- format/ -- scripts used to go between the various miscellaneous sequence formats
- simulate/ -- scripts that help run Revolver, ANCESCON, and HMMER3
- test/ -- a test directory with an example script `test.sh`

## Notes
- This is currently a huge mess, but surprisingly works
- Increase the java stack size with `-XssN` for large alignments. For alignments with more than 1052 sequences
set `N` greater than or equal to 16m (eg. `-Xss16m`).
- ANCESCON has a weird bug that doesn't like long path names.
	- A workaround involving symlinking requires absolute paths be used.
- ANCESCON is unusable with more than 250 sequences. An alternate starting sequence is generated from the alignment.
- Don't run multiple instances with the same job name at the same time...
- Be very careful about editing `simulate_alignment.py` to run Revolver in parallel, it will overwrite Revolver's `out.fa` or block.

## To do
- [ ] Package nicely
- [ ] Find replacement or source for ANCESCON
