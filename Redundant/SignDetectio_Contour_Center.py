import numpy as np
import cv2


def getLargestContour(img,largestIndex):
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
##    height, width, channels = img.shape
    ret,thresh = cv2.threshold(imgray,120,255,cv2.THRESH_BINARY)
    cv2.imshow("thresh",thresh)
    _,contours, hierarchy = cv2.findContours(thresh,1,2)

    areaArray = []
    count = 1

    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
##        if area  > 0:
##        print area
        areaArray.append(area)

    #first sort the array by area
    sorteddata = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)
    #print sorteddata
    ##    print len(sorteddata)
    #find the nth largest contour [n-1][1], in this case 2
    if (len(sorteddata) - largestIndex >= 0) :
        largestcontour = sorteddata[largestIndex - 1][1]
    else:
        largestcontour = None
    return largestcontour;


img = cv2.imread('cell9c.jpg')
height, width, channels = img.shape

print height,width
################################################################################
imgCpy = img.copy()
secondlargestcontour = getLargestContour(img,2)

if not (secondlargestcontour is None):
    #draw it
    x, y, w, h = cv2.boundingRect(secondlargestcontour)
    cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 1)
    print x, y, w, h
    #cv2.drawContours(img, secondlargestcontour, -1, (255, 0, 0),20)
    if( (w * h) > 0.01* (height *width)):
        
        
        cx = x+w/2
        cy = y+h/2
        center = (cx,cy)
        cv2.circle(img,center,1,[0,0,255],-1)

        if (w+h)/2 > 0.3*(height+width)/2:
            searchingPar = 0.2*(w+h)/2
        else:
            searchingPar = 0.05*(w+h)/2

        if((cx-searchingPar) > 0 and (cx+searchingPar)< width and (cy-searchingPar) > 0 and (cy+searchingPar) < height):
            searchingROI = imgCpy[cx-searchingPar:cx+searchingPar,cy-searchingPar:cy+searchingPar]
            #searchingROI = img[cx:60,cy:80]
            #dst = cv2.resize(searchingROI,(0,0), fx=10, fy=10)
                        
            cv2.imshow("ROI",searchingROI);

            gray = cv2.cvtColor(searchingROI,cv2.COLOR_BGR2GRAY)
            ret,thresh = cv2.threshold(gray,50,255,0)
            _,contours,h = cv2.findContours(thresh,1,2)

            print len(contours)
            if len(contours) > 1 :
                print "X"
            else:
                print "O"
        else:
            print "a"
    else:
        print "b"
else:
    print "c"
#################################################################################


cv2.imshow('img',img)

cv2.waitKey(0)
cv2.destroyAllWindows()
