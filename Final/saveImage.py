import cv2
import numpy as np

cam = cv2.VideoCapture(1)
ret, frame = cam.read()

cv2.imwrite("initial.jpg",frame)
cv2.imshow("frame",frame)
cv2.waitKey()
cv2.destroyAllWindows()
