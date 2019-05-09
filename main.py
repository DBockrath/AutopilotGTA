import numpy as np
from PIL import ImageGrab
import cv2
import time
from directkeys import PressKey, ReleaseKey, W, A, S, D

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    return processed_img

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)

while (True):
    screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
    new_screen = process_img(screen)
    # print('Down')
    # PressKey(W)
    # time.sleep(3)
    # print('Up')
    # ReleaseKey(W)
    cv2.imshow('Screen', cv2.cvtColor(new_screen, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break