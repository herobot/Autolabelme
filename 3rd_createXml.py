#!/usr/bin/env python

import os
import sys
import cv2
import glob
from itertools import islice
from xml.dom.minidom import Document




def create_test_train_trainval_val(root_dir):
    labels = root_dir + 'Boxlabels/'
    imgpath = root_dir + 'JPEGImages/'
    xmlpath_new = root_dir + 'Annotations/'
    foldername = 'VOC2007'


    if not os.path.isdir(labels):        os.mkdir(labels)
    if not os.path.isdir(imgpath):        os.mkdir(imgpath)
    if not os.path.isdir(xmlpath_new):        os.mkdir(xmlpath_new)
    fileNames =[]
    for walk in os.walk(labels):
        for each in walk[2]:
            if ".txt" in each:
                fileNames.append(each)



    for i in range(len(fileNames)):
        fileNames[i] = fileNames[i].replace(".txt","")

    test_rate = 0.1

    test_file_name=[]
    rest_in_train_step=[]
    for i in range(len(fileNames)):
        if i < len(fileNames)*test_rate:
            test_file_name.append(fileNames[i])
        else:
            rest_in_train_step.append(fileNames[i])

    val_in_train_rate = 0.2
    val_in_train_file_name=[]
    train_in_train_file_name=[]
    for i in range(len(rest_in_train_step)):
        if i < len(fileNames)*val_in_train_rate:
            val_in_train_file_name.append(rest_in_train_step[i])
        else:
            train_in_train_file_name.append(rest_in_train_step[i])
    if not os.path.isdir(root_dir+"ImageSets/Main/"):
        if not os.path.isdir(root_dir):
            os.mkdir(root_dir)
        if not os.path.isdir(root_dir+"ImageSets/"):
            os.mkdir(root_dir+"ImageSets/")
        if not os.path.isdir(root_dir+"ImageSets/Main/"):
            os.mkdir(root_dir+"ImageSets/Main/")


    with open(root_dir+"ImageSets/Main/test.txt",'w') as f:
        for name in test_file_name:
            f.write("{}\n".format(name))

    with open(root_dir+"ImageSets/Main/train.txt",'w') as f:
        for name in train_in_train_file_name:
            f.write("{}\n".format(name))


    with open(root_dir+"ImageSets/Main/val.txt",'w') as f:
        for name in val_in_train_file_name:
            f.write("{}\n".format(name))


    with open(root_dir+"ImageSets/Main/trainval.txt",'w') as f:
        for name in rest_in_train_step:
            f.write("{}\n".format(name))

    print(root_dir+"Imagesets/Main/bala bala is done")

def create(root_dir):

    labels = root_dir + 'Boxlabels'
    imgpath = root_dir + 'JPEGImages/'
    xmlpath_new = root_dir + 'Annotations/'
    foldername = 'VOC2007'

    if not os.path.isdir(labels):
        os.mkdir(labels)
    if not os.path.isdir(imgpath):
        os.mkdir(imgpath)
    if not os.path.isdir(xmlpath_new):
        os.mkdir(xmlpath_new)

    for walk in os.walk(labels):
        for each in walk[2]:
            if ".txt" not in each:
                continue

            def insertObject(doc, datas):
                obj = doc.createElement('object')
                name = doc.createElement('name')
                name.appendChild(doc.createTextNode(datas[0]))
                obj.appendChild(name)
                pose = doc.createElement('pose')
                pose.appendChild(doc.createTextNode('Unspecified'))
                obj.appendChild(pose)
                truncated = doc.createElement('truncated')
                truncated.appendChild(doc.createTextNode(str(0)))
                obj.appendChild(truncated)
                difficult = doc.createElement('difficult')
                difficult.appendChild(doc.createTextNode(str(0)))
                obj.appendChild(difficult)
                bndbox = doc.createElement('bndbox')

                xmin = doc.createElement('xmin')
                xmin.appendChild(doc.createTextNode(str(datas[1])))
                bndbox.appendChild(xmin)

                ymin = doc.createElement('ymin')
                ymin.appendChild(doc.createTextNode(str(datas[2])))
                bndbox.appendChild(ymin)
                xmax = doc.createElement('xmax')
                xmax.appendChild(doc.createTextNode(str(datas[3])))
                bndbox.appendChild(xmax)
                ymax = doc.createElement('ymax')
                if '\r' == str(datas[4])[-1] or '\n' == str(datas[4])[-1]:
                    data = str(datas[4])[0:-1]
                else:
                    data = str(datas[4])
                ymax.appendChild(doc.createTextNode(data))
                bndbox.appendChild(ymax)
                obj.appendChild(bndbox)
                return obj

            fidin = open(walk[0] + '/' + each, 'r')
            objIndex = 0

            for data in islice(fidin, 1, None):
                objIndex += 1
                data = data.strip('\n')
                datas = data.split(' ')
                if 5 != len(datas):
                    print 'bounding box information error'
                    continue

                pictureName = None
                for walkfolder in os.walk(imgpath):
                    for imgfile in walkfolder[2]:
                        if each[:6] in imgfile:
                            pictureName = imgfile
                            break
                imageFile = imgpath + pictureName
                img = cv2.imread(imageFile)
                imgSize = img.shape
                if 1 == objIndex:
                    xmlName = each.replace('.txt', '.xml')
                    f = open(xmlpath_new + xmlName, "w")
                    doc = Document()
                    annotation = doc.createElement('annotation')
                    doc.appendChild(annotation)

                    folder = doc.createElement('folder')
                    folder.appendChild(doc.createTextNode(foldername))
                    annotation.appendChild(folder)

                    filename = doc.createElement('filename')
                    filename.appendChild(doc.createTextNode(pictureName))
                    annotation.appendChild(filename)

                    source = doc.createElement('source')
                    database = doc.createElement('database')
                    database.appendChild(doc.createTextNode('My Database'))
                    source.appendChild(database)
                    source_annotation = doc.createElement('annotation')
                    source_annotation.appendChild(doc.createTextNode(foldername))
                    source.appendChild(source_annotation)
                    image = doc.createElement('image')
                    image.appendChild(doc.createTextNode('flickr'))
                    source.appendChild(image)
                    flickrid = doc.createElement('flickrid')
                    flickrid.appendChild(doc.createTextNode('NULL'))
                    source.appendChild(flickrid)
                    annotation.appendChild(source)

                    owner = doc.createElement('owner')
                    flickrid = doc.createElement('flickrid')
                    flickrid.appendChild(doc.createTextNode('NULL'))
                    owner.appendChild(flickrid)
                    name = doc.createElement('name')
                    name.appendChild(doc.createTextNode('target'))
                    owner.appendChild(name)
                    annotation.appendChild(owner)

                    size = doc.createElement('size')
                    width = doc.createElement('width')
                    width.appendChild(doc.createTextNode(str(imgSize[1])))
                    size.appendChild(width)
                    height = doc.createElement('height')
                    height.appendChild(doc.createTextNode(str(imgSize[0])))
                    size.appendChild(height)
                    depth = doc.createElement('depth')
                    depth.appendChild(doc.createTextNode(str(imgSize[2])))
                    size.appendChild(depth)
                    annotation.appendChild(size)

                    segmented = doc.createElement('segmented')
                    segmented.appendChild(doc.createTextNode(str(0)))
                    annotation.appendChild(segmented)
                    annotation.appendChild(insertObject(doc, datas))
                else:
                    annotation.appendChild(insertObject(doc, datas))
            try:
                f.write(doc.toprettyxml(indent='    '))
                f.close()
                fidin.close()
            except:
                pass


if __name__ == '__main__':
    # root_dir1 = "/media/gtx/data3T1/clothData/2017_HT/total/crop_512x512/"
    # root_dir1 = "E:/clothData/redCloth/total/crop_512x512/"
    # root_dir2 = "/media/gtx/data3T1/clothData/2017_HT/total/resize_512x512/"
    root_dir2 = "E:/clothData/redCloth/total/resize_512x512/"

    # create(root_dir1)
    create(root_dir2)

    # create_test_train_trainval_val(root_dir1)
    create_test_train_trainval_val(root_dir2)
    print ("done")
    exit
