import cv2
import numpy as np


def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img,(x,y),100,(255,0,0),-1)
        mouseX,mouseY = x,y

def isolerImage(image, mouseX, mouseY):
    if mouseX == -1 :
        return
    
    hsv = cv2.cvCloneImage(image)
    cv2.cvCvtColor(image, hsv, cv2.CV_BGR2HSV)
    mask = cv2.cvCreateImage(cv2.cvGetSize(image), 8, 1)
    
    h,s,v = hsv[mouseX,mouseY,:]
    tolerance = 10

    cv2.cvInRangeS(hsv, cv2.cvScalar(h - tolerance -1, s - tolerance, 0), cv2.cvScalar(h + tolerance -1, s + tolerance, 255), mask) 
    
    kernel = cv2.cvCreateStructuringElementEx(5, 5, 2, 2, cv2.CV_SHAPE_ELLIPSE)
    cv2.cvDilate(mask, mask, kernel, 1)
    cv2.cvErode(mask, mask, kernel, 1)
    
    cv2.imshow(mask)


mouseX = -1
mouseY = -1

img = cv2.imread('image.png')
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)  

while(1):
    cv2.imshow('image',img)
    isolerImage(img, mouseX, mouseY)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print (mouseX, mouseY)
    elif k == ord('q'):
        break
        
