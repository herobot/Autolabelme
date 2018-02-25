#! /usr/bin/env python
# -*- coding: utf8 -*-

# This file is used to rename image file.

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

class EdgePoint(object):
    def rename_image_file(self,path):
        # fileList = []
        count = 0
        for item in os.listdir(path):
            if item.find('.jpg', 0, len(item)) != -1:
                # fileList.append(item)
                newImgName = '{:0>6}.jpg'.format(count)
                src = Image.open(os.path.join(path, newImgName))
                src.resize((1024,1024)).save(os.path.join(path+'/resize/', newImgName))
                count += 1
                print item, 'change NAME ok'

    def find_edge_counters(self,path,current_jpg_count):
        contours_out = []  # 挑选过的一幅图像的所有包围圈的点----list
        for item in os.listdir(path):
            countImgName = '{:0>6}.jpg'.format(current_jpg_count)
            if item.find(countImgName, 0, len(item)) != -1:
                img = cv2.imread(os.path.join(path,countImgName))
                grayImg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
                thresh,binaryImg = cv2.threshold(grayImg,250,255,cv2.THRESH_BINARY)

                # kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7))
                # openedImg = cv2.morphologyEx(binaryImg,cv2.MORPH_OPEN,kernel)
                # closedImg = cv2.morphologyEx(openedImg,cv2.MORPH_CLOSE,kernel)
                erodeImg = cv2.erode(binaryImg, None, iterations=3)
                dilateImg = cv2.dilate(binaryImg, None, iterations = 3)
                # dilateImg = cv2.dilate(closedImg,None,iterations = 3)

                binary, contours, hierarchy = cv2.findContours(erodeImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                # binary, contours, hierarchy = cv2.findContours(dilateImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

                # cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
                # cv2.namedWindow("Contours", cv2.WINDOW_NORMAL)
                # cv2.imshow("Contours", img)
                # cv2.imwrite('Contours.jpg', binary)
                #
                # edges = cv2.Canny(binary, 0, 255)
                # cv2.imshow("edges", edges)
                # cv2.imwrite('cannyEdge.jpg', edges)

                for contour in contours:  # contours---->(list)  counter---->(ndarray)
                    area = cv2.contourArea(contour)
                    if area < 50:  # 200
                        continue

                    contour_out = []  # 单个包围圈的点
                    CUT_BLOCK = 48
                    for pt in contour:
                        x, y = pt[0]
                        if ((x % CUT_BLOCK == 0) or (y % CUT_BLOCK == 0)):
                            contour_out.append([[x, y]])
                            for point in contour_out:
                                x1, y1 = point[0]
                                a = np.abs(x1 - x)
                                b = np.abs(y1 - y)
                                # Dis = (np.square((x1 - x)) + np.square(y1 - y))   # 简单计算了欧式距离，可以用切比雪夫距离代替更准
                                Dis = max(a, b)
                                if (Dis < CUT_BLOCK) and (Dis != 0):
                                    contour_out.remove([[x, y]])
                                    break
                                else:
                                    continue

                    if len(contour_out) > 3: #点集数量大于3才能封闭成圈
                        temp = np.array(contour_out)
                        contours_out.append(temp)  # 把单个包围圈的点加入list

                # cv2.drawContours(img, contours_out, -1, (255, 0, 0), 2)
                # cv2.namedWindow("Contours_out", cv2.WINDOW_NORMAL)
                # cv2.imshow("Contours_out", img)
                #
                # contours_out_txt = open("contours_out.txt",'w')
                # contours_out_txt.write(str(contours_out))
                # contours_out_txt.close()

        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return contours_out #一张图片的所有点

if __name__ == '__main__':

    currentImgCount = 104
    jpgFilePath = 'E://clothData//2017_10_11//resultImage//original'
    # jpgFilePath = 'E:\\clothData\\2017_10_11\\clothRed\\source\\jpg'
    # jpgFilePath = 'E://clothData//2017_10_11//resultImage/'

    EP = EdgePoint()
    # EP.rename_image_file(jpgFilePath)
    EP.find_edge_counters(jpgFilePath,currentImgCount)
