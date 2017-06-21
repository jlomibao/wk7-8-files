#File Name: getBDBH.py
#Author: John Francis Lomibao
#PID: A11591509

import sys

#b1: ecoli v atume, b2: atume v ecoli
#b3: ecoli v ecoli, b4: atume v atume
blast1, blast2, blast3, blast4 = sys.argv[1:]

def openFile(toOpen):
	with open (toOpen, 'r') as file:
		lines = [line.strip() for line in file]
	return lines

b1_data = openFile(blast1)
b2_data = openFile(blast2)
b3_data = openFile(blast3)
b4_data = openFile(blast4)

'''
columns of interest:
0: pid_1
1: pid_2
4: bitscore
9: qcovs
14: scovs
'''

genes_list1 = []
best_hit1 = {}
bitMax = 0
#b1_data: genome1 vs genome2	
for i in range(len(b1_data)):
	col = b1_data[i].split('\t')
	#Check if either qcovs or scovs is greater than 60 for potential orthologs
	if float(col[9]) >= 60 or float(col[14]) >= 60:
		qseq = col[0]
		sseq = col[1]
		bitscore = col[4]
		#add qseq into list of genes if not already inside
		if qseq not in genes_list1:
			genes_list1.append(qseq)
		#if already inside, check if the bitscore is higher than
		#the highest one recorded so far for that gene
		else:
			bitMax = float(best_hit1[qseq][1])
		#if higher, replace the sseq and bitscore, as the new best hit
		if bitscore > bitMax:
			key = sseq, bitscore
			best_hit1[qseq] = key
			bitMax = 0

genes_list2 = []
best_hit2 = {}
bitMax = 0
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
			bitMax = float(best_hit2[qseq][1])
		if bitscore > bitMax:
			key = sseq, bitscore
			best_hit2[qseq] = key
			bitMax = 0
			
'''			
def printKey(list, dict):
	for i in list:
		print i, dict[i]
		
printKey(genes_list1, dict1)
printKey(genes_list2, dict2)
'''

bdbh = []
for i in genes_list1:
	#check if the besthits mastch
	try:
		if i in str(best_hit2[best_hit1[i][0]]):
			bdbh.append((i, best_hit1[i][0]))
	except KeyError:
		pass
for i in bdbh:
	print i[0]+'\t'+i[1]+'\torthology'+'\tBDBH'


#OHTP
#genome1 v genome1
not_ohtp = []
for i in range(len(b3_data)):
	col = b3_data[i].split('\t')
	#in addition to checking for qcov/scov >= 60, also check
	#that they are not the same gene
	if (float(col[9]) >= 60 or float(col[14]) >= 60 and col[0] != col[1]):
		qseq = col[0]
		sseq = col[1]
		bitscore = col[4]
		if qseq not in genes_list1:
			genes_list1.append(qseq)
		else:
			bitMax = float(best_hit1[qseq][1])
		if bitscore > bitMax:
			key = sseq, bitscore
			best_hit1[qseq] = key
			#since ohtp requires that gene in other genome is higher,
			#this qseq becomes unelligible
			not_ohtp.append(qseq)
			bitMax = 0
		
#genome2 v genome2
for i in range(len(b4_data)):
	col = b4_data[i].split('\t')
	if (float(col[9]) >= 60 or float(col[14]) >= 60 and col[0] != col[1]):
		qseq = col[0]
		sseq = col[1]
		bitscore = col[4]
		if qseq not in genes_list2:
			genes_list2.append(qseq)
		else:
			bitMax = float(best_hit2[qseq][1])
		if bitscore > bitMax:
			key = sseq, bitscore
			best_hit2[qseq] = key
			not_ohtp.append(qseq)
			bitMax = 0

ohtp = []			
for i in genes_list1:
	#if we know that the gene is not in the list of non ohtps,
	#and it is not in the list of bdbhs, it must be ohtp
	print i not in not_ohtp, i not in bdbh, i not in bdbh[0]
	if i not in not_ohtp and i not in bdbh:
		ohtp.append(i, best_hit1[i][0])
		
for i in genes_list2:
	print i not in not_ohtp, i not in bdbh, i not in bdbh[0]
	if i not in not_ohtp and i not in bdbh:
		ohtp.append(i, best_hit2[i][0])
		
for i in ohtp:
	print i[0]+'\t'+i[1]+'\torthology'+'\tOHTP'