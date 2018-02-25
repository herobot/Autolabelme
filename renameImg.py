#! /usr/bin/env python
# -*- coding: utf8 -*-

# This file is used to rename image file.

import re
import os
import sys
import string
from PIL import Image
import cv2


def find_lif_file(path):
    # fileList = []
    global count
    for item in os.listdir(path):
        if item.find('.lif', 0, len(item)) != -1:
            # fileList.append(item)
            newImgName = '{:0>6}.lif'.format(count)
            os.rename((os.path.join(path, item)), os.path.join(path, newImgName))
            count += 1
            print item, 'change LIF NAME ok'


def find_image_file_bmp(path):
    # fileList = []
    global count
    for item in os.listdir(path):
        if item.find('.bmp', 0, len(item)) != -1:
            # fileList.append(item)
            newImgName = '{:0>6}.bmp'.format(count)
            os.rename((os.path.join(path, item)), os.path.join(path, newImgName))
            count += 1
            print item, 'change NAME ok'

def find_image_file_jpg(path):
    # fileList = []
    global count
    for item in os.listdir(path):
        if item.find('.jpg', 0, len(item)) != -1:
            # fileList.append(item)
            newImgName = '{:0>6}.jpg'.format(count)
            os.rename((os.path.join(path, item)), os.path.join(path, newImgName))
            count += 1
            print item, 'change NAME ok'

def rename_image_file_4M(bmpPath, jpgPath): # 4Mb/pic
    # fileList = []
    global count
    for item in os.listdir(bmpPath):
        newImgName = '{:0>6}.jpg'.format(count)
        if item.find('.bmp', 0, len(item)) != -1:
            try:
                Image.open(os.path.join(bmpPath, item)).save(os.path.join(jpgPath, newImgName))
            except IOError:
                print " Can't Convert! ", item

            count += 1
            print item, 'change FORM ok'
#
def rename_image_file_10M(bmpPath, jpgPath): # 10Mb/pic
    global count
    for item in os.listdir(bmpPath):
        newImgName = '{:0>6}.jpg'.format(count)
        if item.find('.bmp', 0, len(item)) != -1:
            try:
                bmpImg = cv2.imread(os.path.join(bmpPath, item))
                cv2.imwrite(os.path.join(jpgPath, newImgName), bmpImg)
            except IOError:
                print " Can't Convert! ", item

            count += 1
            print item, 'change FORM ok'

def resize_image_file(path):
    # fileList = []
    global count
    for item in os.listdir(path):
        if item.find('.jpg', 0, len(item)) != -1:
            # fileList.append(item)
            newImgName = '{:0>6}.jpg'.format(count)
            src = Image.open(os.path.join(path, newImgName))
            src.resize((4096,4096)).save(os.path.join(path+'/resize/', newImgName))
            count += 1
            print item, 'change NAME ok'

if __name__ == '__main__':

    count = 0

    # imgFilePath = 'E:\\clothData\\2017_08_03'
    bmpFilePath = 'E:/clothData/2017_11_16/source/bmp'
    # bmpFilePath = 'E:/clothData/2017-10-26/clothRed/source/bmp'
    # bmpFilePath = 'E:/clothData/clothTest/org'
    jpgFilePath = 'E:/clothData/2017_11_16/source/jpg'
    # jpgFilePath = 'E:/clothData/2017-10-26/clothRed/source/jpg'
    # jpgFilePath = 'E:/clothData/2017_11_07_redsilk/source/jpg'
    # lifFilePath = 'E:/clothData/2017_10_11/clothRed/lif'
    # lifFilePath = 'E:/clothData/2017_11_21/lif'
    # lifFilePath = 'E:/clothData/2017_11_07_redsilk/lif'
    # find_lif_file(lifFilePath)
    # find_image_file_bmp(bmpFilePath)
    # find_image_file_jpg(jpgFilePath)
    # resize_image_file(jpgFilePath)
    rename_image_file_4M(bmpFilePath, jpgFilePath)
    # rename_image_file_4M(bmpFilePath, jpgFilePath)
