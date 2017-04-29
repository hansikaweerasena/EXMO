import numpy as np
import cv2

def rotateImage(image, angle):
    center=tuple(np.array(image.shape[0:2])/2)
    rot_mat = cv2.getRotationMatrix2D(center,angle,1.0)
    return cv2.warpAffine(image, rot_mat, image.shape[0:2],flags=cv2.INTER_LINEAR)


img = cv2.imread('1.jpg')

imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,120,200,cv2.THRESH_BINARY)
_,contours, hierarchy = cv2.findContours(thresh,1,2)



##canny_edge = cv2.Canny(thresh, 0, 0)
##
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(thresh,kernel,iterations = 1)


cv2.imshow('erosion',erosion)

kernel = np.ones((3,3),np.uint8)
dilation = cv2.dilate(erosion,kernel,iterations = 1)


cv2.imshow('dilation',dilation)


kernel = np.ones((15,15),np.uint8)
erosion2 = cv2.erode(dilation,kernel,iterations = 1)


##cv2.imshow('erosion2',erosion2)
##
##kernel = np.ones((3,3),np.uint8)
##dilation2 = cv2.dilate(erosion,kernel,iterations = 1)
##
##
##cv2.imshow('dilation2',dilation2)
##
##_,contours, hierarchy = cv2.findContours(dilation2,1,2)
##
##print len(contours)

for i, c in enumerate(contours):
    area = cv2.contourArea(c)
    approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
    
    if len(approx)==4:
        (x, y, w, h) = cv2.boundingRect(c)
        #print approx
        #im = cv2.drawContours(img,[c],0,(0,0,255),2)
        cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)
##        cv2.drawContours(img, c, -1, (0,255, 0),20)


##edges = cv2.Canny(imgray,50,150,apertureSize = 3)
##minLineLength = 100
##maxLineGap = 10
##lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
##for x1,y1,x2,y2 in lines[0]:
##    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)


cv2.imshow('thresh',thresh)




cv2.imshow('img',img)
##cv2.imshow('erosion',erosion)




#cv2.imshow('canny',canny_edge)

cv2.waitKey(0)
cv2.destroyAllWindows()
