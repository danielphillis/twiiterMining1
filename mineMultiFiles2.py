import sys
import subprocess
from subprocess import call
import time
import datetime
import twitter
import io
import os
from os import listdir
from os.path import isfile, join

import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from prettytable import PrettyTable
from collections import Counter

import argparse
parser = argparse.ArgumentParser(description='Short sample app')
# Declare an argument (`--algo`), telling that the corresponding value should be stored in the `algo` field, and using a default value if the argument isn't given
parser.add_argument('--path', action="store", dest='path', 
	default='../output/leg/aug/samsung/')
# Now, parse the command line arguments and store the values in the `args` variable
args = parser.parse_args()# Individual arguments can be accessed as attributes...
#print("defualt path arg:" + args.path)

#------------------------------------------------------------------
def analyse_content(data, keywords, size, entityThreshold=3):
	#in this file the data is a list not a dictionary
	#Optimisation
	if len(data) == 0:
		print("No data to analyze")
		return

	stop_Words = stopwords.words("english")
	#camel case convention is broken to accentuate custom var over nltk variable

	customStopWords = [
						"Galaxy","Samsung","Note","replies","retweets",
						"Retweet","Reply","Edge","http","iPhone","S7","7","Sep",
						"More","Like","Aug"]

	punc = ["-",":","...","@","#",".",",","?"]
	nums = ["1","2","3","4","5","6","7","8","9","0"," ","\t","\t\t"]

	stop_Words += customStopWords
	stop_Words += punc

	#data = clean(data)
	size = 10
	c = Counter(data).most_common(size)
	# Compute frequencies *with a dictionary (tuples)
	tups = [ (k,v) for (k,v) in c if v >= entityThreshold and k not in stop_Words]

	#print tups #debug

	#pt is suitable for console display but not for writing a csv to disk
	pt = PrettyTable(field_names=['Entity', 'Count'])	
	[ pt.add_row(kv) for kv in tups ]
	pt.align['Entity'], pt.align['Count'] = 'l', 'r' # Set column alignment
	print pt

	# for each item in the keywords dict, count the re-occurances ie a 
	# Freq Dist for a specific subset
	for w in data:
		for k in keywords:
			if ('' +k) in ('' + w):
				#keywords[k] = keywords[k] + 1 #increase the value of key k
				pass
	
	#print "keywords"
	#print keywords #prints each word to a new line	

	return keywords#dictionary
#------------------------------------------------------------------        
# clean(items)
# clean accepts type list, outputs type list
# clean detects adjectives using NLTK Natural Language tool kit
# (www.nltk.org) to help narrow down sentiment
# clean removes nltk.stopwords
# clean converts all elements in the input list to lowercase 
# clean ignores hashtags (#example) when building output list
# clean ignores twitter usernames (@username) when building output list
# clean also gives a before and after count of elements

def clean(items):
	start = time.time()
	print("cleaning...")
	#this still has the twitter meta data structure
	before = len(items)

	stop_words = stopwords.words("english")
	#print stop_words
	
	punc = ["\'","!","-","|",".",",","?"] 
	#custom exclusions
	stop_words += ["RT","rt","the","he","He","of","in","is",
					"his","His","a","&amp"]

	count = 0
	total = len(items)
	for item in items:
		count += 1
		low = item.lower()
		items.remove(item)		
		#j = adjective, r = adverb, v = verb
		allowedTypes = ["J"]
		if low in (stop_words):# or punc):
			items.remove(low)
		else:
			print(low)
			
			print(str(count) + "/" + str(total))
			items.append(low)
		#if low not in stop_words:
			#pos = nltk.pos_tag([low])#pos = part of speech ie JJ for adjective
			#print("pos" +  pos[1][0])
			#for w in pos:
				#detect adjectives
				#if w[1][0] in allowedTypes:#and (w[1][0] != '#'): #is w an 	
				#adjective but not a hashtag
				#print 'adjective detected: ' + w[0]
				#items.append(w)	#w[0] is thw word as opposed to the POS 

	cleaned = []

	#remove hashtags and twitter usernames from reuslts
	for i in items:
		if (i[0] != '#') or (i[0] !='@'):
			#filter out hashtags and twitter 	usernames
			cleaned.append(i)

	after = before - len(cleaned)
	print ('words scrubbed away:' + str(after))
	#print cleaned
	end = time.time()
	exec_time = end - start
	#------------------------------------------------------------------        
	print ('cleanTime(sec): ' + str(int(exec_time)))

	return cleaned
#------------------------------------------------------------------    
# f is file handle
# fil is file name for printing

def stripPath(fileName):
	print("stripping path...")
	print("old fileName:" + fileName)

	#strip readPath and return just the fileName
	oldPath = fileName.split("/")
	#print("old path pieces = " + str(oldPath))
	pathSize = len(oldPath)
	fileName = oldPath[pathSize-1]

	#strip txt extension
	fl = len(fileName)	#print(fileName[:fl-1-3])	
	if str(fileName[(fl-4):]) == '.txt':# 4 chars in ".txt"
		fileName = fileName[:fl-4]#print("extension removed:" + fileName)
	print("new fileName:" + fileName)
	return fileName
#--------------------------------------------------------------------------
def writeCSVDict(fileName, tuples):
	print("writing csv...")	
	#if file exits already, open and append vaues to correct keys
	#add total count
	ext = ".csv"

	#strip path and txt extension
	fileName = stripPath(fileName)
	
	fil = str(fileName) + ext
	fileName += ext
	#print len(tuples)
	#read existing values to append to
	'''
	if io.open('{0}'.format(fileName),'a', encoding ='utf-8'):
		with io.open('{0}'.format(fileName),'a', encoding ='utf-8') as f:
			for i in f:
				print i
	'''
	total = 0

	with io.open('{0}'.format(fileName),'a', encoding ='utf-8') as f:
		for (k,v) in tuples.iteritems(): #
			total += v
			f.write(unicode(str(k) + "\t\t" + str(v) + "\n"))
		#f.write(unicode("\ntotal specified keywords found:\t" + str(total) + "\n"))
	f.close()
	print("* WroteFile :" + fil)


#------------------------------------------------------------------    

# timing of search, clean and output
start = time.time()

#usage
queries = ["#samsung","#Samsung",
			"#SamsungGalaxyNote7", 
			"#Note7",
			#"#GalaxyNote7Edge",
			"#Note7Edge",
			"#GalaxyNote7"
			]

#EXAMPLE QUERIES
#queries = ["#apple", "#Apple", "#iPhone7", "#iPhone"]
#queries += ["#iWatch"]
#queries = ["Note7", "SamsungGalaxyNote7", "Galaxy Note7"]
#queries = ["iWatch"]
#queries = ["trump"]

#load keywords form file
keywordPath = '~/Documents/social/py/mining/'

pos_keywords_f = open((keywordPath + 'sam_sent_pos'),'r').read().decode('utf-8')
pos_keys = word_tokenize(pos_keywords_f)
#assigned scores of 0 to all keys


keywords = {#dictionary
	"explo":0,
	"fire":0,
	"smok":0,
	"recall":0,
	"stop":0,
	"shelved":0,
	"disastor":0
}

#keywords ={"reply":0}
#count = 100
search_results = []
size = 25
v = 18 #optional version identifier suffix for fileName
#path = "../output/leg/aug/samsung/"
#path no longer hardcoded, but taken from Cmd Line args
#ie use python multiMine1.py --path /my/New/Path/

path = args.path

files = [f for f in listdir(path) if (isfile(join(path, f)))]
#and (str(f[(len(f)-4):]) == ".txt"))]
print files

for fileName in files:
	print("processing " + fileName + "...")
	if str(fileName[(len(fileName)-4):]) == ".txt":

		#f = unicode(f,errors='ignore')

		f = path + fileName
		tweetFile = open(str(f),'r').read().decode('utf-8')
		#tweetFile = open(f,'r').read()
		search_results = word_tokenize(tweetFile)
		#print "length of results:",len(search_results)

		# additive process
		keywords = analyse_content(search_results, keywords, size)
		#(analyse_content prints a 	prettyTable)

#returns a dictionary?/array of tuples for writing a FREQ DIST	
writeCSVDict("merged", keywords) #file gets the query name
#------------------------------------------------------------------        
# timing - Ideally collect into an array of times and print at the end 
# of a multi query
end = time.time()
exec_time = end - start
#------------------------------------------------------------------        
print ('elapsedTime(sec): ' + str(int(exec_time)))

#end
