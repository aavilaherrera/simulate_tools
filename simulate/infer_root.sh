#!/bin/bash
# infer ancestral root using ancestral (ANCESCON)

if [ $# -ne 2 ]; then
	echo "Usage: $0 ancphy anctre > gapped_root.fa"
	exit 1
fi

echo '>root'
ancestral -C -RO -i ${1} -t ${2} -o /dev/stdout | grep 'Root_MidPoint' | awk '{print $3}'


