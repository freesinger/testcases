with open('/Users/shanewang/Desktop/temp_fb.txt', 'r', encoding='gbk') as f:
    neib_pair = []
    for sentence in f:
        # print(sentence)
        neib_pair.extend([sentence.split()])
    # print(len(neib_pair))  
    result = []
    nodup_res = []
    for pair in neib_pair:
        cnt = 0          
        for i in range(len(neib_pair)):
            if pair == neib_pair[i][0:2]:
                cnt += 1
        pair.append(cnt)
        result.append(pair)

    result.sort()
    for i in result:
        if i not in nodup_res:
            nodup_res.append(i)
    
    nodup_res.sort()
    for i in nodup_res:
        if i[-1] > 1:
            print(i)