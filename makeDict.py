#File Name: makeDict.py
#Author: John Francis Lomibao
#PID: A11591509

import sys
dict = {'This': 'This is a dictionary that maps gene name to locus tag'}

genPS_file = sys.argv[1]
opS_file   = sys.argv[2]
test = ''
gene_list = []

with open(genPS_file, 'r') as file:
	genPS_data = [line.strip() for line in file]
for i in range(len(genPS_data)):
	if not genPS_data[i].startswith('#'):
		col = genPS_data[i].split('\t')
		if len(col) >= 3 and col[2].startswith('b'):
			#col[1] is the gene name; col[2] is the locus_tag/bnumber
			gene_name = col[1]
			loc_tag   = col[2]
			gene_list.append(gene_name)
			dict[gene_name] = loc_tag;

#for i in gene_list:
#	print 'dict['+i+']:', dict[i]

with open(opS_file, 'r') as file:
	opS_data = [line.strip() for line in file]
for i in range(len(opS_data)):
	if not opS_data[i].startswith('#'):
		col = opS_data[i].split('\t')
		#col[7] is the evidence for confidence level (Confirmed, Strong, Weak)
		#col[0] is the operon name, col[5] are the names of the genes within the operon
		if (len(col) >= 8) and (col[7] == 'Strong' or col[7] == 'Confirmed'):
			op_name = col[0]
			gen_names = col[5]
			evidence = col[7]
			genes = gen_names.split(',')
			locTag_list = []
			for j in genes:
				try:
					locTag_list.append(dict[j])
				except:
					locTag_list.append(j)
			loc_tags = ''
			for j in locTag_list:
				loc_tags += j+','
			loc_tags = loc_tags[:-1]
			
			print op_name+'\t'+loc_tags+'\t'+evidence
			
