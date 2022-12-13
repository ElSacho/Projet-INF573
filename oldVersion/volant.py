import cv2
import numpy as np
from pynput.keyboard import Key, Controller
#import keyboard
#import pyautogui

def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY, img
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(image,(x,y),10,(255,0,0),-1)
        mouseX,mouseY = x,y


def isolerImage(hsv, pixel, method="BOUGER"):
    
    # Rectangular kernal for eroding and dilating the mask for primary noise removal 
    kernel = np.ones((7,7),np.uint8)
    # tolerance de couleur differente de la ou on a clique
    tolerance = np.array([15,50,50])  

    # creation d'un masque
    maskb = cv2.inRange(hsv, pixel-tolerance, pixel+tolerance)
    maskb = cv2.morphologyEx(maskb, cv2.MORPH_OPEN, kernel)
    maskb = cv2.dilate(maskb, kernel, iterations = 1)
    maskb = cv2.erode(maskb, kernel, iterations = 1)

    keyboard = Controller()

    # detection de contours
    contours, _ = cv2.findContours(maskb, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    
    
    # on prend le plus grand contour
    contour = max(contours, key = lambda x: cv2.contourArea(x))
    
    # On trace un rectangle dans ce contour 
    x,y,w,h = cv2.boundingRect(contour)
    cv2.rectangle(maskb, (x,y),(x+w,h+y),(120,120,255),0)
    
    # on cree une nouvelle image noire sur laquelle on trace juste les contours de l'objet qui sert de volant
    volantSeul = np.zeros_like(maskb)
    cv2.drawContours(volantSeul, contour, -1, (255, 255, 255), 3)
    cv2.rectangle(volantSeul, (x,y),(x+w,h+y),(120,120,255),0)

    # on detecte si on va vers le haut, bas ou gauche
    if method == "BOUGER":
        global position_ini
        try :
            if x - position_ini < -150:
                print("gauche")
                keyboard.press("a")
                keyboard.release("a")
                #keyboard.press_and_release("space")
                #pyautogui.typewrite("hello Geeks !")
            elif x - position_ini < 150:
                print("devant")
            else :
                print("droite")
        except:
            position_ini = x
            print("devant")
    else :  
        tol = 4
        for i in range(w):
            if maskb[y+tol,x+i]==255:
                position_sup_droite = i
                cv2.circle(maskb,(x+i,y+tol),10,(255,255,10),-1)

                break
            #print(f"{i} : {maskb[y,x+i]}")
        pourcentage = position_sup_droite/w*100
        print(pourcentage)
        if pourcentage < 20:
            print("devant")
        elif pourcentage < 50:
            print("droite")
        elif pourcentage < 80:
            print("gauche")
        else : 
            print("devant")
            

    cv2.imshow('volant',volantSeul)
    return
    
webcam = cv2.VideoCapture(0)
mouseX, mouseY, temp = -1,-1,-1

while webcam.isOpened():

    ret, image = webcam.read()
    image = cv2.flip(image, 1)
    
    cv2.setMouseCallback('image',draw_circle)
    if mouseX==-1:
        cv2.imshow('image',image)
    elif temp ==-1:
        hsv = cv2.cvtColor( image, cv2.COLOR_BGR2HSV)
        pixel = hsv[mouseY,mouseX,:]
        temp = 0
        isolerImage(hsv, pixel)
    else :
        hsv = cv2.cvtColor( image, cv2.COLOR_BGR2HSV)
        isolerImage(hsv, pixel)

    if cv2.waitKey(1) == ord('q'):
        break
        
webcam.release()
cv2.destroyAllWindows()


#Nous passons l’image en HSV car ainsi nous pourrons nous baser sur la teinte et la saturation de la couleur en laissant plus libre la « brillance » (V – value) de cette dernière. Ce qui nous permet, en partie seulement, d’éloigner les problèmes liés à l’éclairage.
#TODO: Passer l'image de BGR à HSV
"""
hsv = cvCloneImage(image);
cvCvtColor(image, hsv, CV_BGR2HSV)

# on cree un masque
mask = cvCreateImage(cvGetSize(image), image->depth, 1);


# On creer une variable tolerance et on garde tout ce qui est a peu pres egal à la valeur recherchee
tolerance = 10
cvInRangeS(hsv, cvScalar(h - tolerance -1, s - tolerance, 0), cvScalar(h + tolerance -1, s + tolerance, 255), mask);

# erosion pour supprimer les pixels isoles
# dilatation pour regrouper les groupes denses


# On prend un kernel cercle car ça correspond plus aux objets en regle generale
kernel = cvCreateStructuringElementEx(5, 5, 2, 2, CV_SHAPE_ELLIPSE);
"""