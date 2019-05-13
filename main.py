import numpy as np
from PIL import ImageGrab
import cv2
import time
from directkeys import PressKey, ReleaseKey, W, A, S, D
from draw_lanes import draw_lanes
import pyautogui


def draw_lines(img, lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 255], 3)

    except:
        pass


def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked


def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)

    vertices = np.array([[24, 800], [24, 480], [720, 320], [1200, 320], [1920, 480], [1920, 800]])  # [x2.4, x1.6]
    processed_img = roi(processed_img, [vertices])

    lines = cv2.HoughLinesP(processed_img, 1, np.pi / 180, 180, np.array([]), 100, 5)
    draw_lines(processed_img, lines)

    lines = cv2.HoughLinesP(processed_img, 1, np.pi / 180, 180, 20, 15)
    m1 = 0
    m2 = 0

    try:

        l1, l2, m1, m2 = draw_lanes(original_image, lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0, 255, 0], 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0, 255, 0], 30)

    except Exception as e:

        print(str(e))
        pass

    try:

        for coords in lines:
            coords = coords[0]

            try:

                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 0, 0], 3)


            except Exception as e:

                print(str(e))

    except Exception as e:

        pass

    return processed_img, original_image, m1, m2


def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


def left():
    PressKey(A)
    ReleaseKey(W)
    ReleaseKey(D)
    ReleaseKey(A)


def right():
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)


def slow_down():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


for i in list(range(4))[::-1]:
    print(i + 1)
    time.sleep(1)

while (True):
    screen = np.array(ImageGrab.grab(bbox=(0, 40, 1920, 1080)))  # (0, 40, 800, 640)
    new_screen, original_image, m1, m2 = process_img(screen)
    # cv2.imshow('Lines', cv2.cvtColor(new_screen, cv2.COLOR_BGR2RGB))
    cv2.imshow('Lanes', cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))

    if m1 < 0 and m2 < 0:
        right()
    elif m1 > 0 and m2 > 0:
        left()
    else:
        straight()

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
