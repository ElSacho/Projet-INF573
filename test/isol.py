import cv2
import numpy as np


def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY, img
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img,(x,y),10,(255,0,0),-1)
        mouseX,mouseY = x,y


def isolerImage(image, mouseX, mouseY):
    if mouseX == -1 :
        print('non')
        cv2.imshow('image',img)
        return
    #creer un masque tout noir sauf pour le blanc
    #creer une queue avec tous les voisins du pixel
    # si l'intensite entre les voisins est inferieur à un seuil on ajoute dans le masque et on met la couleur de ce voisin à jour puis on ajoute les voisins de ce point
    # sinon on enleve de la queue
    
    
    
    #hsv = cv2.cvCloneImage(image)
    #cv2.cvCvtColor(image, hsv, cv2.CV_BGR2HSV)
    #mask = cv2.cvCreateImage(cv2.cvGetSize(image), 8, 1)
    
    #h,s,v = hsv[mouseX,mouseY,:]
    #tolerance = 10

    #cv2.cvInRangeS(hsv, cv2.cvScalar(h - tolerance -1, s - tolerance, 0), cv2.cvScalar(h + tolerance -1, s + tolerance, 255), mask) 
    
    #kernel = cv2.cvCreateStructuringElementEx(5, 5, 2, 2, cv2.CV_SHAPE_ELLIPSE)
    #cv2.cvDilate(mask, mask, kernel, 1)
    #cv2.cvErode(mask, mask, kernel, 1)
    
    # setting the lower and upper range for mask1,[H,S,V], for lighter shades
    lower_red = np.array([0,70,70])
    upper_red = np.array([10,255,255])
    
    # setting the lower and upper range for mask2, for darker shades
    lower_red = np.array([170,70,70])
    upper_red = np.array([180,255,255])

    # setting the lower and upper range for mask, for blue
    lower_b = np.array([88,78,20])
    upper_b = np.array([128,255,255])

    # Prior initialization of all centers for safety
    one_cen, two_cen = [240,320],[240,320]
    cursor = [960,540]

    # Area ranges for contours of different colours to be detected
    area = [300,1900]

    # Rectangular kernal for eroding and dilating the mask for primary noise removal 
    kernel = np.ones((7,7),np.uint8)
    showCentroid = False
    cur_pos = [240,320]
    contour = -1
    sensitivity= 4 #Scale like 1,2,3,4,5 where 1 is lowest sensitiviy and 5 max

    tolerance1 = np.array([15,50,50])  
    tolerance = 30  
    hsv = cv2.cvtColor( image, cv2.COLOR_BGR2HSV)
    
    print(mouseY,mouseX)
    print(hsv.shape)
    pixel = hsv[mouseY,mouseX,:]
   # pixel = np.array([])
    print(hsv)
    h,s,v = pixel
    print(pixel)
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv,lower_red,upper_red)
    mask1 = mask1+mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel)
    mask1 = cv2.dilate(mask1, kernel, iterations = 1)
    
    maskb = cv2.inRange(hsv, lower_b, upper_b)
    #maskb = cv2.inRange(hsv, pixel-tolerance1, pixel+tolerance1)
    #maskb = cv2.inRange(hsv, cv2.scalar(h - tolerance -1, s - tolerance, 0), cv2.scalar(h + tolerance -1, s + tolerance, 255)) 
    maskb = cv2.morphologyEx(maskb, cv2.MORPH_OPEN, kernel)
    maskb = cv2.dilate(maskb, kernel, iterations = 1)


    contours, _ = cv2.findContours(maskb, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    
    contour = max(contours, key = lambda x: cv2.contourArea(x))
    x,y,w,h = cv2.boundingRect(contour)
    cv2.rectangle(maskb, (x,y),(x+w,h+y),(120,120,255),0)
    print(x,y,w,h)
    cv2.circle(maskb,(x+w,y),10,(255,0,0),-1)
    cv2.imshow('masque',maskb)
    tol = 4

    for i in range(w):
        if maskb[y+tol,x+i]==255:
            position_sup_droite = i
            break
        print(f"{i} : {maskb[y,x+i]}")
    pourcentage = position_sup_droite/w
    print(pourcentage)
    if pourcentage < 20:
        print("devant")
    elif pourcentage < 50:
         print("droite")
    elif pourcentage < 80:
         print("gauche")
    else : 
         print("devant")

    return

mouseX = -1
mouseY = -1

img = cv2.imread('imageBlue.jpg')
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)  

while(1):
    #cv2.imshow('image',img)
    isolerImage(img, mouseX, mouseY)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print (mouseX, mouseY)
    elif k == ord('q'):
        break
        
