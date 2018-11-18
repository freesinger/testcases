# -*- coding: utf-8 -*-

with open('/Users/shanewang/Desktop/train/01010204.txt', 'r', encoding='gbk') as f:
    for sentence in f:
        # sentence.rstrip('\n')
        sentence = sentence.split()
        proc_sentence = []
        for word in sentence:
            temp = word.split('/')
            word = temp[0]
            proc_sentence.append(word)
        neib_pair = []
        for pos in range(len(proc_sentence) - 1):
            #if proc_sentence[pos + 1] != '\n':
                #print([proc_sentence[pos], proc_sentence[pos + 1]])
            neib_pair.append((proc_sentence[pos], proc_sentence[pos + 1]))

        result = []
        # print(neib_pair)
        for pair in neib_pair:
            cnt = 0          
            for cmp_pair in neib_pair:
                if pair == cmp_pair:
                    cnt += 1
            result.append(pair + (cnt,))

        print(list(set(result)))
        