
#author:
#Tharunn

import pandas as py
import numpy as np
import sys,os
import re
import nltk
import collections
from nltk.corpus import stopwords
from nltk.corpus import swadesh
from math import log

# Method to read class names from the directory
def readDir(path):
    classlist = []
    i = 0;
    for path,subirs,files in os.walk(path):
        for name in subirs:
            if(i >= 5):
                break
               # i=0
            classlist.append(name)
            i = i + 1
    return classlist


# Method to find the vocabulary and count of the words in the training data
def Vocabulary(n):
    cachedStopWords = set(stopwords.words("english"))
    cachedCommonWords = set(swadesh.words('en'))
    removewords = cachedStopWords.union(cachedCommonWords)
    for i in classlist:
        local_cnt = collections.Counter()
        count = 0
        path = os.path.join(root,i)
        for path,subdirs,files in os.walk(path):
            for name in files:
                n += 1
                count += 1
                flag = 0
                f = open(os.path.join(path,name),"r")
                for line in f:
                    if flag == 1:
                        tokenizer = nltk.RegexpTokenizer(r'\w+')
                        tokens = tokenizer.tokenize(line)
                        filtered_word = [word.lower() for word in tokens if word.lower() not in removewords]
                        for k in filtered_word:
                            cnt[k] += 1
                            local_cnt[k] +=1
                    if ("Lines:" in line):
                        flag = 1
        Nc[i] = count
        List_cnt[i] = local_cnt
    return n
    

# Method used to train the classifier by storing all the probabilities
def trainNB():
    for i in classlist:
        for j in List_cnt[i]:
            cond_prob[j,i] = float((List_cnt[i][j]+1))/float((sum(List_cnt[i].values())+len(cnt)))
            
                    
#Method used to classify a test document to its appropriate class 
def testNB(doc_words):
    m = float('-inf')
    index = 0
    cls = "null"
    for i in Test_class:
        score = log(float(Nc[i])/float(N))
        for word in doc_words:
            try:
                score += log(cond_prob[word,i])
            except:
                score +=log(float(1)/float((sum(List_cnt[i].values())+len(cnt))))
        if score >= m:
            m=score
            cls = i
        index +=1
    return cls
       

# Method used to extract the words from each test document and run the test algorithm 
def test_util():
    count = 0
    error = 0
    cachedStopWords = set(stopwords.words("english"))
    cachedCommonWords = set(swadesh.words('en'))
    removewords = cachedStopWords.union(cachedCommonWords)
    for i in Test_class:
        path = os.path.join(test,i)
        for path,subdirs,files in os.walk(path):
            for name in files:
                doc_words = []
                flag = 0
                f = open(os.path.join(path,name),"r")
                for line in f:
                    if flag == 1:
                        tokenizer = nltk.RegexpTokenizer(r'\w+')
                        tokens = tokenizer.tokenize(line)
                        filtered_word = [word.lower() for word in tokens if word.lower() not in removewords>2]
                        for k in filtered_word:
                            doc_words.append(k)
                    if ("Lines:" in line):
                        flag = 1
                test_cls = testNB(doc_words)
                if ( i == test_cls):
                    count +=1
                else:
                    error +=1
                    count +=1
    print "Accuracy :",float((float(count-error)/float(count))*100)
            

root = sys.argv[1]
test = sys.argv[2]
classlist = readDir(root)
Test_class = readDir(test)
Nc = {}  
cnt = collections.Counter()
List_cnt = {}
cond_prob = {}
N = Vocabulary(0)
trainNB()
test_util()








# In[ ]:



