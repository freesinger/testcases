import os

rootdir = '/Users/shanewang/Desktop/train/'
resdir = '/Users/shanewang/Desktop/'

def text_process(text, tempresult):
    with open(text, 'r+', encoding='gbk') as f:
        for sentence in f:
            sentence = sentence.split()
            proc_sentence = []
            for word in sentence:
                temp = word.split('/')
                if temp[1] != 'w':
                    word = temp[0]
                    proc_sentence.append(word)

            nebor_pair = []
            for pos in range(len(proc_sentence) - 1):
                nebor_pair.append((proc_sentence[pos], proc_sentence[pos + 1]))
            for elem in nebor_pair:
                tempresult.write(' '.join(str(w) for w in elem) + '\n')

def fre_analysis(temptext, res):
    neb_pair = []
    with open(temptext, 'r', encoding='gbk') as np:
        for sentence in np:
            neb_pair.extend([sentence.split()])

    res = []
    nodup_res =[]
    for pair in neb_pair:
        cnt = 0
        for i in range(len(neb_pair)):
            if pair == neb_pair[i][0:2]:
                cnt += 1
        pair.append(cnt)
        res.append(pair)

    res.sort()
    for i in res:
        if i not in nodup_res:
            nodup_res.append(i)

    nodup_res.sort()
    for i in nodup_res:
        if i[-1] > 5:
            print(i)

def main():
    with open(resdir + 'temp.txt', 'w', encoding='gbk') as tmp, open(resdir + 'result.txt', 'w', encoding='gbk') as res:
        doc = list(os.listdir(rootdir))
        for i in doc:
            text_process(rootdir + i, tmp)
        fre_analysis(resdir + 'temp_fb.txt', res)
        

if __name__ == '__main__':
    main()