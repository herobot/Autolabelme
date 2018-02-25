

pic_dir1 = "/media/gtx/data3T1/clothData/2017_HT/2017_07_27/2017_07_27_source"
mask_dir1 = "/media/gtx/data3T1/clothData/2017_HT/2017_07_27/2017_07_27_lif"

pic_dir2 = "/media/gtx/data3T1/clothData/2017_HT/2017_07_27_2/2017_07_27_2_source"
mask_dir2 = "/media/gtx/data3T1/clothData/2017_HT/2017_07_27_2/2017_07_27_2_lif"


pic_dir3 = "/media/gtx/data3T1/clothData/2017_HT/2017_08_03/2017_08_03_source"
mask_dir3 = "/media/gtx/data3T1/clothData/2017_HT/2017_08_03/2017_08_03_lif"



import glob
import os



def get_pairPics(pic,mask):

    def listFiles(dir):
        res = []
        for files in os.walk(dir):
            for file in files[2]:
                if ".jpg" or ".png" in file:
                    res.append(files[0] + file)
        return res


    pictures = listFiles(pic)
    raw_mask = listFiles(mask)
    masks=[]

    def getName(name):
        index = 0
        while index!=-1:
            index = name.find("/")
            name = name[index+1:]

        index = name.find(".")
        name = name[:index]
        return name

    for p in pictures:
        _p = getName(p)
        replicateCount = 0
        correspond_m = None
        for m in raw_mask:
            _m = getName(m)
            if _p == _m:
                correspond_m = m
                replicateCount +=1
        if replicateCount==1:
            masks.append(correspond_m)
        else:
            print ("mask and jps not matched")
    return pictures,masks



res1 = get_pairPics(pic_dir1,mask_dir1)
res2 = get_pairPics(pic_dir2,mask_dir2)
res3 = get_pairPics(pic_dir3,mask_dir3)

paired_results = res1[0]+res2[0]+res3[0], res1[1]+res2[1]+res3[1]


dst_dir = "/media/gtx/data3T/clothData/2017-8-16-FCN-Mask/total/JPEGImages/"
dst_mask = "/media/gtx/data3T/clothData/2017-8-16-FCN-Mask/total/masks/"
import cv2

for count,_jpg in enumerate(paired_results[0]):
    jpg_name = "{}.jpg".format(count)
    while(len(jpg_name)<len("000000.jpg")):
        jpg_name = '0'+jpg_name

    m = cv2.imread(paired_results[0][count])
    dst_jpg = dst_dir + jpg_name
    cv2.imwrite(dst_jpg,m);
    print ("saved "+dst_jpg)


    mask_name = "{}.png".format(count)
    while(len(mask_name)<len("000000.png")):
        mask_name = '0'+mask_name
    mask = cv2.imread(paired_results[1][count])
    dst_maks = dst_mask + mask_name
    cv2.imwrite(dst_maks,mask);
    print ("saved "+dst_maks)



print ('done')