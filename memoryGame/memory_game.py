import cv2
import numpy as np
from pynput.keyboard import Key, Controller
from memoryGame.memory_game_player import Player
import utils as animation
#import keyboard
#import pyautogui
mouseX, mouseY, temp = -1,-1,-1

def update_values(tab_val, val, lengh =3):
    if len(tab_val)==3:
        tab_val[0]
        tab_val.pop(0)
        return
    tab_val.append(val)

def isolerImage(hsv, pixel, method="BOUGER"):
    
    # Kernal rectangulaire pour l'érosion et la dilatation du masque pour la suppression de bruit 
    kernel = np.ones((7,7),np.uint8)
    # tolerance de couleur differente de la ou on a clique
    tolerance = np.array([15,50,50])  

    # creation d'un masque
    maskb = cv2.inRange(hsv, pixel-tolerance, pixel+tolerance)
    maskb = cv2.morphologyEx(maskb, cv2.MORPH_OPEN, kernel)
    maskb = cv2.dilate(maskb, kernel, iterations = 1)
    maskb = cv2.erode(maskb, kernel, iterations = 1)

    # detection de contours
    contours, _ = cv2.findContours(maskb, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    
    
    # on prend le plus grand contour
    try :
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
                    return (-1 , volantSeul)
                elif x - position_ini < 150:
                    return (0 , volantSeul)
                else :
                    return (1 , volantSeul)
            except:
                position_ini = x
                return (0 , volantSeul)
    except :
        return(0, np.zeros_like(maskb))
 
def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY, img
    if event == cv2.EVENT_LBUTTONDOWN:
        # cv2.circle(image,(x,y),10,(255,0,0),-1)
        mouseX,mouseY = x,y 

def play():
    global mouseX, mouseY, temp
    mouseX, mouseY, temp = -1,-1,-1
    webcam = cv2.VideoCapture(0)
    
    while webcam.isOpened():

        ret, image = webcam.read()
        image = cv2.flip(image, 1)
        cv2.setMouseCallback('jeu',draw_circle)
    
        # Si on a pas encore clique sur l'objet directeur on montre l'image initiale
        if mouseX==-1:
            cv2.imshow('jeu',image)
        
        # SI on vient de cliquer, on recupere le pixel et on isole l'objet
        elif temp ==-1:
            hsv = cv2.cvtColor( image, cv2.COLOR_BGR2HSV)
            pixel = hsv[mouseY,mouseX,:]
            temp = 0
            val, volant = isolerImage(hsv, pixel)
            tab_val = [val]
            game = Player()
            game.update()
            cv2.imshow('jeu',volant)
    
        # On isole l'objet par rapport au pixel initial et on joue au jeu
        else :
            hsv = cv2.cvtColor( image, cv2.COLOR_BGR2HSV)
            
            # On recuperer l'image et la direction choisie par l'utilisateur
            val, volant = isolerImage(hsv, pixel)
            update_values(tab_val, val)
            
            # On regarde si on a du texte a ecrire et si oui, on l'ecrit
            text_to_write = game.value_to_draw_sequence()
            if text_to_write != 'NaN':
               # print(text_to_write)
                
                cv2.putText(volant,text_to_write,
                        (10,500),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2,
                        (255,255,0))
                            
                cv2.imshow('jeu',volant)
            else:
                state = game.player_play(tab_val)
                if state == False:
                   # print('Game Over')
                    val = animation.afficher_game_over_2D(volant)
                    return val
                
                cv2.putText(volant,str(game.nombreDevine),
                        (10,500),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2,
                        (255,255,0))
                
                cv2.imshow('jeu',volant)
            
        if cv2.waitKey(1) == ord('q'):
            return "Quitter"
        if cv2.waitKey(1) == ord('m'):
            return 'Menu'
        
    webcam.release()
    cv2.destroyAllWindows()

def runGame():
    while True :
        keyboard = play()
        if keyboard == "Menu":
            return True
        elif keyboard == "Quitter":
            return False

# runGame()