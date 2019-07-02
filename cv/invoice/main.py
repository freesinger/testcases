import cv2
import numpy as np
import os
import errno
import roi_merge as roi_
import util_funs as util
from get_rects import *

DIRPATH = os.path.dirname(__file__) + '/results/'
ROOT = '/Users/shanewang/Desktop/Codes/testcases/cv/invoice/images/'


def Slice(image, imgid):
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    region = get_rects(img)
    print(region, len(region))
    
    roi_solve = roi_.Roi_solve(region)
    roi_solve.rm_inside()
    roi_solve.rm_overlop()
    region = roi_solve.merge_roi()
    region = util.sort_region(region)
    # region = util.get_targetRoi(region)
    print(region)
    
    # print(os.path.dirname(__file__))
    # region = [(107, 413, 318, 23), (110, 410, 318, 29), (58, 194, 312, 22), (249, 241, 217, 23), (189, 194, 184, 23)]
    for i in range(len(region)-1):
        rect2 = region[i]
        w1, w2 = rect2[0], rect2[0]+rect2[2]
        h1, h2 = rect2[1], rect2[1]+rect2[3]
        box = [[w1, h2], [w1, h1], [w2, h1], [w2, h2]]
        cv2.drawContours(img, np.array([box]), 0, (0, 255, 0), 1)
        cv2.imwrite(DIRPATH+str(imgid)+'/slice_{}.jpg'.format(str(i)), img[h1:h2, w1:w2])
    cv2.imwrite(DIRPATH+str(imgid)+'/image.jpg', img)    
    # cv2.imshow('img', img)
    # cv2.waitKey(0)


for i in range(4):
    try:
        if not os.path.exists(DIRPATH+'{}'.format(i+1)):
            os.mkdir(DIRPATH+'{}'.format(i+1))
    except Exception as e:
        if e.errno != errno.EEXIST:
            raise
        pass
    img = cv2.imread(ROOT+"{}.png".format(i+1))
    Slice(img, i+1)
