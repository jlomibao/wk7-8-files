#File Name: getBDBH.py
#Author: John Francis Lomibao
#PID: A11591509

import sys

blast1 = sys.argv[1]
blast2 = sys.argv[2]

#Open both blast tables and put data in each into 2 arrays
with open(blast1, 'r') as file:
	b1_data = [line.strip() for line in file]

with open(blast2, 'r') as file:
	b2_data = [line.strip() for line in file]

'''
columns of interest:
0: pid_1
1: pid_2
4: bitscore
9: qcovs
14: scovs
'''

genes_list1 = []
dict1 = {}
bitMax = 0
#b1_data: genome1 vs genome2	
for i in range(len(b1_data)):
	col = b1_data[i].split('\t')
	#Check if either qcovs or scovs is greater than 60 for potential orthologs
	if float(col[9]) >= 60 or float(col[14]) >= 60:
		qseq = col[0]
		sseq = col[1]
		bitscore = col[4]
		if qseq not in genes_list1:
			genes_list1.append(qseq)
		else:
			bitMax = float(dict1[qseq][1])
		if bitscore > bitMax:
			key = sseq, bitscore
			dict1[qseq] = key

genes_list2 = []
dict2 = {}

#b2_data: genome2 vs genome1
for i in range(len(b2_data)):
	col = b2_data[i].split('\t')
	if float(col[9]) >= 60 or float(col[14]) >= 60:
		qseq = col[0]
		sseq = col[1]
		bitscore = col[4]
		
		if qseq not in genes_list2:
			genes_list2.append(qseq)
		else:
			bitMax = float(dict2[qseq][1])
		if bitscore > bitMax:
			key = sseq, bitscore
			dict2[qseq] = key
'''			
def printKey(list, dict):
	for i in list:
		print i, dict[i]
		
printKey(genes_list1, dict1)
printKey(genes_list2, dict2)
'''

bdbh = []
for i in genes_list1:
	try:
		if i in str(dict2[dict1[i][0]]):
			bdbh.append((i, dict1[i][0]))
	except KeyError:
		pass
for i in bdbh:
	print i[0]+'\t'+i[1]+'\torthology'+'\tBDBH'
