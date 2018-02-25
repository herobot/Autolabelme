import os
import re
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
import pylab as pl
import math

def generateRectForxml(project_dir):
    if not os.path.isdir(project_dir):
        os.mkdir(project_dir)

    src_dir = project_dir + "JPEGImages"
    if os.path.exists(src_dir) == False:
        os.mkdir(src_dir)

    mask_dir = project_dir + "mask/"
    if os.path.exists(mask_dir) == False:
        os.mkdir(mask_dir)

    label_txt_folder = project_dir + "Boxlabels/"
    if not os.path.isdir(label_txt_folder):
        os.mkdir(label_txt_folder)

    # handwrite_dir = project_dir + "handwrite/"
    # if os.path.exists(handwrite_dir) == False:
    #     os.mkdir(handwrite_dir)

    testdir="E:/clothData/redTest/total/resize_512x512/mask"
    k = os.listdir(testdir)
    print k

    mask_jpgs = os.listdir(mask_dir)
    jpegs = os.listdir(src_dir)

    for mask in mask_jpgs:
        bFindOut = False
        for jpg in jpegs:
            if mask[:6] == jpg[:6]:
                bFindOut = True
                break
        if bFindOut == False:
            print mask + " is not matched"

    # imags = []
    # titles=[]
    # for i in range(12):
    #    jpg = mask_dir+mask_jpgs[i]
    #    img = cv2.imread(jpg)
    #    imags.append(img)
    #    titles.append(mask_jpgs[i])
    # for i in range(12):
    #    plt.subplot(3,4,i+1)
    #    plt.imshow(imags[i])
    #    plt.title(titles[i])
    # plt.show()


    with open(project_dir+"MaskToRectTxt.log",'w') as logfile:
        for mask in mask_jpgs:
            logfile.write("r: " + mask_dir + mask+"\n")
            img = cv2.imread(mask_dir + mask)
            img_file_name = src_dir + mask.replace(".jpg", ".jpg")
            label_name = label_txt_folder + mask.replace(".jpg", ".txt")
            save_img_name = label_txt_folder + mask.replace(".jpg", ".jpg")

            jpgImg = cv2.imread(img_file_name)
            if img.size == 0:
                raise Exception(img_file_name + " is not found")
                continue

            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            cv2.imshow("src", img)
            cv2.waitKey(1);
            ret, img = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)

            CUT_BLOCK = 30

            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if ((i % CUT_BLOCK == 0) or (j % CUT_BLOCK == 0)):
                        img[i][j] = 0

            # kernel = np.ones([1,1],np.uint8)
            # img = cv2.morphologyEx(img,cv2.MORPH_ERODE,kernel=kernel,iterations=1)

            #contours = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # binary = img
            # showImg = np.zeros([img.shape[0], img.shape[1], 3], np.uint8)
            # contours = cv2.findContours(img, cv2.RETR_TREE|cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # for contour in contours[1]:
            #    contour_out = []
            #    for pt in contour:
            #        x, y = pt[0]
            #        contour_out.append([x, y])
            #
            #        contours_out = []
            #
            #
            # contours_out.append(contour_out)
            # numpy_contours = np.array(contours_out)
            # cv2.drawContours(showImg, numpy_contours, 0, 255, cv2.FILLED)



            binary = img
            contours = cv2.findContours(img, cv2.RETR_TREE | cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[1]
            showImg = np.zeros([img.shape[0], img.shape[1], 3], np.uint8)
            cv2.drawContours(showImg, contours, -1, (255, 255, 255), 1)
            cv2.imshow("showImg", showImg)
            cv2.waitKey(1)

            availableRectAndArea = []
            for contour in contours:
                areaCount = cv2.contourArea(contour)
                if areaCount >= 0 and areaCount < img.size * 0.5:
                    res = contour, areaCount
                    availableRectAndArea.append(res)


            def mergedClosedArea(rectAndArea):
                mergedAvailableRectAndArea = []
                b_continue = True
                while b_continue:
                    b_continue = False
                    for a_from_src in rectAndArea:
                        if a_from_src[1] < CUT_BLOCK * CUT_BLOCK:
                            distance = 1e10
                            a_closed_tuple = None
                            a_closed_idx = -1
                            for b in rectAndArea:
                                if np.all(a_from_src[0]==b[0]):
                                    continue
                                for pt_a in a_from_src[0]:
                                    for pt_b in b[0]:
                                        x_dist = pt_a[0][0]-pt_b[0][0]
                                        y_dist = pt_a[0][1]-pt_b[0][1]
                                        dist = math.sqrt(x_dist * x_dist + y_dist * y_dist)
                                        if dist < distance:
                                            distance = dist
                                            a_closed_tuple = b

                            if a_closed_tuple==None:
                                if len(rectAndArea)>1:
                                    raise Exception("rectAndArea greate than 1 should find the closed")
                                continue

                            pts_a = a_from_src[0]
                            pts_b = a_closed_tuple[0]
                            list_a = list(pts_a[:])
                            list_b = list(pts_b[:])
                            list_a.extend(list_b)
                            merged_ab = np.array(list_a)
                            rect = cv2.boundingRect(np.array(merged_ab, np.int32))

                            b_too_slim = False
                            if rect[2] > 5 * rect[3] or rect[3] > 5 * rect[2] or (
                                            rect[2] > 1.5 * CUT_BLOCK and rect[3] > 1.5 * CUT_BLOCK):
                                b_too_slim = True

                            if distance < CUT_BLOCK * 2 and a_closed_tuple != -1 and b_too_slim == False:
                                showImg = np.zeros([img.shape[0], img.shape[1], 3], np.uint8)
                                cv2.drawContours(showImg,merged_ab[np.newaxis,...], 0, (random.randrange(0, 125), random.randrange(0, 125), random.randrange(0, 125)), 2)
                                cv2.drawContours(showImg,pts_b[np.newaxis,...], 0, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), 1)
                                cv2.drawContours(showImg,pts_a[np.newaxis,...], 0, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), 1)
                                cv2.imshow("TinyMerged", showImg)
                                cv2.waitKey(1)

                                res_area = cv2.contourArea(merged_ab)
                                res = merged_ab, cv2.contourArea(merged_ab)

                                for v in range(len(rectAndArea)):
                                    if np.all(rectAndArea[v][0]==a_from_src[0]) and np.all(rectAndArea[v][1]==a_from_src[1]):
                                        del rectAndArea[v]
                                        break
                                for v in range(len(rectAndArea)):
                                    if np.all(rectAndArea[v][0]==a_closed_tuple[0]) and np.all(rectAndArea[v][1]==a_closed_tuple[1]):
                                        del rectAndArea[v]
                                        break
                                rectAndArea.append(res)
                                b_continue = True
                if len(rectAndArea)<1:
                    raise Exception("We do not accept the perfect images now")

                return rectAndArea




            mergedClosedArea(availableRectAndArea)

            showImg = np.zeros([img.shape[0], img.shape[1], 3], np.uint8)

            for rect in availableRectAndArea:
                cv2.drawContours(showImg, np.array(rect[0]), 0, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), 1)
            cv2.imshow("TinyMerged", showImg)
            cv2.waitKey(1)

            anchorRect = []
            for PtsRect in availableRectAndArea:
                points = []
                for pt in PtsRect[0]:
                    x = pt[0]
                    points.append(x)
                points = np.array(points)
                rect = cv2.boundingRect(points)
                pt1 = rect[0], rect[1]
                pt2 = pt1[0] + rect[2], pt1[1] + rect[3]
                color = (random.randrange(0, 125), random.randrange(0, 125), random.randrange(0, 125))
                cv2.rectangle(jpgImg, pt1, pt2, color, 3)
                anchorRect.append((pt1, pt2))

            # cv2.imshow("finnal", jpgImg)
            # cv2.imwrite(save_img_name, jpgImg)
            k = cv2.waitKey(1000)
            if k != -1:
                cv2.waitKey(0)
                cv2.waitKey(0)
                cv2.waitKey(0)
                cv2.waitKey(0)

            logfile.write("w: " + label_name + "\n\n")
            with open(label_name, 'w') as f:
                f.write("{}\n".format(len(anchorRect)))
                for anchor in anchorRect:
                    f.write("target {} {} {} {}\n".format(anchor[0][0], anchor[0][1], anchor[1][0], anchor[1][1], ))


# picture_root1 = "/media/gtx/data3T1/clothData/2017_HT/total/crop_512x512/"
# picture_root2 = "/media/gtx/data3T1/clothData/2017_HT/total/resize_512x512/"
# picture_root2 = "E:/clothData/redCloth/total/resize_512x512/"
picture_root2 = "E:/clothData/redTest/total/resize_512x512/"
#generateRectForxml(picture_root1)
generateRectForxml(picture_root2)

print ('done')
raw_input("done")












































































































