import os
import numpy as np

rootdir = '/Users/shanewang/Desktop/train/'
resdir = '/Users/shanewang/Desktop/results/'

# tag: frequency
tag = {}
# (currenet_tag, previous_tag): frequency
pair_tag = {}
# (word, tag): frequency
word_tag_freq = {}
# word: [tags]
word_tag = {}
# store sentences without tag
proc_sentence = []


def text_proc(text):
    # s = text.readlines()
    for sentence in text:
        sentence = sentence.split()[1:-1]
        # tag = {}
        # word_tag_freq = {}
        for word in sentence:
            temp = word.split('/')
            if temp[1] not in tag:
                tag[temp[1]] = 1
            else:
                tag[temp[1]] += 1
            tup = (temp[0], temp[1])
            if tup not in word_tag_freq:
                word_tag_freq[tup] = 1
            else:
                word_tag_freq[tup] += 1
        # pair_tag = {}
        for i in range(1, len(sentence) - 3):
            pretag = sentence[i].split('/')[1]
            curtag = sentence[i + 1].split('/')[1]
            tup = (curtag, pretag)
            if tup not in pair_tag:
                pair_tag[tup] = 1
            else:
                pair_tag[tup] += 1
        # word-tag = {}
        for word in sentence:
            temp = word.split('/')
            if temp[0] not in word_tag:
                word_tag[temp[0]] = [temp[1]]
            elif temp[1] not in word_tag[temp[0]]:
                word_tag[temp[0]].append(temp[1])
        # proc_sentence = []
        for p in range(len(sentence)):
            sentence[p] = sentence[p].split('/')[0]
        proc_sentence.append(sentence)

def freq_analysis(dic):
    total = 0
    for i in dic:
        total += dic[i]
    for i in dic:
        dic[i] /= total

def init(firstword):
    tagset = word_tag[firstword]
    curval = 0
    for t in tagset:
        curval += tag[t] * word_tag_freq[(firstword, t)]
    return curval
    
def calculate(preword, curword):
    curval = 0
    p_tagset = word_tag[preword]
    curtagset = word_tag[curword]
    for cur in curtagset:
        for pre in p_tagset:
            if not pair_tag.__contains__((cur, pre)):
                pair_tag.update({(cur, pre): 0})
            else:
                curval += pair_tag[(cur, pre)] * word_tag_freq[(curword, cur)]
    return curval

def forwardHMM(sentence):
    value = []
    for i in range(len(sentence) - 1):
        if i == 0:
            PI = init(sentence[0])
            value.append(PI)
        else:
            temp = calculate(sentence[i], sentence[i + 1])
            value.append(temp)
    return(np.prod(value))

def main():
    with open(rootdir + '01010101.txt', 'r', encoding='gbk') as t:
        s = t.readlines()
        text_proc(s)
        # print(proc_sentence, tag, pair_tag, word_tag_freq)
        freq_analysis(tag)
        freq_analysis(pair_tag)
        freq_analysis(word_tag_freq)
        print("Process Done!")
        # print(tag, pair_tag, word_tag_freq, word_tag)

        for sentence in proc_sentence:
            print(pow(forwardHMM(sentence), 0.5))
        

if __name__ == "__main__":
    main()