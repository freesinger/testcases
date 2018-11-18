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
                word = temp[0]
                proc_sentence.append(word)

            nebor_pair = []
            for pos in range(len(proc_sentence) - 1):
                nebor_pair.append((proc_sentence[pos], proc_sentence[pos + 1]))
            for elem in nebor_pair:
                tempresult.write(' '.join(str(w) for w in elem) + '\n')

def fre_analysis(temptext, res):
            result = []
            with open(temptext, 'r', encoding='gbk') as np:
                nebor_pair = np.readlines()
            for pair in nebor_pair:
                cnt = 0
                for cmp_pair in nebor_pair:
                    if pair == cmp_pair:
                        cnt += 1
                # str convert to tuple
                result.append(pair + ' ' + str(cnt))

            result = list(set(result))
            for i in result:
                res.write('(' + ', '.join(str(c) for c in i) + ') ' + '\n')

def main():
    with open(resdir + 'temp.txt', 'w', encoding='gbk') as tmp, open(resdir + 'result.txt', 'w', encoding='gbk') as res:
        doc = list(os.listdir(rootdir))
        for i in doc:
            text_process(rootdir + i, tmp)
        # fre_analysis(resdir + 'temp.txt', res)
        

if __name__ == '__main__':
    main()