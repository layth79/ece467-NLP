# ECE-467 Project 1
# Layth Yassin
# Professor Sable
# This program is an implementation of the Naive Bayes machine learning algorithm for text categorization

# function returns a list of all the words (with no repetition) that occur in the labeled training set
def vocabulary(tokenized):
	flattened_tokenized = list(chain.from_iterable(tokenized))
	return list(set(flattened_tokenized))

# function returns the categories that are being dealt with in the labeled training set
def uniqueCategories(correspondCats):
	return list(set(correspondCats))

# function returns the number of documents in a specified category in the labeled training set 
def NumDocsInCat(correspondCats, distinctCat):
	return correspondCats.count(distinctCat)

# function returns a list of strings, where each string is a document. The list contains all the documents in a specified category
def bigDoc(docs, correspondCats, distinctCat):
	return [docs[i] for i, element in enumerate(correspondCats) if element == distinctCat]

# function returns the number of documents a word appears in for a specified category
def numerator(word, bigdoc, c):
	counter = 0
	for i in range(len(bigdoc[c])):
		if word in bigdoc[c][i]:
			counter += 1
	return counter

# function trains the system
def trainNB(docs, correspondCats, tokenized):
	flattenedList = vocabulary(tokenized)
	uniqueCats = uniqueCategories(correspondCats)
	V = []

	# conditionals find which set of categories the system is dealing with
	if ('Str' or 'Pol' or 'Dis' or 'Cri' or 'Oth') in uniqueCats:
		k = 0.15
		V = flattenedList
	elif ('I' or 'O') in uniqueCats:
		k = 0.02
		V = flattenedList
	else:
		k = 0.15
		for w in flattenedList:
			if w.isalpha():
				V.append(w)		
	
	Ndoc = len(docs)

	logprior = []
	count = []
	bigdoc = []
	outerlist = [None] * len(uniqueCats)
	innerdict = {}

	# loops calculate the log of the likelihood of a word appearing a specific category (done for all words in the vocabulary and all the categories) 
	for c in range(0, len(uniqueCats)):
		Nc = NumDocsInCat(correspondCats, uniqueCats[c])		
		logprior.append(math.log10(Nc/Ndoc))

		bigdoc.append(bigDoc(docs, correspondCats, uniqueCats[c]))

		for w in V:
			count = numerator(w, bigdoc, c) 
			loglikelihood = math.log10((count + k) / (len(bigdoc[c]) * k))
			innerdict[w] = loglikelihood 
		outerlist[c] = innerdict
		innerdict = {}

	return uniqueCats, logprior, outerlist

# function returns the system's prediction for the category of the given test document
def testNB(testdoc, logprior, correspondCats, outerlist, uniqueCats):
	sum1 = []
	
	for c in range(len(uniqueCats)):
		sum1.append(logprior[c])
		
		for w in testdoc:
			if w in outerlist[c].keys():
				sum1[c] = sum1[c] + outerlist[c][w] 
				
	greatest = max(sum1)
	index = sum1.index(greatest)
	argmaxc = uniqueCats[index]
	return argmaxc

from nltk.tokenize import word_tokenize
from itertools import chain
import math

fileName1 = input("Enter name of file containing list of labeled training documents: ")
fileObj1 = open(fileName1, 'r')
contentList1 = fileObj1.readlines()

docs = []
correspondCats = []

# loop populates two lists: one containing all the documents from the labeled training set, 
# the other containing the corresponding category of each document in the same index as the documents list
for i in range(len(contentList1)):
    contentSplit = contentList1[i].split()
    tempObj = open(contentSplit[0])
    docs.append(tempObj.read())
    correspondCats.append(contentSplit[1])

# tokenizing of all the documents in the labeled training set
tokenized = [word_tokenize(i) for i in docs]

uniqueCats, logprior, outerlist = trainNB(docs, correspondCats, tokenized)

fileObj1.close()

fileName2 = input("Enter name of file containing list of unlabeled test documents: ")
fileObj2 = open(fileName2)
contentList2 = fileObj2.read().splitlines()

outputFileName = input("Enter name of output file: ")
outputFile = open(outputFileName, 'w')

# loop formats the system's predictions and outputs it to a file specified by the user
for i in range(len(contentList2)):
	tempDocObj = open(contentList2[i])
	tempdoc = tempDocObj.read()
	tempDocObj.close()
	testdoc = word_tokenize(tempdoc)
	argmaxc = testNB(testdoc, logprior, correspondCats, outerlist, uniqueCats)
	outputFile.write(contentList2[i] + ' ' + argmaxc + '\n')

fileObj2.close()
outputFile.close()
