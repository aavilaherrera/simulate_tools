#!/bin/bash
# tre_to_anctre.sh trims root branchlen from newick string

perl -pne 's/:\d+.\d+;/;/'
