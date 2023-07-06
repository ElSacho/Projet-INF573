from biscuit.biscuit import runGame as biscuit
from memoryGame.memory_game import runGame as memory
from segmentation.coloriage import runGame as coloriage
from soleil.soleil  import runGame as soleil
from piano.glass import runGame as piano
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
    mousePos = (-1,-1)
    menu = cv2.imread("animation/intro/introduction539.png")
    cv2.imshow("jeu", menu)
    while True:
        cv2.setMouseCallback('jeu',get_mouse_pos)
        key = cv2.waitKey(1)
        if mousePos[0] != -1:
            if mousePos[1] < 600:
                if mousePos[0] < 640:
                    print(1)
                    return 1
                elif mousePos[0] < 1280:
                    print(2)
                    return 2
                elif mousePos[0] < 1920:
                    print(3)
                    return 3
            elif mousePos[1]<1080:
                if mousePos[0] < 640:
                    print(4)
                    return 4
                elif mousePos[0] < 1280:
                    print(5)
                    return 5
                elif mousePos[0] < 1920:
                    return -1
        if key == ord('&') :
            return 1
        if key == ord('é') :
            return 2
        if key == ord('"') :
            return 3
        if key == ord("'") :
            return 4 
        if key == ord('('):
            return 5
        if key == ord('q') or key == ord('§'):
            return -1

def lancer_le_jeu(n):
    if n == 1:
        action = soleil()
    elif n == 2:
        action = biscuit()
    elif n== 3 :
        action = memory()
    elif n== 4:
        action = coloriage()
    elif n== 5 :
        action = piano()
    else :
        return False
    
    return action
    
introDuJeu()

