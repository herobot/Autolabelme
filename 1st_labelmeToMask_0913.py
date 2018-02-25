# coding=utf-8
import os
import re
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl

saved_count = 0
saved_count_512x512 = 0



def generateMask(json_folder,img_folder,dst_dir):

    dst_source_img_folder = dst_dir + "JPEGImages/"
    dst_mask_img_folder = dst_dir + "mask/"
    dst_handwrite_img_folder = dst_dir + "handwrite/"
    global saved_count


    if os.path.exists(dst_dir) == False:
        os.mkdir(dst_dir)
    if os.path.exists(dst_source_img_folder) == False:
        os.mkdir(dst_source_img_folder)

    if os.path.exists(dst_mask_img_folder) == False:
        os.mkdir(dst_mask_img_folder)

    if os.path.exists(dst_handwrite_img_folder) == False:
        os.mkdir(dst_handwrite_img_folder)




    with open(dst_dir + "readFromLabelmeTxt.log",'w') as logfile:  # write logfile
        fold_or_files = os.listdir(json_folder)
        for file in fold_or_files:
            file_name = file[:6]
            fined_anchors_rect = []
            with open(json_folder +  file, 'rb') as f:
                logfile.write("r: " + json_folder +  file +"\t{}".format(saved_count) +"\n")
                lines = f.read()
                image_path = img_folder + file_name + '.bmp'
                srcImg = cv2.imread(image_path)
                handwriteImg = srcImg.copy()
                img_W = srcImg.shape[1]
                img_H = srcImg.shape[0]
                raw_mask_img = np.zeros((img_H, img_W), np.uint8)

                raw_points = lines.split('},')
                point_lists = []
                for points in raw_points:
                    re_points = '(\d+\.\d+)+\,\s+(\d+\.\d+)+'
                    points = re.findall(re_points, points)
                    point_lists.append(points)

                    pts = []
                    for p in points:
                        x,y=p
                        pts.append([int(float(x)),int(float(y))])
                    cnt = []
                    cnt.append(pts)
                    array_pts = np.array(cnt)
                    cv2.drawContours(raw_mask_img, array_pts, 0, 255, cv2.FILLED)
                    cv2.drawContours(handwriteImg, array_pts, 0, (0,255,255), 2)


                # global saved_count
                str = '{:0>6}.jpg'.format(saved_count)
                saved_count += 1

                cv2.imwrite(dst_mask_img_folder + str, raw_mask_img)
                cv2.imwrite(dst_source_img_folder + str, srcImg)
                cv2.imwrite(dst_handwrite_img_folder + str, handwriteImg)

                print ("saved " + dst_mask_img_folder + str)
                logfile.write("saved " + dst_mask_img_folder + str + "\n\n\n")









def crop(project_dir):
    global saved_count_512x512
    if os.path.isdir(project_dir) == False:            os.mkdir(project_dir)
    with open(project_dir + "crop_readwrite.log", 'w') as logfile:



        crop_dst_dir = project_dir + "crop_512x512/"
        if os.path.isdir(crop_dst_dir) == False:os.mkdir(crop_dst_dir)
        dst_512x512_source_crop_img_folder = crop_dst_dir + "JPEGImages/"
        if os.path.exists(dst_512x512_source_crop_img_folder) == False:os.mkdir(dst_512x512_source_crop_img_folder)
        dst_512x512_mask_crop_img_folder = crop_dst_dir + "mask/"
        if os.path.exists(dst_512x512_mask_crop_img_folder) == False:os.mkdir(dst_512x512_mask_crop_img_folder)
        dst_512x512_handwrite_crop_img_folder = crop_dst_dir + "handwrite/"
        if os.path.exists(dst_512x512_handwrite_crop_img_folder) == False:os.mkdir(dst_512x512_handwrite_crop_img_folder)


        resize_dst_dir = project_dir + "resize_512x512/"
        if os.path.isdir(resize_dst_dir) == False:            os.mkdir(resize_dst_dir)

        dst_512x512_source_resize_img_folder = resize_dst_dir + "JPEGImages/"
        if os.path.exists(dst_512x512_source_resize_img_folder) == False:os.mkdir(dst_512x512_source_resize_img_folder)
        dst_512x512_mask_resize_img_folder = resize_dst_dir + "mask/"
        if os.path.exists(dst_512x512_mask_resize_img_folder) == False:os.mkdir(dst_512x512_mask_resize_img_folder)
        dst_512x512_handwrite_resize_img_folder = resize_dst_dir + "handwrite/"
        if os.path.exists(dst_512x512_handwrite_resize_img_folder) == False:os.mkdir(dst_512x512_handwrite_resize_img_folder)








        source_files = os.listdir(project_dir + "JPEGImages/")
        hand_write_files = os.listdir(project_dir + "handwrite/")
        mask_files = os.listdir(project_dir + "mask/")

        for i in range(len(source_files)):
            logfile.write("\n\nr: " + project_dir + "JPEGImages/" + source_files[i]  + '\t{}'.format(i)+ '\n')

            srcImg = cv2.imread(project_dir + "JPEGImages/" + source_files[i])
            handwriteImg = cv2.imread(project_dir + "handwrite/" + hand_write_files[i])
            mask_img = cv2.imread(project_dir + "mask/" + mask_files[i])

            img_H = mask_img.shape[0]
            img_W = mask_img.shape[1]

            roi_W = 512
            roi_H = 512
            for x in range(img_W / roi_W):
                for y in range(img_H / roi_H):
                    raw_mask_img_512x512 = mask_img[y * roi_H:y * roi_H + roi_H, x * roi_W:x * roi_W + roi_W]
                    raw_mask_img_512x512_test = raw_mask_img_512x512[(int)(roi_H * 0.2):(int)(roi_H * 0.8),
                                                (int)(roi_W * 0.2):(int)(roi_W * 0.8)]
                    n = np.amax(raw_mask_img_512x512_test)
                    if n > 0:
                        # global saved_count_512x512
                        str = '{:0>6}.jpg'.format(saved_count_512x512)
                        saved_count_512x512 += 1

                        img_512x512 = handwriteImg[y * roi_H:y * roi_H + roi_H, x * roi_W:x * roi_W + roi_W]
                        srcImg_512x512 = srcImg[y * roi_H:y * roi_H + roi_H, x * roi_W:x * roi_W + roi_W]
                        cv2.imwrite(dst_512x512_mask_crop_img_folder + str, raw_mask_img_512x512)
                        cv2.imwrite(dst_512x512_source_crop_img_folder + str, srcImg_512x512)
                        cv2.imwrite(dst_512x512_handwrite_crop_img_folder + str, img_512x512)

                        logfile.write("s: " + dst_512x512_handwrite_crop_img_folder + str + '\n')
                        print ("saved" + dst_512x512_handwrite_crop_img_folder + str)


            # global saved_count_512x512
            str = '{:0>6}.jpg'.format(saved_count_512x512)
            saved_count_512x512 += 1
            resize_srcImg = cv2.resize(srcImg, (512, 512))
            resize_handwriteImg = cv2.resize(handwriteImg, (512, 512))
            resize_mask_img = cv2.resize(mask_img, (512, 512))

            cv2.imwrite(dst_512x512_mask_resize_img_folder + str, resize_mask_img)
            cv2.imwrite(dst_512x512_source_resize_img_folder + str, resize_srcImg)
            cv2.imwrite(dst_512x512_handwrite_resize_img_folder + str, resize_handwriteImg)
            logfile.write("s: " + dst_512x512_handwrite_resize_img_folder + str + '\n')

# root1 =  "/media/gtx/data3T1/clothData/2017_HT/2017_07_27/"
# root2 =  "/media/gtx/data3T1/clothData/2017_HT/2017_07_27_2/"
# root3 =  "/media/gtx/data3T1/clothData/2017_HT/2017_08_03/"
# root4 = "/media/gtx/data3T1/clothData/2017_HT/2017_08_30/clothRed/"
# root5 = "E:/clothData/2017_09_07/clothRed/"
# root5 = "E:/clothData/redCloth/"
root5 = "E:/clothData/redTest/"

# dst_dir =  "/media/gtx/data3T1/clothData/2017_HT/total/"
# dst_dir_HT = "E:/clothData/2017_09_07/total/"
dst_dir_HT = "E:/clothData/redTest/total/"




#generateMask(root1,dst_dir)
#generateMask(root2,dst_dir)
#generateMask(root3,dst_dir)
# generateMask(root4+"lif/",root4+"source/",dst_dir)
generateMask(root5+"lif/",root5+"source/bmp/",dst_dir_HT)


# crop(dst_dir)
crop(dst_dir_HT)
print ("done")
