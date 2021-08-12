import random

testDoc = open("corpus2_train.labels")

#Cross Validation
testSet = open("corpus2_test.list", 'w')
validation = open("corpus2_test.labels", 'w')
trainSet = open("corpus3_train1.labels", 'w')

#shuffle data
lines = testDoc.readlines()
random.shuffle(lines)
open('corpus3_shuffled.labels', 'w').writelines(lines)

shuffled = open('corpus3_shuffled.labels')

i = 0
for line in shuffled: 
    i+=1
    if (i == 716):
        break
    trainSet.write(line)
trainSet.close()
    
for line in shuffled: 
    x = line.split()
    testSet.write(x[0] + '\n')
    validation.write(line)

validation.close()
testSet.close()

