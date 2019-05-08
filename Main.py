import numpy as np
from PIL import ImageGrab
import cv2

while (True):
    screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
    cv2.imshow('window', screen)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break