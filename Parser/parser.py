# ECE-467 Project 1
# Layth Yassin
# Professor Sable
# This program is an implementation of the CKY algorithm as a parser.

import re

# function returns the grammar rules (A -> B C or A -> w) in a dict where the keys are the non-terminal A, and the items are
# either a list of tuples (B, C) or a list of strings w
def storeCNF(fileCNFobj):
	dictCNF = {}
	while(1):
		tempLine = fileCNFobj.readline()
		line = tempLine.rstrip() # gets a single CNF grammar rule at a time
		if not line: # if statement is true, the EOF has been reached
			break
		count = 0
		index = [] # list that stores the indexes of the whitespaces in the grammar, which allows for obtaining the individual terminals and non-terminals
		for i in range(len(line)):
			if line[i] == ' ':
				index.append(i)
				count += 1
		if count == 2: # if true, the CNF is of the form of A -> w
			A = line[0:index[0]]
			w = line[index[1] + 1:]
			if A in dictCNF.keys(): # if true, the terminal value is added to the end of the list of terminals corresponding to the non-terminal
				dictCNF[A].append(w)
			else: # if true, a list is created to serve as the item of dictCNF[A], which stores the first terminal corresponding to the non-terminal
				dictCNF[A] = [w]
		if count == 3: # if true, the CNF is of the form of A -> B C
			A = line[0:index[0]]
			B = line[index[1] + 1:index[2]]
			C = line[index[2] + 1:]
			if A in dictCNF.keys(): # if true, the non-terminal values are added to the end of the list of terminals corresponding to the non-terminal as a tuple
				dictCNF[A].append((B, C))
			else: # if true, a list is created to serve as the item of dictCNF[A], which stores the first pair of non-terminals corresponding to the non-terminal as a tuple
				dictCNF[A] = [(B, C)]
	return dictCNF

# implementation of binary tree to keep track of backpointers
class TreeNode:
	def __init__(self, nonTerminal, leftChild, rightChild = None): # right child of node is set to "None" for the case that a terminal is the only child
		self.nt = nonTerminal # the non-terminal points to its child nodes from which its grammar is derived
		self.lc = leftChild # left child of parent node
		self.rc = rightChild # right child of parent node

# recursive function that prints the bracketed format of the parse
def printBracketed(node):
	if not (node.rc == None): # both child nodes are recursively called until base case is reached
		return "[" + node.nt + " " +  printBracketed(node.lc) + " " + printBracketed(node.rc) + "]"
	else: # base case where the only child the parent node has is a terminal
		return "[" + node.nt + " " + node.lc + "]"

# function to print the textual parse tree
def printTree(bracketParse):
	numTabs = 1 # keeps track of the number of tabs to output the correct amount of tabs
	prevIndex = 1 # index that keeps track of the last element that was not printed
	print('[', end = '') # prints the initial opening bracket before the 'S'

	for i in range(1, len(bracketParse)): # loops through the input sentence
		if bracketParse[i] == '[': # if true, the substring from prevIndex to the current index i is output (i.e., not including the '[')
			print(bracketParse[prevIndex:i] + '\n' + numTabs * '\t', end = '')
			numTabs += 1
			prevIndex = i
		if bracketParse[i] == ']': # if true, the substring from prevIndex to the current index i + 1 is output (i.e., including the ']')
			print(bracketParse[prevIndex:i + 1] + '\n' + (numTabs - 2) * '\t', end = '')
			numTabs -= 1
			prevIndex = i + 1

# populates the cells along the diagonal of the matrix with the possible part of speech tags of each word from the input sentence
def populateDiagonal(words, dictCNF, table, j):
	for A in dictCNF:
			if words[j - 1] in dictCNF[A]: # if the word (the terminal) is found in the grammar, store the appropriate POS
				table[j - 1][j].append(TreeNode(A, words[j - 1])) # node appended to list of possible nodes that could be formed
	return table

# populates the non-diagonal cells with the proper nodes; binary tree essentially formed that keeps track of the parse
def populateOther(dictCNF, table, i, j, k):
	listB = table[i][k] # list of the nodes at position [i, k]
	listC = table[k][j] # list of the nodes at position [k, j]
	if len(listB) > 0 and len(listC) > 0: # condition checks if both positions contain at least one node
		for A in dictCNF.keys():
			for BNode in listB:
				for CNode in listC:
					if (BNode.nt, CNode.nt) in dictCNF[A]: # if there is a matching rule in the CNF, a new node is added to the position [i, j]
						table[i][j].append(TreeNode(A, BNode, CNode))
	return table

# implementation of the CKY algorithim
def CKY(words, dictCNF, n):
	table = [[[] for col in range(n + 1)] for row in range(n)] # creation of the matrix
	for j in range(1, n + 1): # iterates over columns of matrix
		populateDiagonal(words, dictCNF, table, j)
		for i in range(j - 2, -1, -1): # iterates over the rows of the matrix
			for k in range(i + 1, j): # iterates over all the cells where a substring spanning i to j in the input can be split into 2
				populateOther(dictCNF, table, i, j, k)
	return table

# handling of cnf input file
fileCNF = input("Enter the name of the file containing the CFG in CNF: ")
fileCNFobj = open(fileCNF, 'r')

dictCNF = storeCNF(fileCNFobj)

fileCNFobj.close()

print("Loading grammar...\n")

while (1): # the system prompts the user for input repeatedly until the user inputs "quit" to exit 
	parseTreeYN = input("Do you want textual parse trees to be displayed (y/n)?: ")
	sentence = input("Enter a sentence or type \"quit\" to exit: ")
	
	if sentence == "quit":
		print("Goodbye!")
		break
	
	# processing of input sentence
	sentence = sentence.lower() # converts the input to all lowercase, allowing for the user to input capital letters
	words = re.findall('[A-Za-z0-9]+', sentence) # only stores words and numbers, allowing for the user to input punctuation
	
	n = len(words)
	table = CKY(words, dictCNF, n)

	parseList = [] # this list will store the the nodes that have 'S' as their root node, which means it's a valid parse
	parseNum = 0
	for value in table[0][n]:
		if value.nt == 'S':
			parseList.append(value)
			parseNum += 1

	if parseNum > 0: # if true, then there exists at least 1 valid parse
		print("VALID SENTENCE\n")
	else:
		print("NO VALID PARSES\n")

	# outputs the parses in bracketed form and as parse trees if the user chooses to have them displayed
	count = 0
	while count < parseNum:
		for node in parseList:
			count += 1
			print(f"Valid parse #{count}: ")
			bracketParse = printBracketed(node)
			print(bracketParse + '\n')
			if parseTreeYN == 'y':
				printTree(bracketParse)

	print(f"\nNumber of valid parses: {parseNum}\n")
