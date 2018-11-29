import os
import numpy as np

rootdir = '/Users/shanewang/Desktop/train/'
resdir = '/Users/shanewang/Desktop/results/'

# tag: frequency
tag = {}
# (tag, tag_next): frequency
pair_tag = {}
# (word, tag): frequency
word_tag = {}

def text_proc(text):
    with open(text, 'r', encoding='gbk') as t:
        s = t.readlines()
        for sentence in s:
            sentence = sentence.split()
            for word in sentence:
                if word == '<BOS>' or word == '<EOS':
                    continue
                temp = word.split('/')
                if temp[1] not in tag:
                    tag[temp[1]] = 1
                else:
                    tag[temp[1]] += 1
                tup = (temp[0], temp[1])
                if tup not in word_tag:
                    word_tag[tup] = 1
                else:
                    word_tag[tup] += 1
            for i in range(1, len(sentence) - 1):
                pretag = sentence[i].split('/')[1]
                curtag = sentence[i + 1].split('/')[1]
                tup = (curtag, pretag)
                if tup not in pair_tag:
                    pair_tag[tup] = 1
                else:
                    pair_tag[tup] += 1

def freq_analysis(dic):
    total = 0
    for i in dic:
        total += dic[i]
    for i in dic:
        dic[i] /= total

def init(firstword):
    temp = firstword.split('/')
    return tag[temp[1]] * word_tag[(temp[0], temp[1])]


