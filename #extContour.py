#! /usr/bin/env python
# -*- coding: utf8 -*-

import re
import os
import sys
import string
from PIL import Image
import cv2
import numpy as np
from array import array
from PIL import Image
from math import sqrt
from scipy.spatial.distance import pdist,squareform



def edgeFind(img_path):
    #count = 0
    for item in os.listdir(img_path):
        if item.find(".jpg",1,len(item)) != -1:
            imgData = cv2.imread(item, -1)


    return 0

def pro_lut(grayimg):
    seek_table = np.zeros(256, dtype=grayimg.dtype)


    hist = cv2.calcHist([grayimg], [0], None, [256], [0.0, 255.0])
    minBinNo, maxBinNo = 0, 255
    for binNo, binValue in enumerate(hist):
        if binValue != 0:
            minBinNo = binNo
            break

    for binNo, binValue in enumerate(reversed(hist)):
        if binValue != 0:
            maxBinNo = 255 - binNo
            break
    print minBinNo, maxBinNo

    for i, v in enumerate(seek_table):
        if i < minBinNo:
            seek_table[i] = 0
        elif i > maxBinNo:
            seek_table[i] = 255
        else:
            seek_table[i] = int(255.0 * (i - minBinNo) / (maxBinNo - minBinNo) + 0.5)

    img_lut = cv2.LUT(grayimg, seek_table)
    return img_lut

def pro_lut_np(grayimg):
    # seek_table = np.zeros(256, dtype=grayimg.dtype)

    hist, bins = np.histogram(grayimg.flatten(), 256, [0, 255])
    cdf = hist.cumsum()
    cdf_m = np.ma.masked_equal(cdf,0)
    cdf_m = (cdf_m-cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
    cdf = np.ma.filled(cdf_m,0).astype('uint8')

    img_lut = cdf[grayimg]
    return img_lut

if __name__ == '__main__':
# 1. 原图
    img_path = "000014.bmp"
    img = cv2.imread(img_path)
    cv2.imwrite("#1_img.jpg", img)
    cv2.namedWindow("#1_img", cv2.WINDOW_NORMAL)
    cv2.imshow("#1_img",img)

    # img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # cv2.imwrite("#1_img_hsv.jpg",img_hsv)
    # cv2.namedWindow("#1_img_hsv", cv2.WINDOW_NORMAL)
    # cv2.imshow("#1_img_hsv",img_hsv)

    # (H, S, V) = cv2.split(img_hsv)
    # img_h = H + S
    # cv2.imwrite("#1_img_h.jpg",img_h)
    # cv2.namedWindow("#1_img_h", cv2.WINDOW_NORMAL)
    # cv2.imshow("#1_img_h",img_h)
    # cv2.cvtColor(img_h,cv2.COLOR_HLS2BGR)
    # cv2.cvtColor(img_h,cv2.COLOR_RGB2GRAY)

    # img_thread = cv2.threshold(img,125,255,cv2.THRESH_BINARY)
    # cv2.imwrite("#2_img_thread.jpg",img_thread)
    # cv2.namedWindow("#2_img_thread", cv2.WINDOW_NORMAL)
    # cv2.imshow("#2_img_thread",img_thread)
# 2. 灰度化
    img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    cv2.imwrite("#2_img_gray.jpg",img_gray)
    cv2.namedWindow("#2_img_gray", cv2.WINDOW_NORMAL)
    cv2.imshow("#2_img_gray",img_gray)
    # ret, thresh = cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# 3. 灰度值对比度拉升
#     img_lut = pro_lut(img_gray)
    img_lut = pro_lut_np(img_gray)
    cv2.imwrite("#3_img_lut.jpg",img_lut)
    cv2.namedWindow("#3_img_lut", cv2.WINDOW_NORMAL)
    cv2.imshow("#3_img_lut",img_lut)

# 4. 中值滤波
    img_med = cv2.medianBlur(img_lut,5)
    cv2.imwrite("#4_img_med.jpg", img_med)
    cv2.namedWindow("#4_img_med", cv2.WINDOW_NORMAL)
    cv2.imshow("#4_img_med", img_med)

# 5. OSTU阈值分割得到二值图
    ret, thresh = cv2.threshold(img_med,0,255,cv2.THRESH_OTSU)
    cv2.imwrite("#5_img_thresh.jpg",thresh)
    cv2.namedWindow("#5_img_thresh", cv2.WINDOW_NORMAL)
    cv2.imshow("#5_img_thresh",thresh)
# 6. 形态学处理
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(11,11))
    openedImg = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel)
    closedImg = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel)
    morphImg = closedImg
    # erodeImg = cv2.erode(thresh, None, iterations=3)
    # dilateImg = cv2.dilate(thresh, None, iterations=3)
    cv2.imwrite("#6_img_morphImg.jpg",morphImg)
    cv2.namedWindow("#6_img_morphImg", cv2.WINDOW_NORMAL)
    cv2.imshow("#6_img_morphImg",morphImg)



    cv2.waitKey()

    print 0
