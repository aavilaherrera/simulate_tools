#!/bin/bash
# infer_root.sh -- infer ancestral root using ancestral (ANCESCON)

if [ $# != 2 ]; then
	echo "Usage: $0 ancphy anctre > gapped_root.fa" > /dev/stderr
	exit 1
fi

if [ "$(which ancestral)" == "" ]; then
	echo "Error: ancestral not installed" > /dev/stderr
	echo "Please symlink or install ancestral to your path" > /dev/stderr
	exit 2
fi

echo '>root'
ancestral -C -RO -i ${1} -t ${2} -o /dev/stdout | grep 'Root_MidPoint' | awk '{print $3}'


