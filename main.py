from biscuit.biscuit import runGame as biscuit
from memoryGame.memory_game import runGame as memory
import utils as animation
import cv2
import pygame
# lancer la sequence intro du jeu
# lancer le jeu sur lequel on cliquer

mousePos = (-1,-1)

def introDuJeu():
    global mousePos 
    pygame.mixer.init()
    musicIntro = pygame.mixer.Sound('animation/intro.mp3')
    musicIntro.play()
    musicAmbiance = pygame.mixer.Sound('biscuit/assets/UnfinishedBusiness.mp3')
    action = animation.afficher_intro()
    if action == "Quitter":
        return
    musicIntro.stop()
    musicAmbiance.play()
    play = True
    while play:
        n = get_game()
        mousePos = (-1,-1)
        if n == -1:
            return
        play = lancer_le_jeu(n)
    return

def get_mouse_pos(event,x,y,flags,param):
    global mousePos
    if event == cv2.EVENT_LBUTTONDOWN:
        mousePos = (x,y)
    
def get_game():
    global mousePos
    menu = cv2.imread("animation/intro/introduction539.png")
    cv2.imshow("jeu", menu)
    while True:
        cv2.setMouseCallback('jeu',get_mouse_pos)
        key = cv2.waitKey(1)
        if mousePos[0] != -1:
            if mousePos[0] < 600:
                if mousePos[1] < 640:
                    return 1
                elif mousePos[1] < 1280:
                    return 2
                elif mousePos[1] < 1920:
                    return 3
            elif mousePos[1]<1080:
                if mousePos[1] < 640:
                    return 4
                elif mousePos[1] < 1280:
                    return 5
                elif mousePos[1] < 1920:
                    return -1
        if key == ord('1') or key == ord('2') or key == ord('3') or key == ord('4') or key == ord('5'):
            return int(key)
        if key == ord('q') or key == ord('6'):
            return -1

def lancer_le_jeu(n):
    if n == 1:
        action = biscuit()
    else :
        action = memory()
    return action
    
introDuJeu()

