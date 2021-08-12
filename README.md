# ece467-NLP #

## Text Categorization ##

This program is an implementation of a text categorization system a using Naive Bayes classifier. The system takes in two input files: one contains a list of labeled training documents, and the other containing a list of unlabeled documents. The first input file is used to train the system, and the second input file is used to test the system. The system outputs the labeled results to a user specified output file.

### Instructions for Running ###

#### corpus1 ####

Run the program
> python3 TC_Bayes.py

You will be prompted to enter the training set
> Enter name of file containing list of labeled training documents: corpus1_train.labels

You will be prompted to enter the test set:
> Enter name of file containing list of unlabeled test documents: corpus1_test.list

You will be prompted to enter the output text file (you can name this whatever you want):
> Enter name of output file: output.txt

Now the system has classified all the documents in the test set and is in the output file. To evaluate the performance, you will need to use the analyze.pl script.
> perl analyze.pl output.txt corpus1_test.labels

#### corpus2 and corpus3 ####

For these corpora, we only have a training set. To test the system on these corpora, I wrote a python script to perform cross-vaidation on the corpora (kfoldprep2.py for corpus2 and kfoldprep.py for corpus3)

Run kfoldprep2.py
> python3 kfoldprep2.py

You will see 4 new files were created: corpus2_shuffled.labels, corpus2_test.labels, corpus2_test.list, and corpus2_train1.labels. Disregard corpus2_shuffled.labels, this is just used in the python script. corpus2_train1.labels is the training set, corpus2_test.list is the unlabeled test documents, and corpus2_test.labels is the file containing the labeled documents to be used for evaluating how the system did on the unlabeled test documents. With these new files, follow the steps above using these files and you should be able to run and evaluate the system for corpus2 and corpus3.

## Parser ##

This program parses sentences using the CKY algorithm.

### Instructions for Running ###

Run the program
> python3 parser.py

You will be prompted to enter the file containing the CFG in CNF
> Enter the name of the file containing the CFG in CNF: cnf.txt

You will be prompted about whether you want the textual parse trees to be displayed. After that, enter a sentence and if it is valid according to the grammar, the parser will output "VALID SENTENCE" and all the possible valid parses (along with the textual parse trees if you choose enter "y" when prompted about them). The parser will prompt for a new sentence until you enter "quit".
