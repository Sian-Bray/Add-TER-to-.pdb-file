#Written by Sian Bray on 4th December 2018
#This script will add missing TER line(s), which indicate the end of a chain of residues, to a .pdb file that has been messed up manually in Coot.
#The script will also increase the atom serial number up for all subsequent lines to avoid repeating or misordered serial numbers.
#You will need to specify your input .pdb file with -i and output file with -o. Do give the output a different name to the input and output!
#As .pdb files are justified (not tab or comma delimited) the script takes input to direct it to the locations of the atom serial number and chain IDs. Please do eyeball your .pbd file in a text veiwer and check these locations against the defaults specified for -a (atom serial number) and -c (chain ID).
#Note: this script will not add a TER line to the end of the last chain, but that is easy to do manually as you don't need to change the atom number for all subsequent entries! :)

import argparse
parser = argparse.ArgumentParser(description="Add missing TER signals to .pdb files that have been manually messed up in Coot. Note: this script will not add a TER line to the end of the last chain, but that is easy to do manually as you don't need to change the atom number for all subsequent entries! :)")
parser.add_argument('-i', type=str, metavar='input_file', required=True, help='Path to the input .pdb file')
parser.add_argument('-o', type=str, metavar='output_file', required=True, help='Name for the output .pdb file. The output file will be created in your current directory.')
parser.add_argument('-a', type=int, metavar='atom_number', nargs='+', default=[6,11], help='The location of the atom serial numbers in the .pdb file. Open the .pdb file in a text veiwer, find the largest atom serial number (scroll right to the bottom of the .pdb, find the last row that starts ATOM and use the number in the second column) and count the characters, including spaces, starting at 0. From this insert the first and last+1 character-numbers of the atom-serial-numbers-location in the second column seperated by a space (e.g. for the last line "ATOM  41470  CD1 ILE b 177      14.073 -45.538-136.612  1.00 49.06           C  " write "6 11").')
parser.add_argument('-c', type=int, metavar='chain_number', default=21, help='The location of your chain ID in the .pdb file. Open the .pdb file in a text veiwer, find the chain ID and count the characters including spaces (from 0) upto the chain ID (e.g. for "ATOM  41470  CD1 ILE b 177      14.073 -45.538-136.612  1.00 49.06           C  " write 21).')
args = parser.parse_args()

input_file=open(args.i, 'r')
output_file=open(args.o, 'w+')
input_length=len(input_file.readlines())
input_file.close
input_file=open(args.i, 'r')
file_line_count=0
TER_additions=0

while file_line_count<(input_length-1):
	try:
		previous_line_number=current_line[args.a[0]:args.a[1]]
	except NameError:
		pass
	try:
		previous_line=current_line
	except NameError:
		pass
	try:
		previous_chain=current_chain
	except NameError:
		pass
	current_line=input_file.readline()
	current_line=current_line.replace('\n', '')
	try:
		num_increase=(current_line[args.a[0]:args.a[1]])
		num_increase=num_increase.replace(' ', '')
		num_increase=int(num_increase)+TER_additions
		num_increase=str(num_increase)
		while len(num_increase)<len(current_line[args.a[0]:args.a[1]]):
				num_increase=' '+num_increase
	except ValueError:
		pass
	if current_line[0:4]=='ATOM':
		current_chain=current_line[args.c]
	try:
		if current_chain!=previous_chain:
			if previous_line[0:3]!='TER':
				gap_1=int(args.a[0])-3 #gap size between TER and args.a
				gap_2=(args.c-5)-(args.a[1]) #gap between a no. and begining of chain sides
				chain_sides_1=args.c-5 #range of chain position +4 characters either side
				chain_sides_2=args.c+4
				gap_3= len(current_line)-len(current_line[:(args.c+4)])#gap between residue no. and end of the line (current line length - last digit in gap_2)
				TER_line='TER'+(' '*gap_1)+num_increase+(' '*gap_2)+previous_line[chain_sides_1:chain_sides_2]+(' '*gap_3)
				output_file.write(TER_line+'\n')
				TER_additions+=1
				num_increase=(current_line[args.a[0]:args.a[1]])
				num_increase=num_increase.replace(' ', '')
				num_increase=int(num_increase)+TER_additions
				num_increase=str(num_increase)
				while len(num_increase)<len(current_line[args.a[0]:args.a[1]]):
						num_increase=' '+num_increase
				written_line=current_line.replace(current_line[int(args.a[0]):int(args.a[1])], num_increase)
				output_file.write(written_line+'\n')
			if previous_line[0:3]=='TER':
				written_line=current_line.replace(current_line[int(args.a[0]):int(args.a[1])], num_increase)
				output_file.write(written_line+'\n')
	except NameError:
		output_file.write(current_line+'\n')
	try:
		if current_chain==previous_chain:
			written_line=current_line.replace(current_line[int(args.a[0]):int(args.a[1])], num_increase)
			output_file.write(written_line+'\n')
	except NameError:
		pass
	file_line_count+=1
if file_line_count==(input_length-1):
	output_file.write('END')

input_file.close()
output_file.close()