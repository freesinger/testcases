import os

rootdir = '/Users/shanewang/Desktop/train/'
resdir = '/Users/shanewang/Desktop/results/'
# store result of frequences of nebor pairs

# store results
dict_res = {}


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
            for pos in range(len(proc_sentence) - 1):
                single_npair.append((proc_sentence[pos], proc_sentence[pos + dist]))
    return single_npair

def fre_calculate(curtext, dict):
    for pair in curtext:
        if not dict.__contains__(pair):
            dict[pair] = 1
            # dict_pair.update({pair : 1})
        else:
            dict[pair] += 1

def filter_result(dict):
    filtresult = []
    sorted_res = sorted(dict.items(), key = lambda k: k[1])
    # res.append([pair, num] for pair, num in dict_pair())
    for i in reversed(sorted_res):
        if i[1] > 100:
            filtresult.append(i)
    return filtresult

def distance_frequence(curpair, step):
    """
    :type pair: tuple
    :rtype: dict
    """
    pair = curpair[0]
    value = curpair[1]
    if not dict_res.__contains__(pair):
        dict_res.update({pair : [value]})
    elif step == 0:
        return dict_res
    else:


def main():
    # with open(resdir + '1_a.txt', 'w', encoding='gbk') as res:
    doc = list(os.listdir(rootdir))     
    for i in doc:
        if i == '.DS_Store':
            doc.remove(i)
    dict_pair = {}
    for i in range(len(doc)):
        fre_calculate(text_process(rootdir + doc[i], 1), dict_pair)
    print(filter_result(dict_pair))
    # print(type(res[0][0][0]), type(res[0][1]))

if __name__ == '__main__':
    main()
        