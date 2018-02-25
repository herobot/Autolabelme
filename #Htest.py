#! usr/bin/env python
# _*_ coding:utf-8 _*_

import numpy as np
import cv2
# from numpy import *

def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),100,(255,0,0),-1)


img = np.zeros((512,512,3),np.uint8)
# cv2.line(img,(0,0),(234,234),(0,0,255),3)
# cv2.rectangle(img,(55,55),(234,234),(0,0,255),3)
# cv2.ellipse(img,(55,55),(234,234),0,0,100,200,-1)
font = cv2.FONT_HERSHEY_PLAIN
cv2.putText(img, "labelme", (0, 50), font, 7, (255,255,255), 2, cv2.LINE_AA)
cv2.imwrite("#HT_TEST.jpg", img)
cv2.namedWindow("#HT", cv2.WINDOW_NORMAL)
cv2.imshow("#HT", img)





cv2.waitKey(0)