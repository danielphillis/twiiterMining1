#!!training text updated to new version
#------------------------------------------------------------------
# This code thankfully acknowledges the python from the book
# "Mining the Social Web 2nd Edition
# and the tutorials by Harrison on the youtube channel "sentdex"

# this code developed by daniel phillis with acknowledgements above
# SID 2110633, FAN phil0411
# 
#------------------------------------------------------------------

#------------------------------------------------------------
# well make out own text classifier for sentiment analysis
# it will try to classify positive and negative sentiment
# we utilise naive bayes algorithm
# ffrq dist is ordered form the most common words to the least

#pickle is a way we can save pytohn objects and basically save time
# no piclingis done in this version
#expect slow return of results - 5-10 mins !
#------------------------------------------------------------

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
#from nltk.corpus import movie_reviews
from nltk.corpus import opinion_lexicon
from nltk.corpus import words
from nltk.classify.scikitlearn import SklearnClassifier

import random
import time
import pickle

#scikit learn is more of an artificial learning machine toolkit
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode

class VoteClassifier(ClassifierI) :
        def __init__(self, *classifiers):
                #we will pass as arguments a list of classifiers tot his class for voting
                self._classifiers = classifiers

        def classify(self, features):
                votes = []
                for c in self._classifiers:
                        v = c.classify(features)# get the vote from each classifier 
                        votes.append(v)
                return mode(votes) #who go the most votes
        # recall mode is the value that appears most often in a set of data

        def confidence(self, features):
                votes = []
                for c in self._classifiers:
                        v = c.classify(features)
                        votes.append(v)
                        
                choice_votes = votes.count(mode(votes))
				# counts how many occurances of the most  popular votes
                confidence =  choice_votes / len(votes) #confidence of that vote, 
				#a certainty
                return confidence

                choice_votes = votes.count(mode(votes))
                
#-------------------------------------------------------------------------------
start = time.time()

short_pos = open('../short_reviews/positive_enc.txt','r').read().decode('utf-8')
#print word_tokenize(short_pos)

short_neg = open('../short_reviews/negative_enc.txt','r').read().decode('utf-8')
#print word_tokenize(short_neg)

docs = []

for r in short_pos.split('\n'):
	docs.append( (r, "pos"))

for r in short_pos.split('\n'):
	docs.append( (r, "neg"))

all_words = []

short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)

for w in short_pos_words:
	all_words.append(w.lower())

for w in short_neg_words:
	all_words.append(w.lower())

#print all_words
all_words = nltk.FreqDist(all_words) # we need the order provided by a FreqDist
# we wont focus on the values
# (ie the words not the freq associated with it)
# we will check on the top x000 words (values are number popularity)

word_features = list(all_words.keys()[:3000])#for the top 5000 words only

print('word_features is using the ' + str(len(word_features)) + ' most popular words...')
#print word_features

'''
find features function will
1) Remove duplicates from the input doc
2) Make a new dictionary called features
3) For each wordfrom allwords(top 5000),
the dictionary feature is populated with a word from the input doc set 
4) 
'''

def find_features(document):
        words = word_tokenize(document)
        features = {} #defines a dictionary
        for w in word_features: #the top 5000 words from all words
                features[w] = (w in words)# this creates the boolean value
#by evaluating (w in words)

        return features   # returns a dict with keys but not values     

'''find the features of the words fromthe opinion dataSet'''
##print("find features Results:")
##print(find_features('neg/cv000_29416.txt'))
##print(find_features(opinion_lexicon.words(opData)))
#this will convert the reviews words
#to the words with true or false paired with it

featureSets = [(find_features(rev), category) for (rev,category) in docs]
random.shuffle(featureSets)

#print featureSets

#print("##number of instances of the word 'stupid':")
#print(all_words["stupid"])

#These two sets must be different to avoid bias
trainingSet = featureSets[:5000] #before 10000 is 
testingSet = featureSets[5000:] # after 10000 is

# we will use a naive Bayes aka stupid bayes algorithm
# its very basic therefore we can scale it tovery large datasets
# and we can still get satisfactory results
# it is well known and sometimes out performs  
# more sophiticated classifiers

# Bayes theorem gives us a way to calculate the prob
# of a class given the data (posterior probability)
# 
# basically the Bayes algorithm is basically:
# likelyhood of something being positive is 
# posterior(liklihood) = (prior occurances)*(liklihood) /current evidence

#define classifier
#---------------------------------------------------------------------------

classifier = nltk.NaiveBayesClassifier.train(trainingSet)

#---------------------------------------------------------------------------

print("Vanilla Naive Bayes Algo accuracy%: ", 
      nltk.classify.accuracy(classifier, testingSet)*100)

#tell us the most popular words on both sides (pos and neg)
classifier.show_most_informative_features(15)
#---------------------------------------------------------------------------

MultinomialNB_classifier = SklearnClassifier( MultinomialNB() )
MultinomialNB_classifier.train(trainingSet)
print("MultinomialNaiveBayes Algo accuracy%: ", 
      nltk.classify.accuracy(MultinomialNB_classifier, testingSet)*100)


BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(trainingSet)
print("BernoulliNaiveBayes Algo accuracy%: ", 
      nltk.classify.accuracy(BernoulliNB_classifier, testingSet)*100)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(trainingSet)
print("LogisticRegression Algo accuracy%: ", 
      nltk.classify.accuracy(LogisticRegression_classifier, testingSet)*100)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(trainingSet)
print("StochGradientClassifier Algo accuracy%: ", 
      nltk.classify.accuracy(SGDClassifier_classifier, testingSet)*100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(trainingSet)
print("LinearSVC Algo accuracy%: ", 
      nltk.classify.accuracy(LinearSVC_classifier, testingSet)*100)

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(trainingSet)
print("NuSVC Algo accuracy%: ", 
      nltk.classify.accuracy(NuSVC_classifier, testingSet)*100)

#---------------------------------------------------------------------------
# from these diff classifiers - we will make another that votes on the
# best scores this will give us some reliability and higher accuracy

voted_classifier = VoteClassifier(
	classifier, #the regular classifier
    MultinomialNB_classifier,
    BernoulliNB_classifier,
    LogisticRegression_classifier,
    SGDClassifier_classifier,# stochastic gradient descent
    LinearSVC_classifier,
    NuSVC_classifier
)


#save_classifier = open('naive.pickle','wb')#save as bytes
#pickle.dump(classifier, save_classifier)
#save_classifier.close()


#classifier_f = open('naive.pickle','rb')
#classifier = pickle.load(classifier_f)
#classifier_f.close()


print("Voted Classifier Accuracy %: ",
      nltk.classify.accuracy(voted_classifier, testingSet)*100)

print ("Classification:", voted_classifier.classify(testingSet[0][0]),
       "Confidence%:", voted_classifier.confidence(testingSet[0][0])*100)
#[0][0] here is just for testing

print ("Classification:", voted_classifier.classify(testingSet[1][0]),
       "Confidence%:", voted_classifier.confidence(testingSet[1][0])*100)

print ("Classification:", voted_classifier.classify(testingSet[2][0]),
       "Confidence%:", voted_classifier.confidence(testingSet[2][0])*100)

print ("Classification:", voted_classifier.classify(testingSet[3][0]),
       "Confidence%:", voted_classifier.confidence(testingSet[3][0])*100)

print ("Classification:", voted_classifier.classify(testingSet[4][0]),
       "Confidence%:", voted_classifier.confidence(testingSet[4][0])*100)

print ("Classification:", voted_classifier.classify(testingSet[5][0]),
       "Confidence%:", voted_classifier.confidence(testingSet[5][0])*100)

#---------------------------------------------------------------------------

#What did we do
end = time.time()
ex_time = end - start
print("ex_time =  " + str(ex_time) + " s")

