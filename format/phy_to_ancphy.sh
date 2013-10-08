#!/bin/bash
# phy_to_ancphy.sh trims header from phylip file
# pipe friendly

if [ $# -ne 0 ]; then
	echo "usage: $0 < phy > ancphy" >> /dev/stderr
	exit 1
fi

tail -n+2 /dev/stdin


