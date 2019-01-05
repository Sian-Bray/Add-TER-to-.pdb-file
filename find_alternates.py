#Written by Sian Bray on 26th December 2018. 

#Script that locates alternate rotamer conformations in .pdb files then prints out the offending line.
#This script is expecially useful if you want to try Rosetta Refine but your ~6000 residue structure contains ONE alternate conformation that is preventing you.

import argparse
parser = argparse.ArgumentParser(description='Locates any alternative rotamer conformations in a .pdb file.')
parser.add_argument('-i', type=str, required=True, help='path to the input .pdb')
args=parser.parse_args()

input_file=open(args.i, 'r')
input_length=len(input_file.readlines())
input_file.close
input_file=open(args.i, 'r')

residue_list=['ALA', 'GLY', 'LEU', 'MET', 'PHE', 'TRP', 'LYS', 'GLN', 'GLU', 'SER', 'PRO', 'VAL', 'ILE', 'CYS', 'TYR', 'HIS', 'ARG', 'ASN', 'ASP', 'THR',]

line_count=0

while line_count < input_length:
	current_line=input_file.readline()
	for item in residue_list:
		if 'A'+item in current_line:
			print(current_line)
	line_count+=1
