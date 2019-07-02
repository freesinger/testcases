import cv2
import numpy as np


def get_u_d_l_r(rect_):
    # 获取rect的上下左右边界值
    upper_, down_ = rect_[1], rect_[1] + rect_[3]
    left_, right_ = rect_[0], rect_[0] + rect_[2]
    return upper_, down_, left_, right_

# region排序。flag=1时：从上到下；flag=0时：从左到右
def sort_region(region, flag=1):
    temp = []
    region_new = []
    for rect in region:
        temp.append(rect[flag])
    temp_sort = sorted(temp)
    for height_ in temp_sort:
        index_ = temp.index(height_)
        region_new.append(region[index_])
    return region_new

# 判断上下两个相邻框框是否为发票代码、发票号码
def judge_(rect_0, rect_1):
    u_d_l_r_0 = get_u_d_l_r(rect_0)
    u_d_l_r_1 = get_u_d_l_r(rect_1)
    # 两个rect上边界之间的距离不超过box_height的四倍
    distance_ = rect_1[1] - rect_0[1]
    box_height = float(rect_0[3] + rect_1[3])/2
    # 上边框的右边界值更大
    if (distance_ > 0 and distance_ < box_height*3 and rect_0[0]+rect_0[2] > rect_1[0]+rect_1[2]):
        return True
    return False

# 获取 “发票代码”、“发票号码”的区域
def get_targetRoi(region):
    if len(region) > 1:
        # 按照从上到下排序
        new_region = sort_region(region)
        for i in range(len(new_region)-1):
            if judge_(new_region[i], new_region[i+1]):
                return [new_region[i], new_region[i+1]]
