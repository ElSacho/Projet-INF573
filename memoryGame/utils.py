import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from PIL import Image
import time 

def afficher_game_over(img):
    t=0
    img = cv2.merge((img, img, img))
    #print(img.shape)
    while t<60:
        time.sleep(0.004)
        if t<10:
            screen = cv2.imread('animation/gameOver/gameOver0'+str(t)+'.png', cv2.IMREAD_UNCHANGED)
        else :
            screen = cv2.imread('animation/gameOver/gameOver'+str(t)+'.png', cv2.IMREAD_UNCHANGED)
        dim = (img.shape[1],img.shape[0])
        screen = cv2.resize(screen, dim, interpolation = cv2.INTER_AREA)
        img = cvzone.overlayPNG(img, screen)
        cv2.imshow("jeu", img)
        key = cv2.waitKey(1)
        if key == ord('r'):
            return "Restart"
        if key == ord('q'):
            return "Menu"
        t+=1
    while True :
        cv2.imshow("jeu", img)
        key = cv2.waitKey(1)
        if key == ord('r'):
            return "Restart"
        if key == ord('q'):
            return "Menu"
        
def afficher_win(img):
    t=0
    while t<139:
        time.sleep(0.004)
        if t<10:
            screen = cv2.imread('animation/won/won00'+str(t)+'.png', cv2.IMREAD_UNCHANGED)
        elif t<100 :
            screen = cv2.imread('animation/won/won0'+str(t)+'.png', cv2.IMREAD_UNCHANGED)
        else :
            screen = cv2.imread('animation/won/won'+str(t)+'.png', cv2.IMREAD_UNCHANGED)
        dim = (img.shape[1],img.shape[0])
        screen = cv2.resize(screen, dim, interpolation = cv2.INTER_AREA)
        img_to_show = cvzone.overlayPNG(img, screen)
        cv2.imshow("Image", img_to_show)
        key = cv2.waitKey(1)
        if key == ord('r'):
            return "Restart"
        if key == ord('q'):
            return "Menu"
        t+=1
    while True :
        cv2.imshow("Image", img_to_show)
        key = cv2.waitKey(1)
        if key == ord('r'):
            return "Restart"
        if key == ord('q'):
            return "Menu"
        


     


    