#File Name: findConserved.py
#Author: John Francis Lomibao
#PID: A11591509

import sys

#set args
'''
Usage: "python findConserved.py <gene_file> <bdbh_file>"
'''
gene_file = sys.argv[1]
bdbh_file = sys.argv[2]

#open files
with open(gene_file, 'r') as file:
	gene_data = [line.strip() for line in file]
	
with open(bdbh_file, 'r') as file:
	bdbh_data = [line.strip() for line in file]
	
def hasOrtholog(geneToCheck):
	for i in range(len(bdbh_data)):
		orth_col = bdbh_data[i].split('\t')
		if geneToCheck == orth_col[0]:
			return orth_col[0]
		if geneToCheck == orth_col[1]:
			return orth_col[1]
	return 'none'

def checkRev(ortholog, gene):
	for i in range(len(gene_data)):
		gene_col = gene_data[i].split('\t')
		if ortholog == gene_col[4]:
			for j in range(1,6):
				rev_col = gene_data[i-j].split('\t')
				if hasOrtholog(rev_col[4]) == gene:
					return True
	return False
print hasOrtholog('NP_414544')
'''
#iterate through gene file
for i in range(len(gene_data)):
	col = gene_data[i].split('\t')
	curr_gene = col[4]
	if hasOrtholog(curr_gene) != 'none':
		for j in range(1, 6):
			col = gene_data[i+j].split('\t')
			if hasOrtholog(col[4]) != 'none':
				curr_orth = hasOrtholog(col[4])
				if checkRev(curr_orth, curr_gene) == True:
					print curr_gene+', '+hasOrtholog(curr_orth)+'\t'+hasOrtholog(curr_gene)+', '+curr_orth
'''
	
		
	