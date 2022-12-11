import cv2
import numpy as np
from segmentation.randomWalker import random_walk

click_pos = (-1,-1)

def get_mouse_pos(event,x,y,flags,param):
    global click_pos
    if event == cv2.EVENT_LBUTTONDOWN:
        click_pos = (y,x)
        
        
def get_label(img, nbrLabel=3, nbrClicks=5):
    global click_pos
    click = 1
    labels = np.zeros((img.shape[0], img.shape[1]))
    label = 1
    tab_click = []
    tab_colors = []
    while True:
        cv2.imshow('jeu',img)
        cv2.setMouseCallback('jeu',get_mouse_pos)
        key = cv2.waitKey(1)
        if click_pos[0] != -1:
            labels[click_pos]=label
            tab_click.append(click_pos)
            tab_colors.append(img[click_pos])
            if label ==1:
                img[click_pos]=[0,0,255]
            elif label ==2:
                img[click_pos]=[255,0,0]
            elif label ==3:
                img[click_pos]=[0,255,0]
            click_pos = (-1,-1)
            click +=1
            if click>nbrClicks:
                return labels
            if click == nbrClicks and label ==1:
                label +=1
        if key == ord(" "):
            if label<nbrLabel:
                label +=1
        if key == ord('a'):
            if click > 0:
                labels[tab_click[-1]] = 0
                img[tab_click[-1]] = tab_colors[-1]
                tab_click.pop()
                tab_colors.pop()
                click -= 1
        if key == ord("l"):
            if label>0 and click !=nbrClicks:
                label -=1
        if key == ord("q"):
            labels[0,0] = -1
            return labels
        if key == ord("m"):
            labels[0,0] = -2
            return labels

def adapter(imgLabel,convert, nbrLabels):
    # pour tous les pixels de l'image, on remplace par une valeur proportionnelle au label 
    shape = imgLabel.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            val = int((int(imgLabel[i][j])*255/int(nbrLabels)))
            convert[i][j]=[val,val,val]
    # on affiche l'image finale
    return convert
        
def play():
    click_pos = (-1,-1)
    nbrLabel = 3
    nbrClicks = 10
    img = cv2.imread("segmentation/assets/tetePetite.jpg")
    # img = cv2.resize(img, (80,80), interpolation = cv2.INTER_AREA)
    labels = get_label(img, nbrLabel, nbrClicks)
    try :
        if labels[0,0] == -1:
            return "Quitter"
        if labels[0,0] == -2:
            return 'Menu'
    except :
        pass
    img_seg = random_walk(img, labels, nbrClicks ,nbrLabel, 100)
    # img_seg = cv2.merge((img_seg, img_seg, img_seg))
    img_seg = adapter(img_seg, img, nbrLabel)
    cv2.imshow('jeu',img_seg)
    while True:
        cv2.imshow('jeu',img_seg)
        key = cv2.waitKey(1)
        if key == ord('q'):
            return "Quitter"
        if key == ord('m'):
            return 'Menu'
        if key == ord('r'):
            return 'Restart'
            
def runGame():
    while True :
        keyboard = play()
        if keyboard == "Menu":
            return True
        elif keyboard == "Quitter":
            return False
        elif keyboard == "Restart":
            keyboard = play()
    
# runGame()