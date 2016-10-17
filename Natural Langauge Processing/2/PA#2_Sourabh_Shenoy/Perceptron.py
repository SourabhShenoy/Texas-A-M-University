import sys
import getopt
import os
import math
import operator
import random

class Perceptron:
  class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test. 
    """
    def __init__(self):
      self.train = []
      self.test = []

  class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
      self.klass = ''
      self.words = []


  def __init__(self):
    """Perceptron initialization"""
    #in case you found removing stop words helps.
    self.stopList = set(self.readFile('../data/english.stop'))
    self.numFolds = 10
    self.input = []
    self.output = []
    self.totalVocab = {} #fetch features from the wordlist chosen
    for w in engWords:
      self.totalVocab[w] = 0
    
    self.weights = ([0] * len(self.totalVocab)) #Initial weight vector, set to 0s
      
  #############################################################################
  # TODO TODO TODO TODO TODO 
  # Implement the Perceptron classifier with
  # the best set of features you found through your experiments with Naive Bayes.

  def classify(self, words):
    for w in words:
      try:
        self.totalVocab[w] += 0.0001
      except KeyError: #To avoid exceptions when 0s are encountered
        pass
  
    new = 0
    values = self.totalVocab.values()
    tuple = zip(values,self.weights) #Zip function takes arguments and returns them in the form of a tuple
    for i,j in tuple:
      new += i * j
    for i in self.totalVocab:
      self.totalVocab[i] = 0

    return 'pos' if new > 0 else 'neg'

  def train(self, split, iterations):
    for example in split.train:
        words = example.words
        self.addExample(example.klass, words)
        k = len(self.input)
    
    #Implementation of averaged perceptron training algorithm is according to what is described in the paper http://www.umiacs.umd.edu/~hal/docs/daume06thesis.pdf
    c = 1 # c is the counter
    #Running weight vector, initialized to 0
    w0 = [0] * len(self.totalVocab)
    #Averaged weight vector, initialized to 0
    wa = [0] * len(self.totalVocab)

    #Algo runs for the number of iterations mentioned in the cmd line arg. The more, the better
    for i in range(iterations):
        for j in range(k): #Iterate through each example
            new = 0
            tuple = zip(w0,self.input[j])
            for x,y in tuple:
                new += x * y
            if self.output[j] * sign(new) < 0: #check to see if the example is classified corrctly; If no, then their product will be -ve, coz their signs will be different
                tuple1 = zip(self.input[j],w0)
                tuple2 = zip(self.input[j], wa)
                w0 = [(self.output[j] - sign(new)) * m + n for m,n in tuple1] #Update the running weight vector and move it closer to the correct sign
                wa = [(self.output[j] - sign(new)) * m * c + n for m,n in tuple2] #Update the averaged vector the same way, but use multiplicative factor 'c'
    c += 1 #Increment the iteration
  
    tuple = zip(w0,wa)
    #Return the weights by subtracting wa/c from w0, so that we get the averaged weight
    self.weights = [i-(j/c) for i,j in tuple]


  def addExample(self, klass, words):
    for w in words:
      try:
        self.totalVocab[w] += 0.0001
      except KeyError: #To avoid exceptions when 0s are encountered
        pass
  
    self.input.append(self.totalVocab.values())
    for i in self.totalVocab:
      self.totalVocab[i] = 0

    self.output.append(-1) if klass == 'neg' else self.output.append(1)


  # END TODO (Modify code beyond here with caution)
  #############################################################################
  
  
  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here, 
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    result = self.segmentWords('\n'.join(contents)) 
    return result

  
  def segmentWords(self, s):
    return s.split()

  
  def trainSplit(self, trainDir):
    """Takes in a trainDir, returns one TrainSplit with train set."""
    split = self.TrainSplit()
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    for fileName in posTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
      example.klass = 'pos'
      split.train.append(example)
    for fileName in negTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
      example.klass = 'neg'
      split.train.append(example)
    return split


  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = [] 
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      random.shuffle(split.train)
      splits.append(split)
    return splits
  
  
  def filterStopWords(self, words):
    """Filters stop words."""
    filtered = []
    for word in words:
      if not word in self.stopList and word.strip() != '':
        filtered.append(word)
    return filtered

def test10Fold(args):
  pt = Perceptron()
  
  iterations = int(args[1])
  splits = pt.crossValidationSplits(args[0])
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = Perceptron()
    accuracy = 0.0
    classifier.train(split,iterations)
  
    for example in split.test:
      words = example.words
      guess = classifier.classify(words)
      if example.klass == guess:
        accuracy += 1.0

    accuracy = accuracy / len(split.test)
    avgAccuracy += accuracy
    print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy) 
    fold += 1
  avgAccuracy = avgAccuracy / fold
  print '[INFO]\tAccuracy: %f' % avgAccuracy
    
    
def classifyDir(trainDir, testDir,iter):
  classifier = Perceptron()
  trainSplit = classifier.trainSplit(trainDir)
  iterations = int(iter)
  classifier.train(trainSplit,iterations)
  testSplit = classifier.trainSplit(testDir)
  accuracy = 0.0
  for example in testSplit.train:
    words = example.words
    guess = classifier.classify(words)
    if example.klass == guess:
      accuracy += 1.0
  accuracy = accuracy / len(testSplit.train)
  print '[INFO]\tAccuracy: %f' % accuracy
    
def main():
  (options, args) = getopt.getopt(sys.argv[1:], '')
  
  if len(args) == 3:
    classifyDir(args[0], args[1], args[2])
  elif len(args) == 2:
    test10Fold(args)

#To check if it is +ve class or -ve class
def sign(x):
    return 1 if x > 0 else -1

if __name__ == "__main__":
    file = open('engwords-5000.txt','r') # Using the 5000 most common words in English as features. Data from https://raw.githubusercontent.com/dwyl/english-words/master/words.txt
    #There are other word lists, which may help improve accuracy. However, the longer the list, the higher the runtime
    engWords=[]
    for line in file:
        engWords.append(line.strip())
    main()
