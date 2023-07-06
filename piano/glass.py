# Source from mediapipe: https://google.github.io/mediapipe/solutions/hands.html
#
import numpy as np
import pygame
import random
import cv2
import cvzone
import mediapipe as mp
import utils as animation
import piano.questions as questions
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
pygame.init()

class Glass:

    def __init__(self):

        # Time that begins when the user dies for the forst time, usefull to animate the death
        self.timingVideoGameOver = -30

        # Saved the current image
        self.image = 0

        # Saved the location (region of image) of the glass step
        self.roi_fake = 0
        self.roi_fake_2 = 0
        self.roi = 0
        # Idem but as a mask
        self.mask_fake = 0
        self.mask = 0

        # save the png linked to the glass step
        self.glass_broken = 0
        self.glass = 0

        self.musicShot = pygame.mixer.Sound('biscuit/assets/blood.mp3')

    def end_game(self, x, y, x_broken, size, x_broken_2=0):
            print("Time Gave Over: ", self.timingVideoGameOver)
            if self.timingVideoGameOver < 0:
                self.timingVideoGameOver+=1

                self.roi_fake =self.image[y-size[1]:y, x_broken -size[0]:x_broken]
                self.roi_fake[np.where(self.mask_fake)] = 0
                self.roi_fake += self.glass_broken

                self.roi =self.image[y-size[1]:y, x-size[0]:x]
                self.roi[np.where(self.mask)] = 0
                self.roi += self.glass

                if(x_broken_2 != 0):
                    self.roi_fake_2 =self.image[y-size[1]:y, x_broken_2 -size[0]:x_broken_2]
                    self.roi_fake_2[np.where(self.mask_fake)] = 0
                    self.roi_fake_2 += self.glass_broken
                
                key = cv2.waitKey(1)
                if key == ord('r'):
                    return "Restart"
                if key == ord('m'):
                    return "Menu"
                if key == ord('q'):
                    return "Quitter"
                return "Continue"
                

            elif self.timingVideoGameOver<46:
                if self.timingVideoGameOver<10:
                    imgDead = cv2.imread('biscuit/assets/gameOver/gunShot0'+str(self.timingVideoGameOver)+'.png', cv2.IMREAD_UNCHANGED)
                else :
                    imgDead = cv2.imread('biscuit/assets/gameOver/gunShot'+str(self.timingVideoGameOver)+'.png', cv2.IMREAD_UNCHANGED)
                    
                self.image = cvzone.overlayPNG(self.image, cv2.flip(imgDead, 1))
                self.timingVideoGameOver+=1

                if self.timingVideoGameOver==2:                            
                    self.musicShot.play()

                if self.timingVideoGameOver==45:
                    self.save_last_image =  self.image
                    print("Last image saved")
                #cv2.imshow("jeu",  self.image)
                key = cv2.waitKey(1)
                if key == ord('r'):
                    return "Restart"
                if key == ord('m'):
                    return "Menu"
                if key == ord('q'):
                    return "Quitter"
                return "Continue"
            elif self.timingVideoGameOver<100:
                #cv2.imshow('last', self.save_last_image)
                val = animation.afficher_game_over(cv2.flip(self.save_last_image,1))
                return val


def play():
    # For webcam input:
    cap = cv2.VideoCapture(0)
    draw_landmark = False

    launch = Glass()

    # Load the various possibilities for the glass step
    launch.glass = cv2.imread('piano/glass.png')
    glass_fake = cv2.imread('piano/glass_fake.png')
    launch.glass_broken = cv2.imread('piano/glass_broken.png')

    size = (140, 70)
    score = 0  # Initialize the score
    step = 0 


    # Resize the images
    launch.glass = cv2.resize(launch.glass, size)
    glass_fake = cv2.resize(glass_fake, size)
    launch.glass_broken = cv2.resize(launch.glass_broken, size)

    # Intitialization of the sound background
    mixer = pygame.mixer
    mixer.init()
    music_burst = mixer.Sound('piano/burst.wav')
    music_flicker = mixer.Sound('piano/flicker.wav')
    musicAmbiance = pygame.mixer.Sound('biscuit/assets/UnfinishedBusiness.mp3')
    musicAmbiance.play(fade_ms=2)


    broken = False

    # Create a mask for the localisation of the glass step
    img2gray = cv2.cvtColor(launch.glass, cv2.COLOR_BGR2GRAY)
    _, launch.mask = cv2.threshold(img2gray, 250, 255, cv2.THRESH_BINARY_INV)
    img2gray = cv2.cvtColor(glass_fake, cv2.COLOR_BGR2GRAY)
    _, launch.mask_fake = cv2.threshold(img2gray, 250, 255, cv2.THRESH_BINARY_INV)
    touched = True

    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, launch.image = cap.read()

            # To improve performance, optionally mark thelaunch.image as not writeable to
            # pass by reference.
            launch.image.flags.writeable = False
            launch.image = cv2.cvtColor(launch.image, cv2.COLOR_BGR2RGB)
            results = hands.process(launch.image)
            launch.image.flags.writeable = True
            launch.image = cv2.cvtColor(launch.image, cv2.COLOR_RGB2BGR)

            image_height,image_width, c =launch.image.shape  # get image shape

            # Enter this loop if the user has not lost yet
            if(broken == False):
                # Fist part of the game, the 5 first questions Right or Wrong
                if(step <6):
                    if (touched == True):
                        # Initialize the questions
                        question_list = questions.questions_bool()
                        n = len(question_list)
                        # Choice of a random question
                        index = np.random.randint(0, n)
                        epsilon = question_list[index][1]
                        question = question_list[index][0]
                        print("epsilon", epsilon)
                        # Position of the two possible glass step (x for the safe one and x_broken for the broken one)
                        x = 600 + epsilon * 200
                        y = 650 - step * 100
                        touched = False    
                        x_broken = 600 + (1 - epsilon) * 200

                    # Display the questions and the answers on the screen
                    launch.image = cv2.flip(launch.image, 1)
                    if(step < 2):
                        cv2.putText(img =launch.image, text = question, org = (50, 400), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.0, color = (0, 0, 255), thickness = 4)
                    else:
                        cv2.putText(img =launch.image, text = question, org = (50, 600), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.0, color = (0, 0, 255), thickness = 4)

                    cv2.putText(img =launch.image, text = 'RIGHT', org = (700, 700), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.0, color = (0, 0, 255), thickness = 4)
                    cv2.putText(img =launch.image, text = 'WRONG', org = (500, 700), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.0, color = (0, 0, 255), thickness = 4)
                    
                    launch.image = cv2.flip(launch.image, 1)


                    # Region of image (ROI), where we want to insert the glass
                    launch.roi =launch.image[y-size[1]:y, x-size[0]:x]
                    launch.roi_fake =launch.image[y-size[1]:y, x_broken -size[0]:x_broken]
                    launch.roi[np.where(launch.mask)] = 0
                    launch.roi_fake[np.where(launch.mask_fake)] = 0
                    launch.roi += launch.glass
                    launch.roi_fake += glass_fake

                    if results.multi_hand_landmarks:

                        # iterate on all detected hand landmarks
                        for hand_landmarks in results.multi_hand_landmarks:
                        # we can get points using mp_hands
                            pos_x = (
                                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x) * image_width
                            pos_y = (
                                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y) * image_height

                            if((x-size[0] <pos_x) and (pos_x < x) and (y-size[1] < pos_y) and (pos_y  < y)):
                                touched = True           
                                music_flicker.play()
                                step += 1

                                score += 1
                                print("Score: ", score)

                            elif((x_broken-size[0] <pos_x) and (pos_x < x_broken) and (y-size[1] < pos_y) and (pos_y  < y)):        
                                music_burst.play ()
                                broken = True               
                                action = launch.end_game(x, y, x_broken, size)
                                if action == "Continue":
                                    pass
                                else:
                                    print(action)
                                    return action
                                

                # Second part of the game, the QCM game
                elif(step < 12):
                    if (touched == True):
                        # initialize the questions
                        question_list = questions.questions_choice()
                        n = len(question_list)
                        # CHoice of a random question
                        index = np.random.randint(0, n)
                        epsilon = question_list[index][4]
                        print("epsilon", epsilon)
                        x = 500 + epsilon * 200
                        y = 650 - (step - 6) * 100
                        touched = False
                        if(epsilon == 0):    
                            x_broken =500 + 2 * 200
                            x_broken_2 = 500 +  1 * 200
                        elif(epsilon == 1):
                            x_broken =500 + 2 * 200
                            x_broken_2 = 500 +  0 * 200
                        elif(epsilon == 2):
                            x_broken =500 + 0 * 200
                            x_broken_2 = 500 +  1 * 200

                    launch.image = cv2.flip(launch.image, 1)
                    if(step < 8):
                        cv2.putText(img =launch.image, text = question_list[index][0], org = (50, 400), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.0, color = (0, 0, 255), thickness = 4)
                    else:
                        cv2.putText(img =launch.image, text = question_list[index][0], org = (50, 600), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.0, color = (0, 0, 255), thickness = 4)

                    cv2.putText(img =launch.image, text = question_list[index][1], org = (800, 700), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.0, color = (0, 0, 255), thickness = 4)
                    cv2.putText(img =launch.image, text = question_list[index][2], org = (550, 700), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.0, color = (0, 0, 255), thickness = 4)
                    cv2.putText(img =launch.image, text = question_list[index][3], org = (300, 700), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.0, color = (0, 0, 255), thickness = 4)
                    launch.image = cv2.flip(launch.image, 1)
                

                    # Region of image (ROI), where we want to insert the glass
                    launch.roi =launch.image[y-size[1]:y, x-size[0]:x]
                    launch.roi_fake =launch.image[y-size[1]:y, x_broken -size[0]:x_broken]
                    launch.roi_fake_2 =launch.image[y-size[1]:y, x_broken_2 -size[0]:x_broken_2]

                    # Set an index of where the mask is
                    launch.roi[np.where(launch.mask)] = 0
                    launch.roi_fake[np.where(launch.mask_fake)] = 0
                    launch.roi_fake_2[np.where(launch.mask_fake)] = 0
                    launch.roi += launch.glass
                    launch.roi_fake += glass_fake
                    launch.roi_fake_2 += glass_fake

                    if results.multi_hand_landmarks:

                        # iterate on all detected hand landmarks
                        for hand_landmarks in results.multi_hand_landmarks:
                        # we can get points using mp_hands
                            pos_x = (
                                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x) * image_width
                            pos_y = (
                                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y) * image_height

                            if((x-size[0] <pos_x) and (pos_x < x) and (y-size[1] < pos_y) and (pos_y  < y)):
                                touched = True           
                                music_flicker.play()
                                step += 1

                                score += 1
                                print("Score: ", score)

                            elif((x_broken-size[0] <pos_x) and (pos_x < x_broken) and (y-size[1] < pos_y) and (pos_y  < y)):        
                                music_burst.play ()
                                broken = True
                                action = launch.end_game(x, y, x_broken, size, x_broken_2)
                                if action == "Continue":
                                    pass
                                else:
                                    print(action)
                                    return action
                            
                            elif((x_broken_2-size[0] <pos_x) and (pos_x < x_broken_2) and (y-size[1] < pos_y) and (pos_y  < y)):        
                                music_burst.play ()
                                broken = True
                                action = launch.end_game(x, y, x_broken, size, x_broken_2)
                                if action == "Continue":
                                    pass
                                else:
                                    print(action)
                                    return action
                elif step == 12:
                    return animation.afficher_win(cv2.flip(launch.image,1))


                
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
            


            if(draw_landmark == True):
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                           launch.image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())




            if(broken == True):
                action = launch.end_game(x, y, x_broken, size)
                if action == "Continue":
                    pass
                else:
                    print(action)
                    return action

            launch.image = cv2.flip(launch.image, 1)
            cv2.putText(img =launch.image, text = str(score), org = (70, 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 3.0, color = (255, 255, 255), thickness = 3)
            cv2.putText(img =launch.image, text = "WATCH YOUR STEP", org = (200, 120), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale = 3.0, color = (0, 0, 255), thickness = 9)

            cv2.imshow('jeu',launch.image)
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