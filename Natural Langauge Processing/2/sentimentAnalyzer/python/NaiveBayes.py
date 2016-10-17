import sys
import getopt
import os
import math
import operator
import collections #To use a special type of dictionary, 'default_dict', which allows setting of default values.

class NaiveBayes:
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
    """NaiveBayes initialization"""
    self.FILTER_STOP_WORDS = False
    self.BOOLEAN_NB = False
    self.stopList = set(self.readFile('../data/english.stop'))
    self.numFolds = 10

    self.numPosDocuments = 0        #To compute prior
    self.numNegDocuments = 0        #To compute prior
    self.numTotalDocuments = 0      #To compute prior

    #The structures below will be used to compute the likelihood
    self.pos_word_count = 0 # Total number of unique words in positive documents
    self.neg_word_count = 0 # Total number of unique words in negative documents
    self.TotalPos = collections.defaultdict(lambda: 0) #defaultdict is a member of the collections class. When a non existing key is referenced, we return 0.
    self.TotalNeg = collections.defaultdict(lambda: 0) #defaultdict is a member of the collections class. When a non existing key is referenced, we return 0.

    self.vocabSet = set() #Total number of unique words in the vocabulary across all documents
    self.vocabCount = 0


  #############################################################################
  # TODO TODO TODO TODO TODO 
  # Implement the Multinomial Naive Bayes classifier and the Naive Bayes Classifier with
  # Boolean (Binarized) features.
  # If the BOOLEAN_NB flag is true, your methods must implement Boolean (Binarized)
  # Naive Bayes (that relies on feature presence/absence) instead of the usual algorithm
  # that relies on feature counts.
  #
  #
  # If any one of the FILTER_STOP_WORDS and BOOLEAN_NB flags is on, the
  # other one is meant to be off.

  def classify(self, words):
    if self.FILTER_STOP_WORDS:
      words =  self.filterStopWords(words)
    
    posProbab = 0 #probability that the document is classified as positive
    negProbab = 0 #probability that the document is classified as negative
    
    testSet = set()

    for w in words:
        if w in self.vocabSet:
            if self.BOOLEAN_NB:
                if w not in testSet:
                    posProbab += math.log(self.TotalPos[w] + 1) #log of the numerator of the likelihood, with laplace smoothing to avoid log (0) problem for unseen data
                    posProbab -= math.log(self.pos_word_count + self.vocabCount) #log of the denominator of the likelihood, with laplace smoothing to avoid log (0) problem for unseen data
                    negProbab += math.log(self.TotalNeg[w] + 1) #log of the numerator of the likelihood, with laplace smoothing to avoid log (0) problem for unseen data
                    negProbab -= math.log(self.neg_word_count + self.vocabCount) #log of the denominator of the likelihood, with laplace smoothing to avoid log (0) problem for unseen data
                    testSet.add(w)
            else:
                posProbab += math.log(self.TotalPos[w] + 1) #log of the numerator of the likelihood, with laplace smoothing to avoid log (0) problem for unseen data
                posProbab -= math.log(self.pos_word_count + self.vocabCount) #log of the denominator of the likelihood, with laplace smoothing to avoid log (0) problem for unseen data
                negProbab += math.log(self.TotalNeg[w] + 1) #log of the numerator of the likelihood, with laplace smoothing to avoid log (0) problem for unseen data
                negProbab -= math.log(self.neg_word_count + self.vocabCount) #log of the denominator of the likelihood, with laplace smoothing to avoid log (0) problem for unseen data

    posProbab += math.log(self.numPosDocuments) - math.log(self.numTotalDocuments) #log of the numerator - log of denominator of prior
    negProbab += math.log(self.numNegDocuments) - math.log(self.numTotalDocuments) #log of the numerator - log of denominator of prior

    # Return class with highest probability
    if posProbab > negProbab:
        return 'pos'
    else:
        return 'neg'

  

  def addExample(self, klass, words):
    #To calculate prior, find out number of documents with labels as positive, negative and the total number of documents
    if klass == 'pos':
        self.numPosDocuments += 1
    elif klass == 'neg':
        self.numNegDocuments += 1
    
    self.numTotalDocuments += 1

    pos_bin = set() #Unique words for binary classifier, to see if it has occured or not
    neg_bin = set() #Unique words for binary classifier, to see if it has occured or not
    pos_bin_count = 0 #Count of unique words for binary classifier, to see if it has occured or not
    neg_bin_count = 0 #Count of unique words for binary classifier, to see if it has occured or not

    #count the number of occurrences of words in each class, and check if words occurs or not in case of Boolean NB, and add to set.
    for w in words:
        if klass == 'pos':
            if self.BOOLEAN_NB == True:
                if w not in pos_bin:
                    pos_bin.add(w)
                    pos_bin_count += 1
                    self.TotalPos[w] += 1
            else:
                self.pos_word_count += 1
                self.TotalPos[w] += 1
        elif klass == 'neg':
            if self.BOOLEAN_NB == True:
                if w not in neg_bin:
                    neg_bin.add(w)
                    neg_bin_count += 1
                    self.TotalNeg[w] += 1
            else:
                self.neg_word_count += 1
                self.TotalNeg[w] += 1
        #Add every unique word across all classes to get total unique words, needed for likelihood estimation
        if w not in self.vocabSet:
            self.vocabSet.add(w)
            self.vocabCount += 1
    
    if self.BOOLEAN_NB:
        self.pos_word_count += pos_bin_count
        self.neg_word_count += neg_bin_count




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
    """
     * Splits lines on whitespace for file reading
    """
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

  def train(self, split):
    for example in split.train:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      self.addExample(example.klass, words)


  def crossValidationSplits(self, trainDir):
    """Returns a list of TrainSplits corresponding to the cross validation splits."""
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
      splits.append(split)
    return splits
  
  def filterStopWords(self, words):
    """Filters stop words."""
    filtered = []
    for word in words:
      if not word in self.stopList and word.strip() != '':
        filtered.append(word)
    return filtered

def test10Fold(args, FILTER_STOP_WORDS, BOOLEAN_NB):
  nb = NaiveBayes()
  splits = nb.crossValidationSplits(args[0])
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = NaiveBayes()
    classifier.FILTER_STOP_WORDS = FILTER_STOP_WORDS
    classifier.BOOLEAN_NB = BOOLEAN_NB
    accuracy = 0.0
    for example in split.train:
      words = example.words
      classifier.addExample(example.klass, words)
  
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
    
    
def classifyDir(FILTER_STOP_WORDS, BOOLEAN_NB, trainDir, testDir):
  classifier = NaiveBayes()
  classifier.FILTER_STOP_WORDS = FILTER_STOP_WORDS
  classifier.BOOLEAN_NB = BOOLEAN_NB
  trainSplit = classifier.trainSplit(trainDir)
  classifier.train(trainSplit)
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
  FILTER_STOP_WORDS = False
  BOOLEAN_NB = False
  (options, args) = getopt.getopt(sys.argv[1:], 'fb')
  if ('-f','') in options:
    FILTER_STOP_WORDS = True
  elif ('-b','') in options:
    BOOLEAN_NB = True
  
  if len(args) == 2:
    classifyDir(FILTER_STOP_WORDS, BOOLEAN_NB,  args[0], args[1])
  elif len(args) == 1:
    test10Fold(args, FILTER_STOP_WORDS, BOOLEAN_NB)

if __name__ == "__main__":
    main()
