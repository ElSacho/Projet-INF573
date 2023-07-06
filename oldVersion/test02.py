from pynput.keyboard import Key, Controller
import time
import pyautogui


keyboard = Controller()

time.sleep(3)
print(1)
keyboard.press('a')
keyboard.release('a')
keyboard.type('x')
pyautogui.typewrite("asfdasdfs")
print(2)