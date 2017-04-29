import numpy as np
import cv2

def rotateImage(image, angle):
    center=tuple(np.array(image.shape[0:2])/2)
    rot_mat = cv2.getRotationMatrix2D(center,angle,1.0)
    return cv2.warpAffine(image, rot_mat, image.shape[0:2],flags=cv2.INTER_LINEAR)

def getLargestContour(img,largestIndex):
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
##    ret,thresh = cv2.threshold(imgray,70,150,cv2.THRESH_BINARY)
    ret,thresh = cv2.threshold(imgray,50,200,cv2.THRESH_BINARY)
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

def getSymbol2(img):
    height, width, channels = img.shape

    #print height,width
    imgCpy = img.copy()
    secondlargestcontour = getLargestContour(img,2)

    if not (secondlargestcontour is None):
        #draw it
        x, y, w, h = cv2.boundingRect(secondlargestcontour)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 1)
        #print x, y, w, h
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
                            
                #cv2.imshow("ROI",searchingROI);

                gray = cv2.cvtColor(searchingROI,cv2.COLOR_BGR2GRAY)
                ret,thresh = cv2.threshold(gray,50,255,0)
                _,contours,h = cv2.findContours(thresh,1,2)

                #print len(contours)
                if len(contours) > 1 :
                    return "X"
                else:
                    return "O"
            else:
                return ""
        else:
            return ""
    else:
        return ""

    
img = cv2.imread('1.jpg')

imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
##ret,thresh = cv2.threshold(imgray,70,150,cv2.THRESH_BINARY)
ret,thresh = cv2.threshold(imgray,100,200,cv2.THRESH_BINARY)
_,contours, hierarchy = cv2.findContours(thresh,1,2)

areaArray = []
count = 1

for i, c in enumerate(contours):
    area = cv2.contourArea(c)
    areaArray.append(area)

#first sort the array by area
sorteddata = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)

#find the nth largest contour [n-1][1], in this case 2
secondlargestcontour = sorteddata[1][1]

#draw it
x, y, w, h = cv2.boundingRect(secondlargestcontour)
#cv2.drawContours(img, secondlargestcontour, -1, (255, 0, 0),20)
#cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 5)

avgDim = (w+h)/2
pol = cv2.approxPolyDP(secondlargestcontour,0.01*cv2.arcLength(secondlargestcontour,True),True)

##cv2.circle(img,(pol[0][0][0],pol[0][0][1]), 10, (0,0,255), -1)
##cv2.circle(img,(pol[1][0][0],pol[1][0][1]), 10, (0,0,255), -1)
##cv2.circle(img,(pol[2][0][0],pol[2][0][1]), 10, (0,0,255), -1)
##cv2.circle(img,(pol[3][0][0],pol[3][0][1]), 10, (0,0,255), -1)

pts_src = np.array([[pol[0][0][0],pol[0][0][1]] ,[pol[1][0][0],pol[1][0][1]],[pol[3][0][0],pol[3][0][1]], [pol[2][0][0],pol[2][0][1]]] )
pts_dst = np.array([[0, 0],[avgDim, 0],[0, avgDim],[avgDim, avgDim]])

# Calculate Homography
h, status = cv2.findHomography(pts_src, pts_dst)
     
# Warp source image to destination based on homography
im_out = cv2.warpPerspective(img, h, (avgDim,avgDim))
im_out = rotateImage(im_out,-90)

dst = cv2.resize(im_out,(0,0), fx=1, fy=1) 
cv2.imshow("Warped Source Image", dst)

height, width, channels = dst.shape

boundThresh = 10

matrix = []

cell1 = dst[boundThresh:height/3-boundThresh,boundThresh:width/3-boundThresh]
cv2.imshow("Cell 1", cell1)
cv2.imwrite("cell011.jpg",cell1)
matrix.append(getSymbol2(cell1))

cell2 = dst[boundThresh:height/3-boundThresh,width/3+boundThresh:2*width/3-boundThresh]
cv2.imshow("Cell 2", cell2)
cv2.imwrite("cell012.jpg",cell2)
matrix.append(getSymbol2(cell2))

cell3 = dst[boundThresh:height/3-boundThresh,2*width/3+boundThresh:width-boundThresh]
cv2.imshow("Cell 3", cell3)
cv2.imwrite("cell013.jpg",cell3)
matrix.append(getSymbol2(cell3))

cell4 = dst[height/3+boundThresh:2*height/3-boundThresh,boundThresh:width/3-boundThresh]
cv2.imshow("Cell 4", cell4)
cv2.imwrite("cell014.jpg",cell4)
matrix.append(getSymbol2(cell4))

cell5 = dst[height/3+boundThresh:2*height/3-boundThresh,width/3+boundThresh:2*width/3-boundThresh]
cv2.imshow("Cell 5", cell5)
cv2.imwrite("cell015.jpg",cell5)
matrix.append(getSymbol2(cell5))

cell6 = dst[height/3+boundThresh:2*height/3-boundThresh,2*width/3+boundThresh:width-boundThresh]
cv2.imshow("Cell 6", cell6)
cv2.imwrite("cell016.jpg",cell6)
matrix.append(getSymbol2(cell6))

cell7 = dst[2*height/3+boundThresh:height-boundThresh,boundThresh:width/3-boundThresh]
cv2.imshow("Cell 7", cell7)
cv2.imwrite("cell017.jpg",cell7)
matrix.append(getSymbol2(cell7))


cell8 = dst[2*height/3+boundThresh:height-boundThresh,width/3+boundThresh:2*width/3-boundThresh]
cv2.imshow("Cell 8", cell8)
cv2.imwrite("cell018.jpg",cell8)
matrix.append(getSymbol2(cell8))


cell9 = dst[2*height/3+boundThresh:height-boundThresh,2*width/3+boundThresh:width-boundThresh]
cv2.imshow("Cell 9", cell9)
cv2.imwrite("cell019.jpg",cell9)
matrix.append(getSymbol2(cell9))

print matrix
##cv2.namedWindow('img',cv2.WINDOW_NORMAL)
##cv2.resizeWindow('img', 600,600)
##cv2.imshow('img',img)

cv2.waitKey(0)
cv2.destroyAllWindows()
