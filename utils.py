import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from PIL import Image
import time 

def afficher_game_over(img):
    t=0
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
        if key == ord('m'):
            return "Menu"
        if key == ord('q'):
            return "Quitter"
        t+=1
    while True :
        cv2.imshow("jeu", img)
        key = cv2.waitKey(1)
        if key == ord('r'):
            return "Restart"
        if key == ord('m'):
            return "Menu"
        if key == ord('q'):
            return "Quitter"
        
def afficher_win(img):
    t=0
    while t<139:
        #time.sleep(0.0025)
        if t<10:
            screen = cv2.imread('animation/won/won00'+str(t)+'.png', cv2.IMREAD_UNCHANGED)
        elif t<100 :
            screen = cv2.imread('animation/won/won0'+str(t)+'.png', cv2.IMREAD_UNCHANGED)
        else :
            screen = cv2.imread('animation/won/won'+str(t)+'.png', cv2.IMREAD_UNCHANGED)
        dim = (img.shape[1],img.shape[0])
        screen = cv2.resize(screen, dim, interpolation = cv2.INTER_AREA)
        img_to_show = cvzone.overlayPNG(img, screen)
        cv2.imshow("jeu", img_to_show)
        key = cv2.waitKey(1)
        if key == ord('r'):
            return "Restart"
        if key == ord('m'):
            return "Menu"
        if key == ord('q'):
            return "Quitter"
        t+=1
    while True :
        cv2.imshow("jeu", img_to_show)
        key = cv2.waitKey(1)
        if key == ord('r'):
            return "Restart"
        if key == ord('m'):
            return "Menu"
        if key == ord('q'):
            return "Quitter"
        
def afficher_game_over_2D(img):
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
        if key == ord('m'):
            return "Menu"
        if key == ord('q'):
            return "Quitter"
        t+=1
    while True :
        cv2.imshow("jeu", img)
        key = cv2.waitKey(1)
        if key == ord('r'):
            return "Restart"
        if key == ord('q'):
            return "Quitter"
        if key == ord('m'):
            return "Menu"

def afficher_intro():
    t=0
    while t<420:
        time.sleep(0.004)
        if t<10:
            screen = cv2.imread('animation/intro/introduction00'+str(t)+'.png', cv2.IMREAD_UNCHANGED)
        elif t<100 :
            screen = cv2.imread('animation/intro/introduction0'+str(t)+'.png', cv2.IMREAD_UNCHANGED)
        else :
            screen = cv2.imread('animation/intro/introduction'+str(t)+'.png', cv2.IMREAD_UNCHANGED)
        cv2.imshow("jeu", screen)
        key = cv2.waitKey(1)
        if key == ord(' '):
            t=418
        if key == ord('q'):
            return "Quitter"
        t+=2
    return "Menu"


def afficher_intro02():
    # Ouvrir la vidéo en utilisant la fonction cv2.VideoCapture()
    cap = cv2.VideoCapture('animation/intro.mp4')

    # Boucle tant que la vidéo est ouverte
    while cap.isOpened():
        # Lire le frame actuel en utilisant la fonction cap.read()
        ret, frame = cap.read()

        # Si le frame est retourné sans erreur, affiche à l'aide de la fonction cv2.imshow()
        if ret:
            cv2.imshow("jeu", frame)
        key = cv2.waitKey(1)
        if key == ord(' '):
            t=418
        if key == ord('q'):
            return "Quitter"

    # Librerer les ressources
    cap.release()
    return "Menu"