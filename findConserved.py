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

#Check if gene has homolog, return the homolog if it does, and 'none' if not
def hasHomolog(geneToCheck):
	for i in range(len(bdbh_data)):
		hom_col = bdbh_data[i].split('\t')
		if geneToCheck == hom_col[0]:
			return hom_col[1]
		if geneToCheck == hom_col[1]:
			return hom_col[0]
	return 'none'

#Check if last previous 5 genes from homolog is a homolog of a given gene
def checkRev(homolog, gene):
	gene_hom = hasHomolog(gene)
	for i in range(len(gene_data)):
		gene_col = gene_data[i].split('\t')
		if homolog in gene_col[4]:
			for j in range(1,6):
				rev_col = gene_data[i-j].split('\t')
				if rev_col[4] == gene_hom:
					return True
	return False
#iterate through gene file
for i in range(len(gene_data)):
	col = gene_data[i].split('\t')
	curr_gene = col[4]
	#check if gene has homolog
	if hasHomolog(curr_gene) != 'none':
		#if homolog, find next 5 genes
		for j in range(1, 6):
			next_col = gene_data[i+j].split('\t')
			#check if those genes have homologs
			if hasHomolog(next_col[4]) != 'none':
				curr_hom = hasHomolog(col[4])
				#check the previous 5 genes of the homologs of the genes found with homologs
				#if one of those genes is the homolog to curr_gene, then conserved gene has been found
				'''
				No pairs of conserved genes were found. May be due to incomplete homolog list as I was not
				able to finish finding OHTP homologs
				'''
				if checkRev(curr_hom, curr_gene):
					print curr_gene+', '+hasHomolog(curr_orth)+'\t'+hasHomolog(curr_gene)+', '+curr_orth

	
		
	