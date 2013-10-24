#!/usr/bin/perl -w
# converts raxml readable phylip format to
# (a2m) to stockholm multiple
# sequence format
# Aram Avila-Herrera (Aram.Avila-Herrera@ucsf.edu)

# Usage: perl phytosto.pl < input.phy > output.sto

use strict;

if ($#ARGV > 1){
	my $usage = "$0 < input.fa > output.sto\n";
	print STDERR $usage;
	exit(1);
}

print "# STOCKHOLM 1.0\n\n";
foreach my $line (<STDIN>){
	chomp $line;
	if (length($line) < 11 or $. == 0){
		next;
	}
	my($head) = substr($line, 0,10);
	$head =~ s/\s+$//;
	my($seq) = substr($line, 10);
	print "$head\t$seq\n";
	next;
}

print "\n//\n";

