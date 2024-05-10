import pyautogui
import cv2
import numpy as np
import time
from PIL import ImageGrab

pyautogui.FAILSAFE = False

def identifyCoordinateOfTarget(screen, target):
    target = cv2.imread(target)
    result = cv2.matchTemplate(screen, target, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.8:  # Adjust threshold for better/worse matches
        top_left = max_loc
        bottom_right = (top_left[0] + target.shape[1], top_left[1] + target.shape[0])
        center = ((top_left[0]+bottom_right[0])/2, (top_left[1]+bottom_right[1])/2)
        return center
    else: return False

def press(*targets, delay=0):
    screen = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
    
    for target in targets:
        point = identifyCoordinateOfTarget(screen, target=target)
        pyautogui.click(point[0], point[1], button='left')
        time.sleep(delay)

def waitToPress(target, waitfor):
    screen = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
    waitingPoint = identifyCoordinateOfTarget(screen, target=waitfor)
    if not waitingPoint: waitToPress(target, waitfor)
    else:
        targetPoint = identifyCoordinateOfTarget(screen, target=target)
        pyautogui.click(targetPoint[0], targetPoint[1], button='left')

if __name__ == '__main__':
    press('target2.png', 'target1.png', delay=1)
    time.sleep(3) # Exception to be late for activing audio
    waitToPress(target='target2.png', waitfor='target1.png')
    print("The job has been finished.")
    

