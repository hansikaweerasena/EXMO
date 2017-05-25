import cv2
import numpy as np
import operator

CAMERA = 1


def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)


def takeCapture(capture):
    return capture.read()[1]


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

def correctPoints(points):
    sorted_list=sorted(points, key=operator.itemgetter(0), reverse=False);

    if(sorted_list[0][1] > sorted_list[1][1]):
        temp = sorted_list[0]
        sorted_list[0] =  sorted_list[1]
        sorted_list[1] =  sorted_list[3]
        sorted_list[3] =  temp
    else:
        temp = sorted_list[1]
        sorted_list[1] =  sorted_list[3]
        sorted_list[3] =  temp

    if(sorted_list[1][1] > sorted_list[2][1]):
        temp = sorted_list[1]
        sorted_list[1] =  sorted_list[2]
        sorted_list[2] =  temp

    return sorted_list

def getBoard(img):
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,100,200,cv2.THRESH_BINARY)

    #cv2.imshow("thresh",thresh)
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

    avgDim = (w+h)/2
    pol = cv2.approxPolyDP(secondlargestcontour,0.01*cv2.arcLength(secondlargestcontour,True),True)

    points = [[pol[0][0][0],pol[0][0][1]] ,[pol[1][0][0],pol[1][0][1]] ,[pol[2][0][0],pol[2][0][1]] ,[pol[3][0][0],pol[3][0][1]] ]

    sortedPoints = correctPoints(points)
    #pts_src = np.array([[sortedPoints[1][0],sortedPoints[1][1]] ,[sortedPoints[2][0],sortedPoints[2][1]],[sortedPoints[3][0],sortedPoints[3][1]], [sortedPoints[0][0],sortedPoints[0][1]]] )
    pts_src = np.array([[sortedPoints[0][0],sortedPoints[0][1]],[sortedPoints[3][0],sortedPoints[3][1]],[sortedPoints[1][0],sortedPoints[1][1]] ,[sortedPoints[2][0],sortedPoints[2][1]]] )
     

    #pts_src = np.array([[pol[0][0][0],pol[0][0][1]] ,[pol[1][0][0],pol[1][0][1]],[pol[3][0][0],pol[3][0][1]], [pol[2][0][0],pol[2][0][1]]] )
    pts_dst = np.array([[0, 0],[0, avgDim],[avgDim, 0],[avgDim, avgDim]])

    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)
		 
    # Warp source image to destination based on homography
    im_out = cv2.warpPerspective(img, h, (avgDim,avgDim))
    #im_out = rotateImage(im_out,-90)

    #dst = cv2.resize(im_out,(0,0), fx=1, fy=1)
	
    return im_out




def getSymbol(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    height, width, channels = img.shape

    ret,thresh = cv2.threshold(gray,70,200,0)
    
    _,contours,h = cv2.findContours(thresh,1,2)

    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20,param1=200,param2=30,minRadius=0,maxRadius=height/2)

    if not (circles is None):
        return 'O';
    else:
        cnt = getLargestContour(img,2)
        if not (cnt is None):
            area = cv2.contourArea(cnt)
            #print area
            if(area > 10):      
                return 'X'
            else:
                return None
        else:
            return None

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
                return None
        else:
            return None
    else:
        return None
    

def getMatric(dst):
    height, width, channels = dst.shape
    matrix = []

    boundThresh = 10
    
#1
    cell7 = dst[2*height/3+boundThresh:height-boundThresh,boundThresh:width/3-boundThresh]
    #cv2.imshow("Cell 7", cell7)
    cv2.imwrite("cell7c.jpg",cell7)
##  print getSymbol(cell7)
    matrix.append(getSymbol(cell7))


#2
    cell8 = dst[2*height/3+boundThresh:height-boundThresh,width/3+boundThresh:2*width/3-boundThresh]
    #cv2.imshow("Cell 8", cell8)
    cv2.imwrite("cell8c.jpg",cell8)
##  print getSymbol(cell8)
    matrix.append(getSymbol(cell8))


#3
    cell9 = dst[2*height/3+boundThresh:height-boundThresh,2*width/3+boundThresh:width-boundThresh]
    #cv2.imshow("Cell 9", cell9)
    cv2.imwrite("cell9c.jpg",cell9)
##  print getSymbol(cell9)
    matrix.append(getSymbol(cell9))

#4   
    cell4 = dst[height/3+boundThresh:2*height/3-boundThresh,boundThresh:width/3-boundThresh]
    #cv2.imshow("Cell 4", cell4)
    cv2.imwrite("cell4c.jpg",cell4)
##  print getSymbol(cell4)
    matrix.append(getSymbol(cell4))

#5
    cell5 = dst[height/3+boundThresh:2*height/3-boundThresh,width/3+boundThresh:2*width/3-boundThresh]
    #cv2.imshow("Cell 5", cell5)
    cv2.imwrite("cell5c.jpg",cell5)
##  print getSymbol(cell5)
    matrix.append(getSymbol(cell5))

#6
    cell6 = dst[height/3+boundThresh:2*height/3-boundThresh,2*width/3+boundThresh:width-boundThresh]
    #cv2.imshow("Cell 6", cell6)
    cv2.imwrite("cell6c.jpg",cell6)
##  print getSymbol(cell6)


#7    
    matrix.append(getSymbol(cell6))               
    cell1 = dst[boundThresh:height/3-boundThresh,boundThresh:width/3-boundThresh]
    #cv2.imshow("Cell 1", cell1)
    cv2.imwrite("cell1c.jpg",cell1)
##  print getSymbol(cell1)
    matrix.append(getSymbol(cell1))


#8
    cell2 = dst[boundThresh:height/3-boundThresh,width/3+boundThresh:2*width/3-boundThresh]
    #cv2.imshow("Cell 2", cell2)
    cv2.imwrite("cell2c.jpg",cell2)
##  print getSymbol(cell2)
    matrix.append(getSymbol(cell2))


#9
    cell3 = dst[boundThresh:height/3-boundThresh,2*width/3+boundThresh:width-boundThresh]
    #cv2.imshow("Cell 3", cell3)
    cv2.imwrite("cell3c.jpg",cell3)
##  print getSymbol(cell3)
    matrix.append(getSymbol(cell3))


	
    return matrix
        
 

def senseTicTacBoard():
    cam = cv2.VideoCapture(CAMERA)

    # Read three images first:
    t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

    motionState = False
    motionPeriod = 0
    nomotionPeriod = 0

    while True:
        imgDiff = diffImg(t_minus, t, t_plus)

        ret,thresh = cv2.threshold(imgDiff,40,255,cv2.THRESH_BINARY)

        kernel = np.ones((2,2),np.uint8)
        eroded = cv2.erode(thresh,kernel,iterations = 1)

        _,contours, hierarchy = cv2.findContours(thresh,1,2)

##        print len(contours)
        if(len(contours)>100):
            motionPeriod = motionPeriod + 1
        else:
            nomotionPeriod = nomotionPeriod + 1

        if(motionPeriod > 5):
            if(not motionState):
                print "motion started"
            motionState = True
            motionPeriod = 0
            nomotionPeriod = 0
        if(nomotionPeriod > 20):
            if(motionState):
                print "motion stoped"
                frame = takeCapture(cam)
                cv2.imshow("Frame",frame)
                #cv2.imwrite("1.jpg",frame)
                board = getBoard(frame)
                cv2.imshow("board",board)

                matrix = getMatric(board)
                print matrix
               # cam.release()
               # cv2.destroyAllWindows()
               # return matrix
                #print matrix
                #cv2.imshow("Board",board)
            motionState = False
            motionPeriod = 0
            nomotionPeriod = 0
        

        cv2.imshow( "Original",t_plus)
        #cv2.imshow( "Motion",eroded)

        t_minus = t
        t = t_plus
        t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

        key = cv2.waitKey(10)
        
        
        if key == 27:
            cam.release()
            cv2.destroyAllWindows()
            break
    

matrix =senseTicTacBoard();
#print matrix

