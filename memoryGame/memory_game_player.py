import time
import cv2
import random

start = time.time()

class Player:
    def __init__(self, seuil_time = 20):
        self.score = 0
        self.tab = []
        self.nombreDevine = 0
        self.draw_time = time.time()
        self.time = time.time()
        self.seuil_time = seuil_time
        self.is_drawing=False
        self.passed_middle = True
        
    def value_to_draw_sequence(self):
        value = int((time.time()-self.draw_time)//1)
        if value > len(self.tab):
            self.is_drawing = False
            return 'NaN'
        if value == len(self.tab):
            self.time = time.time()
            return 'Go'
        self.is_drawing = True
        if self.tab[value] == 1 :
            return str(value+1)+': Droite'
        else : return str(value+1)+':Gauche'
        
    def player_play(self, answer):
        if int((time.time()-self.time )//1) > self.seuil_time*(self.score+1):
          #  print('Time damage')
            return False
        el = answer[0]
        for other_el in answer:
            if el != other_el:
                return True
        if el == 0:
            self.passed_middle = True
            return True
        #Si on est bien repasse au milieu
        if self.passed_middle :
            if el == self.tab[self.nombreDevine]:
               #t('Good')
                if self.nombreDevine == self.score:
                    self.score += 1
                    self.update()
                    self.passed_middle = False
                    return True
                self.nombreDevine +=1
                self.passed_middle = False 
                return True
          #  print(self.tab[self.nombreDevine])
         #  print(answer)
            return False
       # print('wtf')
        return True
    
    def update(self):
        self.nombreDevine = 0
        a = random.randint(1,2)
        if a==2:
            a=-1
        self.tab.append(a)
        self.draw_time = time.time()
        
        
        
        