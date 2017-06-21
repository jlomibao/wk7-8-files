#File Name: mkBlastTbl.py
#Author: John Francis Lomibao
#PID: A11591509

import os.path
import re
import sys

'''
Usage: python mkBlastTbl.py <blast_output> <output_file_name>
''' 
boutToTbl = sys.argv[1]
writeFile = sys.argv[2]

col = []
qseqid, sseqid = '', ''
qlen = slen = nident = length = qstart = qend = sstart = send = 0
bitscore = evalue = pident = qcovs = scovs = 0.0
writeData = ''

#function to empty file
def emptyFile(*filesToEmpty):
	for i in filesToEmpty:
		if os.path.exists(i):
			thisFile = open(i, 'w')
			thisFile.truncate()
			thisFile.close()

#function to write string to given file
def writeToFile(fileToWrite, strToPutInFile):
	thisFile = open(fileToWrite, 'a')
	thisFile.write(strToPutInFile)
	strToPutInFile = ''
	thisFile.close()

emptyFile(writeFile)
with open(boutToTbl,  'r') as f:
	data = [line.strip() for line in f]
for i in range(len(data)):
	col = data[i].split('\t')
	
	m = re.search(r"([A-Z]+_[0-9]+)", col[0])
	qseqid = m.group(1)
	
	m = re.search(r"([A-Z]+_[0-9]+)", col[1])
	sseqid = m.group(1)
	
	qlen     = int(col[2])
	slen     = int(col[3])
	bitscore = float(col[4])
	evalue   = float(col[5])
	pident   = float(col[6])
	nident   = int(col[7])
	length   = int(col[8])
	qcovs    = float(col[9])
	qstart   = int(col[10])
	qend     = int(col[11])
	sstart   = int(col[12])
	send     = int(col[13])
	scovs    = (float(length)/float(slen))*100

	writeData += (qseqid+'\t'+sseqid+'\t'+str(qlen)+'\t'+str(slen)+'\t'+
		   str(bitscore)+'\t'+str(evalue)+'\t'+str(pident)+'\t'+str(nident)
		   +'\t'+str(length)+'\t'+str(qcovs)+'\t'+str(qstart)+'\t'+str(qend)
		   +'\t'+str(sstart)+'\t'+str(send)+'\t'+str(scovs)+'\n')
writeToFile(writeFile, writeData)

	
