'''
Created on 2015-04-18

@author: Shen Wang

play.py
'''

from nltk import ngrams
import random
import os

'''
process_file
	Inputs:
		filename: the path to file string
		ngram_value: the ngrams used
	Output: map from each word to the number of times it appears
'''
def process_file(filename, ngram_value):
    hist = {}
    fp = file(filename)

    text = fp.read()
    # text = text.lower()
    text = text.split()
    all_ngrams = find_ngrams(text, ngram_value)
    for gram in all_ngrams:
		hist[gram] = hist.get(gram, 0) + 1
    
    return hist

''' 
find_ngrams
	Input: a document of text, a number n
	Output: a set of tuples that respresents n-grams

'''

def find_ngrams(sentence_list, n):
	return ngrams(sentence_list, n)

'''
most_common
	Input: histogram
	Output:list of key-value pairs from histogram and sorts them in descending order by frequency

'''
def most_common(hist):
    t = []
    for key, value in hist.items():
        t.append((value, key))

    t.sort()
    t.reverse()
    return t

'''
print_most_common
	Input:
		histogram
		the number of the most commons to print
	Output:
		prints the most common

'''
def print_most_common(hist, num=10):
    t = most_common(hist)
    print 'The most common words are:'
    for freq, word in t[:num]:
        print word, '\t', freq

'''
WeightedPick
	Input:
		dictionary of keys and integer values as weights
	Outputs:
		a pick of a key based on the weighted values
'''
def WeightedPick(d):
    r = random.uniform(0, sum(d.itervalues()))
    s = 0.0
    for k, w in d.iteritems():
        s += w
        if r < s: return k
    return k

'''
PickNext
	Inputs:
		key_has: A tuple key of n-gram
		d: the histogram of key value pairs
		ngram_value: the ngram used
	Outputs:
		Takes a key and picks the next key from dictionary based on the last tuple value
		If no last tuple value exists, pick a random one
'''
def PickNext(key_has, d, ngram_value):
	new_dict = {}
	for key in d:
		if key[0] == key_has[ngram_value - 1]:
			new_dict[key] = d[key]

	if len(new_dict) > 0:
		new_key = WeightedPick(new_dict)
	else:
		new_key = WeightedPick(d)
	return new_key

'''
PickRandom
	Inputs:
		d: the histogram of key value pairs
	Output:
		a random weighted pick of the key from histgram
'''

def PickRandom(d):
	return WeightedPick(d)

'''
GenerateText
	Inputs:
		hist: the dictionary of histograms of ngrams
		n: length of sentence that you want to generate in words
		ngram_value: the ngram used
		ran: to generate randomint from 1-ran for random jumbling purposes
		variation: the threshold value between variation-ran which allows for randomness
	Output:
		a string that is generated from the histograms
'''

def GenerateText(hist, n, ngram_value, ran=100, variation=101):
	punctuations = '!?.'
	sentence = ''
	tup = random.choice(hist.keys())
	sentence += ' '.join(tup)

	while len(sentence) < n:
		if random.randint(1,ran) > variation:
			#This allows for more randomization in it :D
			tup = PickRandom(hist)
		else:
			tup = PickNext(tup, hist, ngram_value)
		sentence += ' '
		sentence += ' '.join(tup[1:])
		

	if sentence[-1] in punctuations:
		pass
	else:
		sentence += '.'
	return sentence

'''
IterateFolder
	Input:
		path: path to folder
		ngram_value: the ngrams to be used
	Output: a histogram of the file in ngram format
	Requires: import os
'''
def IterateFolder(path, ngram_value):
	books = []
	for filename in os.listdir(path):
		print filename #Mainly to show that its working, and what you included
		filename = path + filename
		temp = process_file(filename, ngram_value)
		books.append(temp)
	return books


'''
__main__

Runs the test with inputs and determines output file

'''
if __name__ == '__main__':
	books = []

	# Set all variables
	path = 'test_data/'
	path_to_ouput = 'output.txt'
	n = 2
	repeat = 2


	books = IterateFolder(path, n)

	hist = {}
	for thing in books:
		hist.update(thing)

	f = open(path_to_ouput, 'w')
	while repeat > 0:
		sentence = GenerateText(hist, 140, n)
		f.write(sentence + '\n\n')
		repeat = repeat - 1




