
import cv2
import numpy as np
import roi_merge as roi_
import util_funs as util


def get_rects(img_):
    region = []
    # 灰度化、滤波、sobel边沿检测后，将保留下来的边界通过形态学变化进行连接成块
    img = sobel_(img_.copy())
    img = morphological_(img)
    # 对所有block进行分析，保留可能的目标块，存入region中
    region = region + find_region(img)
    # 代码数字的颜色可能是“红”、“黑”、“蓝”。
    # 将目标颜色区域进行分离，形态学连接成块，保留可能的目标块。
    for i in range(3):
        # i=0:分类黑色； i=1：分类红色； i=2：分离蓝色
        img = color_(img_.copy(), i)
        img = morphological_(img)
        region = region + find_region(img)
    return list(set(region))


def sobel_(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    # 高斯平滑
    img = cv2.GaussianBlur(img, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
    img = cv2.equalizeHist(img)
    # 中值滤波
    median = cv2.medianBlur(img, 5)
    # Sobel算子，X方向求梯度
    sobel = cv2.Sobel(median, cv2.CV_8U, 1, 0, ksize=3)
    # 二值化
    ret, binary = cv2.threshold(sobel, 170, 255, cv2.THRESH_BINARY)
    return binary


def color_(img, flag):
    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # LowerBlue从左到右分别表示"black","red","red","blue"的hsv值
    LowerBlue = [np.array([0, 0, 0]), np.array([0, 43, 46]), np.array(
        [156, 43, 46]), np.array([100, 43, 46])]
    UpperBlue = [np.array([180, 255, 180]), np.array(
        [10, 255, 255]), np.array([180, 255, 255]), np.array([124, 255, 255])]
    if flag == 0:
        mask_ = cv2.inRange(HSV.copy(), LowerBlue[3], UpperBlue[3])
    if flag == 1:
        mask_ = cv2.inRange(HSV.copy(
        ), LowerBlue[1], UpperBlue[1]) + cv2.inRange(HSV.copy(), LowerBlue[2], UpperBlue[2])
    if flag == 2:
        mask_ = cv2.inRange(HSV.copy(), LowerBlue[0], UpperBlue[0])
    return mask_


def morphological_(img):
    # 膨胀和腐蚀操作的核函数
    element0 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    # 膨胀、腐蚀、再膨胀，数字连接成一个区块
    dilation = cv2.dilate(img, element0, iterations=1)
    erosion = cv2.erode(dilation, element0, iterations=1)
    dilation_ = cv2.dilate(erosion, element1, iterations=3)
    return dilation_


def find_region(img):
    # 图像的宽带和高度
    h_img, w_img = img.shape
    # 查找轮廓
    _, contours, hierarchy = cv2.findContours(
        img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 获取矩形框
    rect_list = []
    for i in range(len(contours)):
        cont_ = contours[i]
        # 找到boundingRect
        rect = cv2.boundingRect(cont_)
        rect_list.append(rect)
    # 筛选矩形框
    region = []
    print("Image shape:")
    print(w_img, '*', h_img)
    # print("Default lists:", rect_list, len(rect_list))
    for rect in rect_list:
        # 计算高和宽
        height = rect[3]
        width = rect[2]
        # 判断高度和宽带是否满足要求
        if (width < w_img or width > w_img/3 or height < h_img/50 or height > h_img/15):
            continue
        # 发票代码、号码，长宽比：8-80
        ratio = float(width) / float(height)
        if (ratio > 100 or ratio < 5):
            continue
        # 发票代码和发票号码在右上角
        if(rect[0] > w_img/2 or rect[1] > h_img/2):
            continue
        region.append(rect)
    return region
