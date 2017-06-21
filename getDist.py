#File Name: getDist.py
#Author: John Francis Lomibao
#PID: A11591509

import sys
import _mysql

get_positive_ctrl = True
get_negative_ctrl = True

#check for control flag
try:
	if sys.argv[1] == '-c':
		if sys.argv[2] == 'p': #p for positive
			get_positive_ctrl = True
			get_negative_ctrl = False
		elif sys.argv[2] == 'n': #n for negative
			get_positive_ctrl = False
			get_negative_ctrl = True
		operons_file = sys.argv[3] 
	else:
		print "Usage: python getDist.py '-c p/n'* <operons_file> *optional"
		sys.exit(0)
except:
	print "Usage: python getDist.py '-c p/n'* <operons_file> *optional"
	
def connect():
	#connect to mysql (password omitted for github file)
	return _mysql.connect('bm185s-mysql.ucsd.edu', 'bm185sae', '******', 'bm185sae_db')

'''
operons file:
	column 1 = operon_name
	column 2 = genes in operon_name
'''
with open(operons_file, 'r') as file:
	operons_data = [line.strip() for line in file]
	
#operon_list: list of the genes in each operon_list
operon_list = []

#list of positive control distances
pos_ctrl_dists = []

#get genes of each operon and put into list
for i in range(len(operons_data)):
	col = operons_data[i].split('\t')
	operon_list.append(col[1])

if get_positive_ctrl == True:
	for i in range(len(operon_list)):
		#need to separate the locus tags to use in mysql
		col = operon_list[i].split(',')
		valid_op = True
		
		for j in col:
			#some of the operons in the operons table I made had genes without a locus tag.
			#I listed them anyway with their normal name, but we'll ignore them here
			if not j.startswith('b'): #we know locus tags in e coli start with 'b'
				valid_op = False

		#need operons of length >= 2 to calculate positive control
		if len(col) >= 2 and valid_op:
		
			#construction the command to execute in mysql, start of exe construction
			exe = ("SELECT g.gene_id, e.left_pos, e.right_pos, g.strand "+
				   "FROM genes g JOIN exons e USING(gene_id) "+
				   "WHERE g.locus_tag IN (")
				 
			for j in col:
				exe += "'"+j+"'"+','
			exe = exe[:-1] +') ORDER BY e.left_pos ASC;'
			#end of exe construction
			
			#connect to mysql (password omitted for github file)
			con = connect()
			#con = _mysql.connect('bm185s-mysql.ucsd.edu', 'bm185sae', '64d@r749', 'bm185sae_db')
			con.query(exe) #execute exe in mysql
			result = con.store_result()
			totalrows = result.num_rows()
			
			op_start = True #to mark start of operon,
			#when the for loop goes through it's first iteration,
			#bool is set to false, as it is now not the start of the operon
			for rows in range(totalrows):
				#remove " ' ", " ( ", and " ) " characters from line
				row = "".join(filter(lambda char: char != '\'' and char != '(' and char != ')',str(result.fetch_row())))
				row = row[:-1]
				#col[0] = gene, col[1] = left_pos, col[2] = right_pos
				col = row.split(',')
				left_pos = int(col[1])
				if op_start == False:
					dist = (left_pos-right_pos)+1
					pos_ctrl_dists.append(dist)
					print dist
				right_pos = int(col[2])
				
				op_start = False
			con.close()

gene_list = []
#if negative ctrl flag checked
if get_positive_ctrl == False:
	#exe construction
	exe = ("SELECT g.gene_id, g.locus_tag, "+
		   "e.left_pos, e.right_pos, g.strand "+
		   "FROM genes g JOIN exons e USING(gene_id) "+
		   "WHERE g.genome_id=1 ORDER BY e.left_pos ASC;")
	
	#connect to mysql
	con = connect()
	con.query(exe) #execute exe in mysql
	result = con.store_result()
	totalrows = result.num_rows()
	for rows in range(totalrows):
		#remove " ' ", " ( ", and " ) " characters from line
		row = "".join(filter(lambda char: char != '\'' and char != '(' and char != ')',str(result.fetch_row())))
		row = row[:-1]
		col = row.split(',')
		#col[0] = gene_id, col[1] = locus_tag, col[2] = left_pos, col[3] = right_pos, #col[4] = strand
		gene_list.append((col[0], col[1], col[2], col[3], col[4]))
	con.close()
	
	operon_ends = []
	for i in range(len(operon_list)):
		#need to separate the locus tags to use in mysql
		col = operon_list[i].split(',')
		valid_op = True
		
		for j in col:
			#some of the operons in the operons table I made had genes without a locus tag.
			#I listed them anyway with their normal name, but we'll ignore them here
			if not j.startswith('b'): 
				valid_op = False
		#only use operons with genes in our gene table
		if valid_op:
			operon_ends.append((col[0], col[-1]))
	#go through our list of genes ordered by left exon position
	for i in range(len(gene_list)):
		#initialize bool in_list to false
		#in_list specifies whether curr_gene is in our operon_ends list
		in_list = False
		#.strip() to get rid of white space
		curr_gene = gene_list[i][1].strip()
		for j in range(len(operon_ends)):
			if curr_gene in operon_ends[j]:
				next_gene = gene_list[i+1][1].strip()
				in_list = True
				break
		if in_list:
			for j in range(len(operon_ends)):
				#need to check if next_gene is also in our list
				if next_gene in operon_ends[j]:
					curr_strand = gene_list[i][4].strip()
					next_strand = gene_list[i+1][4].strip()
					if curr_strand == next_strand:
						right_pos = int(gene_list[i][2].strip())
						left_pos = int(gene_list[i+1][3].strip())
						dist = (left_pos - right_pos) + 1
						print dist
						break
		
		
		

		
			
	
		
	

	
