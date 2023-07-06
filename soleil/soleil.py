from time import time
import cv2
import mediapipe as mp
import numpy as np
import pygame
import utils as animation
import cvzone

pygame.init()
pygame.mixer.init()
mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

# Contains all the parameters that are used bith in the function play and in the functions end_game / begin_game
class Launch:
    def __init__(self):

        # launch = True if the speaker is counting 1, 2, 3
        # launch set to False when the count is over
        self.launch = False

        # Time Counter frome the moment when the speaker began to count 1,2,3
        self.time_decount = 0

        # Contains the sound counter  "1, 2, 3 soleil"
        self.soleil = pygame.mixer.Sound("soleil/soleil.mp3")

        # already_dead = True if the game is already over
        self.already_dead = False

        # counter launched when the user loses the game, useful to animate the death
        self.timingVideoGameOver = 0

        # Save the current frame
        self.image = 0

        # musicAlreadyshot = True if the gun musicshot has already fired
        self.musicAlreadyShot = False
        self.musicShot = pygame.mixer.Sound('biscuit/assets/blood.mp3')
        
    def end_game(self):
        print("Time Gave Over: ", self.timingVideoGameOver)
        if self.timingVideoGameOver<46:
            if self.timingVideoGameOver<10:
                imgDead = cv2.imread('biscuit/assets/gameOver/gunShot0'+str(self.timingVideoGameOver)+'.png', cv2.IMREAD_UNCHANGED)
            else :
                imgDead = cv2.imread('biscuit/assets/gameOver/gunShot'+str(self.timingVideoGameOver)+'.png', cv2.IMREAD_UNCHANGED)
            self.image = cvzone.overlayPNG(self.image, imgDead)
            self.timingVideoGameOver+=1
            key = cv2.waitKey(1)
            if key == ord('r'):
                return "Restart"
            if key == ord('m'):
                return "Menu"
            if key == ord('q'):
                return "Quitter"
            return "Continue"
        elif self.timingVideoGameOver<100:
            val = animation.afficher_game_over(self.image)
            return val


    def begin_game(self, mask_new, mask_old, thresh):
        if(self.already_dead == False):
            if(self.launch == False):
                self.time_decount = time()
                self.soleil.play()
                self.launch = True
            # time() - time_decount > 6.5 ---> the speaker finished his counter and is staring at you
            if(time() - self.time_decount > 6.5):
                # time() - time_decount > 12 ---> the speaker finished staring at you and will count one more time
                if(time() - self.time_decount > 12):
                    # launch set to false to launch the new count
                    self.launch = False

                #print("Displacement norm: ", np.linalg.norm(mask_new - mask_old))
                if(np.linalg.norm(mask_new - mask_old) > thresh):
                    print("GAME OVER")
                    # If it's the first frame of the death part, launch the fire shot music 
                    if(self.musicAlreadyShot == False):
                        self.musicShot.play()
                        self.musicAlreadyShot = True
                    self.already_dead = True
                    return self.end_game()
            key = cv2.waitKey(1)
            if key == ord('r'):
                return "Restart"
            if key == ord('m'):
                return "Menu"
            if key == ord('q'):
                return "Quitter"
            return "Continue"
        else:
            return self.end_game()



def play():

    cap = cv2.VideoCapture(0)

    # Between two frames, the algorithm calculates the difference between the mask of the user of each frame
    # Initialization of the first mask
    mask_old = np.zeros((720, 1280))


    start_time = time()
    launch = 1
    launch = Launch()

    # Threshold admitted to detect a displacement
    thresh = 40

    game_rules = pygame.mixer.Sound("soleil/game_rules.wav")

    # True if the rules have already been explained
    game_rule_launched = False
   # musicAmbiance = pygame.mixer.Sound('biscuit/assets/UnfinishedBusiness.mp3')
   # musicAmbiance.play(fade_ms=2)

    with mp_selfie_segmentation.SelfieSegmentation(
            model_selection=1) as selfie_segmentation:

        while cap.isOpened():
            success,  launch.image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Process the mediapipe segmentation
            # the BGR  image to RGB.
            launch.image = cv2.cvtColor(cv2.flip(launch.image, 1), cv2.COLOR_BGR2RGB)
            launch.image.flags.writeable = False
            results = selfie_segmentation.process(launch.image)
            launch.image.flags.writeable = True
            launch.image = cv2.cvtColor(launch.image, cv2.COLOR_RGB2BGR)
            
            # Launch the explanation of the rules after letting a small time to launch the webcam
            if((time() - start_time > 5) and (game_rule_launched == False)):
                game_rules.play()
                # Rules have been explained
                game_rule_launched = True

            # Launch the counter when the rules are finished
            if(time() - start_time > 25):
                mask_new = results.segmentation_mask
                action = launch.begin_game(mask_new, mask_old, thresh)
                if action == "Continue":
                    pass
                else:
                    return action
                mask_old = mask_new
            
            cv2.imshow('jeu',  launch.image)
            key = cv2.waitKey(1)
            if key == ord('r'):
                return "Restart"
            if key == ord('m'):
                return "Menu"
            if key == ord('q'):
                return "Quitter"
    cap.release()

def runGame():
    while True :
        keyboard = play()
        if keyboard == "Menu":
            return True
        elif keyboard == "Quitter":
            return False

# runGame()