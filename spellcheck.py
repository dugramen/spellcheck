# This is the final program
from ast import arg
from multiprocessing.dummy import Array
import sys
import re
from tokenize import Number
from typing import List
import requests
import time
import math
from collections import Counter
from random import sample

try:
    import nltk
    from nltk.metrics.distance import (
        edit_distance,
        jaccard_distance,
    )
    from nltk.util import ngrams
except:
    print("Nltk is not installed. Program will still work but cannot use standard 'Edit Distance' or 'Jaccard Distance'")

#full_text = requests.get("https://www.gutenberg.org/files/2701/2701-0.txt").text.lower() # <-- This is Moby Dick
full_text = requests.get("https://norvig.com/big.txt").text.lower() # <---- A bigger body of text is better

book_words = re.findall('\w+',full_text) # Return words with letters only

Words = set(book_words)

word_freq = {}  
word_freq = Counter(book_words)  
 
probs = {}
total_word_count = sum(word_freq.values())
for i in word_freq.keys():
    probs[i] = word_freq[i]/total_word_count



# Loading a list of english words
def load_words():
    all_words = requests.get("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt").text
    ls = all_words.split()    
    valid_words = set(ls)
    #print(ls[:10])
    return valid_words

english_words = load_words()

# Norvig spell-checker. Get all combinations within 1 edit
def edits1(word): 
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

# Get all combinations within 2 edits
def edits2(word): 
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))



def edit_candidates(word, distance = 2):
    candidates = [set() for i in range(distance + 1)]
    for w in Words:
        e = edit_distance(w, word)
        if e <= distance:
            candidates[e].add(w)
    i = -1
    for c in candidates:
        i+=1
        if len(c) != 0:
            return c
    return {word}

def jaccard_candidates(word, grams = 2, percentage = .3):
    candidates = [set() for i in range(11)]
    for w in Words:
        e = jaccard_distance(set(ngrams(w, grams)), set(ngrams(word, grams)))
        candidates[math.floor(e*10)].add(w)
    for c in candidates:
        if len(c) != 0:
            return c
    return {word}

def edit_candidates_norvig(word):
    if word in english_words:
        return {word}
    candidates = {e for e in edits1(word) if e in english_words}
    #candidates = edits1(word).intersection(english_words)
    if len(candidates) != 0:
        return candidates
    
    candidates = {e for e in edits2(word) if e in english_words}
    #candidates = edits2(word).intersection(english_words)
    if len(candidates) != 0:
        return candidates
    return {"---"}


def jaccard_correction(word):
    candidates = jaccard_candidates(word, 1)
    return get_correction(candidates, word)

def jaccard_bigrams_correction(word):
    candidates = jaccard_candidates(word)
    return get_correction(candidates, word)

def edit_correction(word):
    assert(edit_candidates)
    candidates = edit_candidates(word)
    return get_correction(candidates, word)

def norvig_correction(word):
    candidates = edit_candidates_norvig(word)
    return get_correction(candidates, word)

# Choose most popular word from given candidates
def get_correction(candidates, word):
    cword = -1
    cmax = -1
    for c in candidates:
        if cword == -1:
            cword = c
        
        if c not in probs:
            continue
        if probs[c] >= cmax:
            cmax = probs[c]
            cword = c
    return cword

# For scoring accuracy
def build_error_map():
    error_corpus = requests.get("https://www.dcs.bbk.ac.uk/~roger/wikipedia.dat").text.lower()
    error_list = error_corpus.split()
    key = ""
    map = {}
    for w in error_list:
        if w[0] == "$":
            key = re.sub(r'\W+', '', w)
        else:
            w = w.lower()
            if w in map:
                map[w].add(key)
            else:
                map[w] = {key}
    #print("{} test words".format(len(map)))
    return map

# Evaluates how long it takes to correct 100 random words
def evaluate(func_list, count = 100):
    error_map = build_error_map()
    error_sample = sample([*error_map.keys()], count)

    for (key, func) in func_list:
        t = time.time()
        score = 0
        for error in error_sample:
            correction = error_map[error]
            prediction = func(error)
            if prediction.lower() in correction:
                score += 1
        print(key.capitalize())
        print("   Guessed {} out of {} words correctly in {} seconds".format(score, len(error_sample), time.time() - t))
    print()

def run(methods):
    sentence = input("-> ").lower()
    if not sentence:
        return
	
    splits = sentence.split()
    for (method_name, method) in methods:
        print(method_name.replace('-', ' ').capitalize() + ":\n ", end=" ")
        for split in splits:
            print(method(split), end=" ")
        print("", end="\n")
    
    print("")
    run(methods)


def main():
    args = sys.argv[1:]
    methods = [("norvig", norvig_correction)]
    
    method_map = {
        "jaccard": jaccard_correction,
        "jaccard-bigrams": jaccard_bigrams_correction,
        "edit": edit_correction,
    }

    all = "all" in args
    for item in method_map.items():
        if all or item[0] in args:
            methods.append(item)

    if len(args) > 0 and args[0] in {"-evaluate", "-eval"}:
        if len(args) > 1 and args[1].isnumeric():
            evaluate(methods, int(args[1]))
        else:
            evaluate(methods)
    else:
        run(methods)

main()