import numpy as np
import matplotlib.pyplot as plt
from skimage import morphology, measure, color, data, io
import os
import shutil

RESULT = 'result_v2.txt'

if os.path.isfile(os.path.dirname(os.path.realpath(__file__))+'/'+RESULT):
    os.remove(os.path.dirname(os.path.realpath(__file__))+'/'+RESULT)

def distance(A, B):
    return np.power(np.power(A[0]-B[0], 2) + np.power(A[1]-B[1], 2), 1/2)

for p in range(1, 10):
    Crack = data.imread('./pics/crack{}.jpg'.format(p), as_gray=True)
    mask = Crack < np.full(Crack.shape, 0.9)
    # io.imshow(Crack)
    # plt.show()
    # print(Crack.shape)
    # plt.plot(Crack)
    # plt.show()
    # print(Crack)
    # print(mask)

    # for i in range(Crack.shape[0]):
    #     for j in range(Crack.shape[1]):
    #         Crack[i, j] = 0 if Crack[i, j] < 0.9 else 1

    labels = measure.label(mask, connectivity=2)
    # t = {}
    # for i in labels:
    #     for j in i:
    #         if j not in t:
    #             t[j] = 1
    #       else:
    #           t[j] += 1
    # print(t)
    region_info = measure.regionprops(label_image=labels)
    # for i in region_info:
        # print(i.area)
    Crack = color.label2rgb(labels)
    # print('Region number: {}'.format(labels.max()+1))
    Crack = morphology.remove_small_objects(mask, min_size=300, connectivity=2)

    # fig = plt.figure(figsize=(6,6))
    # io.imshow(Crack)
    # plt.show()

    # ll = measure.label(Crack, connectivity=2)
    # print('Region later: {}'.format(ll.max()+1))

    def getCooByRow(image_mask):
        coo_A, coo_B = [], []
        for i in range(image_mask.shape[0]):
            for j in range(image_mask.shape[1]-1):
                if image_mask[i, j-1] == False and image_mask[i, j] == True:
                    coo_A.append((i, j))
                if image_mask[i, j] == True and image_mask[i, j+1] == False:
                    coo_B.append((i, j))
        return coo_A, coo_B

    def getCooByCol(image_mask):
        coo_A, coo_B = [], []
        for i in range(image_mask.shape[1]):
            for j in range(image_mask.shape[0]-1):
                if image_mask[j-1, i] == False and image_mask[j, i] == True:
                    coo_A.append((i, j))
                if image_mask[j, i] == True and image_mask[j+1, i] == False:
                    coo_B.append((i, j))
        return coo_A, coo_B

    def ratio(image_mask):
        for i in range(image_mask.shape[0]):
            find = False
            for j in range(image_mask.shape[1]-1):
                if image_mask[i, j-1] | image_mask[i, j] == True:
                    start = [i, j]
                    find = True
                    break;
            if find:
                break
        for i in range(image_mask.shape[0]-1,0,-1):
            find = False
            for j in range(image_mask.shape[1]-1,0,-1):
                if image_mask[i, j-1] | image_mask[i, j] == True:
                    end = [i, j]
                    find = True
                    break;
            if find:
                break
        return (end[1]-start[1]) / (end[0]-start[0])


    tangle = ratio(Crack)
    print('Ratio: {:.4f}'.format(tangle))
    if tangle >= -1 and tangle <= 1:
        print('Get coordinates by Column')
        coor_A, coor_B = getCooByCol(Crack)
    else:
        print('Get coordinates by Row')
        coor_A, coor_B = getCooByRow(Crack)

    crack_lengths = []
    for i in coor_A:
        min_len = 512.0
        for j in coor_B:
            min_len = min(min_len, distance(i, j))
        crack_lengths.append(min_len)

    # max and mean
    crack_max = max(crack_lengths)
    crack_mean = np.mean(crack_lengths)
    print('Max: {0:.4f}, Mean: {1:.4f}'.format(crack_max, crack_mean))
    with open(RESULT, 'a', encoding='utf-8') as r:
        r.write('Crack {2:}, Max: {0:.4f}, Mean: {1:.4f}'.format(crack_max, crack_mean, p) + '\n')