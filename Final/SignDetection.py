import numpy as np
import cv2


def getLargestContour(img,largestIndex):
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,50,150,cv2.THRESH_BINARY)
    _,contours, hierarchy = cv2.findContours(thresh,1,2)

    areaArray = []
    count = 1

    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        areaArray.append(area)

    #first sort the array by area
    sorteddata = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)

    #find the nth largest contour [n-1][1], in this case 2
    if (len(sorteddata) - largestIndex > 0) :
        largestcontour = sorteddata[largestIndex - 1][1]
    else:
        largestcontour = None
    return largestcontour;


img = cv2.imread('cell2c.jpg')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

height, width, channels = img.shape

ret,thresh = cv2.threshold(gray,70,255,0)

_,contours,h = cv2.findContours(thresh,1,2)

##print len(contours)

####for cnt in contours:
####    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
####    print len(approx)
####    if len(approx)==5:
####        print "pentagon"
####        cv2.drawContours(img,[cnt],0,255,-1)
####    elif len(approx)==3:
####        print "triangle"
####        cv2.drawContours(img,[cnt],0,(0,255,0),-1)
####    elif len(approx)==4:
####        print "square"
####        cv2.drawContours(img,[cnt],0,(0,0,255),-1)
####    elif len(approx) == 9:
####        print "half-circle"
####        cv2.drawContours(img,[cnt],0,(255,255,0),-1)
####    elif len(approx) > 15:
####        print "circle"
####        cv2.drawContours(img,[cnt],0,(0,255,255),-1)

##############################################################
##areaArray = []
##count = 1
##
##for i, c in enumerate(contours):
##    area = cv2.contourArea(c)
##    areaArray.append(area)
##
###first sort the array by area
##sorteddata = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)
##
###find the nth largest contour [n-1][1], in this case 2
##secondlargestcontour = sorteddata[1][1]
##
###draw it
##x, y, w, h = cv2.boundingRect(secondlargestcontour)
###cv2.drawContours(img, secondlargestcontour, -1, (255, 0, 0),20)
###cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 5)
##
##approx = cv2.approxPolyDP(secondlargestcontour,0.01*cv2.arcLength(secondlargestcontour,True),True)
##print approx
##cv2.drawContours(img,[secondlargestcontour],0,255,-1)
##
##if len(approx) > 15:
##    print "circle"

#############################################################################
circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,32,
                            param1=200,param2=30,minRadius=0,maxRadius=height/2)

##circles = np.uint16(np.around(circles))

if not (circles is None):
    print len(circles[0,:])
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cnt = getLargestContour(img,2)
        print cv2.contourArea(cnt)
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
else:
    cnt = getLargestContour(img,2)
    print cnt
    if not (cnt is None):
        print cv2.contourArea(cnt)
    else:
        print 0.0
    print 0




#################################################################################


cv2.namedWindow('img',cv2.WINDOW_NORMAL)
cv2.resizeWindow('img', 600,600)
cv2.imshow('img',img)

cv2.waitKey(0)
cv2.destroyAllWindows()
