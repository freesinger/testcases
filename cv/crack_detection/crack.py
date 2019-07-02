"""
Single crack length detection.
"""
import cv2
import numpy as np
import os
import shutil

RESULT = 'result.txt'

def distance(A, B):
    return np.power(np.power(A[0]-B[0], 2) + np.power(A[1]-B[1], 2), 1/2)

if os.path.dirname(os.path.realpath(__file__))+'/'+RESULT:
    os.remove(os.path.dirname(os.path.realpath(__file__))+'/'+RESULT)

for p in range(1, 10):
    Crack = cv2.imread('./pics/crack{:}.jpg'.format(p), cv2.IMREAD_GRAYSCALE)
    # cv2.imshow('Image', Crack)
    # cv2.waitKey()
    # print(Crack.shape)

    coo, coo_A, coo_B = [], [], []

    for i in range(Crack.shape[0]):
        for j in range(Crack.shape[1]):
            Crack[i, j] = 0 if Crack[i, j] < 50 else 1

    for i in range(Crack.shape[0]):
        for j in range(Crack.shape[1]-1):
            if Crack[i, j-1] == 1 and Crack[i, j] == 0:
                coo_A.append((i, j))
            if Crack[i, j] == 0 and Crack[i, j+1] == 1:
                coo_B.append((i, j))

    crack_lengths = []
    for i in coo_A:
        min_len = 512.0
        for j in coo_B:
            min_len = min(min_len, distance(i, j))
        crack_lengths.append(min_len)

    # max and mean
    crack_max = max(crack_lengths)
    crack_mean = np.mean(crack_lengths)
    print('Crack {2:}, Max: {0:.4f}, Mean: {1:.4f}'.format(crack_max, crack_mean, p))
    with open(RESULT, 'a', encoding='utf-8') as r:
        r.write('Crack {2:}, Max: {0:.4f}, Mean: {1:.4f}'.format(crack_max, crack_mean, p) + '\n')
# {black : 5538, white: 2556606}
# {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 244, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255}