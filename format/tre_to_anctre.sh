#!/bin/bash
# tre_to_anctre.sh trims root branchlen from newick string
# pipe friendly

if [ $# -ne 0 ]; then
	echo "usage: $0 < tre > anctre" >> /dev/stderr
	exit 1
fi

perl -pne 's/:\d+.\d+;/;/'
