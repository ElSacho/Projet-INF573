import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from PIL import Image
import random
import pygame
import time 
import utils as animation

class BiscuitGameClass:
    def __init__(self, pathFood, timeMax = 20):
        self.points = []  # all points of the decoupe of the biscuit
        self.imgBiscuit = cv2.imread("biscuit/assets/"+pathFood, cv2.IMREAD_UNCHANGED)
        self.imgMask = cv2.imread("biscuit/assets/masque_biscuit1.png", cv2.IMREAD_UNCHANGED)
        self.gameOver = False
        self.started = True
        self.img_contour = np.zeros_like(self.imgMask)
        self.time = time.time()
        self.timeMax = timeMax
 
    def draw_line(self, imgMain):
        for i, point in enumerate(self.points):
            if i != 0:
                cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
            cv2.circle(imgMain, self.points[-1], 20, (0, 255, 0), cv2.FILLED)

    def add_image(self, img):
        return cvzone.overlayPNG(img, self.imgBiscuit)
 
    def hasWon(self):
        pixel = [10,10,10]
        tolerance = np.array([15,50,50])  
        mask = cv2.inRange(self.img_contour, pixel-tolerance, pixel+tolerance)
        try :
            contours, _ = cv2.findContours(mask,  cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours)==3:
                return True
            return False
        except :
            return False    
            
            
    def update(self, imgMain, currentHead, music2):
        wonState = False
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300, 400],
                               scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [300, 550],
                               scale=7, thickness=5, offset=20)
        else:
            cx, cy = currentHead
 
            self.points.append([cx, cy])
              
            # Draw image
            imgMain = self.add_image(imgMain)  
              
            # Draw Snake
            if self.points:
                self.draw_line(imgMain)
                self.draw_line(self.img_contour)
 
            # cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80],
            #                    scale=3, thickness=3, offset=10)
 
            # Check for Collision
            if self.hasWon():
                wonState = True
                print("Won")
                self.points = []
                self.img_contour = np.zeros_like(self.imgMask)
            if cy >= self.imgMask.shape[0] or cx >= self.imgMask.shape[1]:
                self.points = []
                self.img_contour = np.zeros_like(self.imgMask)
            elif self.imgMask[cy,cx,2] > 50:
                #self.gameOver = True
                music2.play()
                self.points = [] 
                self.img_contour = np.zeros_like(self.imgMask)
                 
        return imgMain, wonState
    
    def timeRemaining(self):
        return self.timeMax-int(time.time()-self.time)

def addFaceBoom(img, tete, t, x,w,y,h):
    longeur_deplacement = img.shape[1]-(x+w)
    mouv = int((t-7)*longeur_deplacement/4)
    dep = min(longeur_deplacement, mouv)
    img[y:y+h,dep+x:dep+x+w,:]=tete
    headShotPosX = int(dep+x+4*w//11)
    headShotPosY = int(y+h//4)
    headShot = cv2.imread('biscuit/assets/headShot.png', cv2.IMREAD_UNCHANGED)
    dim = (w//5,h//7)
    headShot = cv2.resize(headShot, dim, interpolation = cv2.INTER_AREA)
    img = cvzone.overlayPNG(img, headShot, (headShotPosX,headShotPosY))
    try :
        nuqPosX = int(dep+x+3*w//11)
        nuqPosY = int(y+23*h//25)
        nuque = cv2.imread('biscuit/assets/nuqueBlood.png', cv2.IMREAD_UNCHANGED)
        dimNuque = (w//2,5*h//25)
        nuque = cv2.resize(nuque, dimNuque, interpolation = cv2.INTER_AREA)
        img = cvzone.overlayPNG(img, nuque, (nuqPosX,nuqPosY))
    except:
        pass
    return img

def light_effect(video,light, blood):
    if light :
        n = random.randint(1,2)
        if n==1:
            gray = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
            # Appliquer un seuil sur les niveaux de gris
            video = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1] 
            video = cv2.cvtColor( video, cv2.COLOR_BGR2HSV)
            return video
        else :
            light = False
            return video
    n = random.randint(1,20)
    if n==1:
        gray = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
        # Appliquer un seuil sur les niveaux de gris
        video = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1]
        pos = (random.randint(1,video.shape[1]-blood.shape[1]-1),random.randint(1,video.shape[0]-blood.shape[0]-1))
        # Combiner les niveaux de gris en un tableau 3D avec une seule valeur de canal pour chaque pixel
        gray3d = cv2.merge((video, video, video))
        gray3d = cvzone.overlayPNG(gray3d, blood, pos)
        return gray3d
    else :
        light = False
        return video


def play():
    # Initialiser le module de son de Pygame
    pygame.mixer.init()
    face_cascade = cv2.CascadeClassifier('/Users/potosacho/opt/anaconda3/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    # Charger le fichier audio
    #music1 = pygame.mixer.music.load('biscuit/assets/UnfinishedBusiness.mp3')
    music2 = pygame.mixer.Sound('biscuit/assets/blood.mp3')
    #music2 = pygame.mixer.music.load('biscuit/assets/blood.mp3')

    blood = cv2.imread('biscuit/assets/blood.png', cv2.IMREAD_UNCHANGED)
    # Jouer le fichier audio
    timingVideoGameOver = -1
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    # playsound('biscuit/assets/UnfinishedBusiness.mp3')

    
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    
    game = BiscuitGameClass("biscuit1.png")
    light = False

    while cap.isOpened():
        success, img = cap.read()
        img = cv2.flip(img, 1)
        if game.timeRemaining()>0:        
            hands, img = detector.findHands(img, flipType=False)
            if hands:
                lmList = hands[0]['lmList']
                pointIndex = lmList[8][0:2]
                img, hasWon = game.update(img, pointIndex, music2)
                if hasWon:
                    return animation.afficher_win(img)
            else : 
                img = game.add_image(img)
            img = light_effect(img, light, blood)
            cv2.putText(img,f"Time remaining : {game.timeRemaining()} s",
                            (img.shape[0]//2,50),
                            cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
                            2,
                            (10,10,250))
            cv2.imshow("jeu", img)
        else :
            if timingVideoGameOver == -1 :
                faces = face_cascade.detectMultiScale(img)
                for (x, y, w, h) in faces:
                    tete = img[y:y+h,x:x+w,:]
                timingVideoGameOver = 0
            elif timingVideoGameOver<46:
                if timingVideoGameOver<10:
                    if timingVideoGameOver==6:
                        music3 = pygame.mixer.Sound('biscuit/assets/blood.mp3')
                        music3.play()
                    imgDead = cv2.imread('biscuit/assets/gameOver/gunShot0'+str(timingVideoGameOver)+'.png', cv2.IMREAD_UNCHANGED)
                else :
                    imgDead = cv2.imread('biscuit/assets/gameOver/gunShot'+str(timingVideoGameOver)+'.png', cv2.IMREAD_UNCHANGED)
                try :
                    if timingVideoGameOver>8:
                        img = addFaceBoom(img, tete, timingVideoGameOver, x,w,y,h)
                    img = cvzone.overlayPNG(img, imgDead)
                    timingVideoGameOver+=1
                except :
                    timingVideoGameOver +=1
                if timingVideoGameOver==45:
                    save_last_image = img
                cv2.imshow("jeu", img)
            elif timingVideoGameOver<100:
                val = animation.afficher_game_over(save_last_image)
                return val
        key = cv2.waitKey(1)
        if key == ord('r'):
            return "Restart"
        if key == ord('m'):
            return "Menu"
        if key == ord('q'):
            return "Quitter"

def runGame():
    while True :
        keyboard = play()
        if keyboard == "Menu":
            return True
        elif keyboard == "Quitter":
            return False
        
# runGame()