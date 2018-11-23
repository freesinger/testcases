import os

rootdir = '/Users/shanewang/Desktop/train/'
resdir = '/Users/shanewang/Desktop/results/'
# store result of frequences of nebor pairs
dict_pair = {}
# store results
dict_res = {}
doc = list(os.listdir(rootdir))

def text_process(text, dist):
    single_npair = []
    with open(text, 'r', encoding='gbk') as f:
        for sentence in f:
            sentence = sentence.split()
            proc_sentence = []
            for word in sentence:
                temp = word.split('/')
                if temp[1] != 'w':
                    word = temp[0]
                    proc_sentence.append(word)
            if dist >= 0:           
                for pos in range(len(proc_sentence) - 1):
                    if pos + dist < len(proc_sentence):
                        single_npair.append((proc_sentence[pos], proc_sentence[pos + dist]))
            else:
                for pos in range(len(proc_sentence) - 1)[::-1]:
                    if pos + dist >= 0:
                        single_npair.append((proc_sentence[pos], proc_sentence[pos + dist]))
    return single_npair

# nebor frequence calc
def fre_calculate(curtext, dict):
    for pair in curtext:
        if not dict.__contains__(pair):
            dict[pair] = 1
            # dict_pair.update({pair : 1})
        else:
            dict[pair] += 1

def filter_result(dict, judge):
    filtresult = []
    sorted_res = sorted(dict.items(), key = lambda k: k[1])
    for i in reversed(sorted_res):
        # print(i[1], type(i[1]))
        if i[1] > judge:
            filtresult.append(i)
    return filtresult

"""
def distance_frequence(curpair, step):
    '''
    :type pair: tuple
    '''
    pair = curpair[0]
    value = curpair[1]
    if not dict_res.__contains__(pair):
        dict_res.update({pair : [value]})
    elif step == 0:
        return
    else:
        for i in range(len(doc)):
            tmp_pair = {}
            step_res = text_process(rootdir + doc[i], step)
            fre_calculate(step_res, tmp_pair)
            if tmp_pair.__contains__(pair):
                # dict_res[pair] += tmp_pair[pair]
                dict_res[pair].append(tmp_pair[pair])
            else:
                # dict_res[pair] += 0
                dict_res[pair].append(0)
"""

def main():
    # with open(resdir + '1_a.txt', 'w', encoding='gbk') as res:
    for i in doc:
        if i == '.DS_Store':
            doc.remove(i)
    for step in range(-5, 6, 1):
        for i in range(len(doc)):
            fre_calculate(text_process(rootdir + doc[i], step), dict_pair)
        one_res = filter_result(dict_pair, 100)
        print(one_res)

    """   
    for i in dict_pair:
        distance_frequence(i, 1)
    """
        
    # print(dict_res)
    

if __name__ == '__main__':
    main()
        