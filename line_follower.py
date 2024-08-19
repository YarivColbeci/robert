from time import sleep

import cv2
import numpy as np

import nanocamera as nano
from extension_board import ExtensionBoard

def get_normalized_alignment(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_bottom = img_gray[-10:]
    img_single_row = img_bottom.mean(axis=0)
    img_grad = img_single_row[1:] - img_single_row[:-1]
    img_grad = np.concatenate((img_grad, [0]))
    img_single_row[np.abs(img_grad) < 3.] = np.inf
    if img_single_row.min() > 100:
        return

    min_index = img_single_row.argmin()
    normalized_alignment = min_index / img_single_row.shape
    return (normalized_alignment * 2 - 1)[0]

cam = nano.Camera()
board = ExtensionBoard()
failures = 0
while True:
    try:
        img = cam.read()
        alignment = get_normalized_alignment(img)
        if not alignment:
            board.buzz(1)
            sleep(1)
            board.buzz(0)
            failures += 1
            if failures >= 3:
                break
            else:
                board.set_both_motors(1., 1.)
                sleep(0.02)
                board.stop_motors()
                sleep(0.02)
                continue
        else:
            failures = 0
        print(alignment)
        left_motor_speed = 0.5 * alignment + 0.5
        right_motor_speed = -0.5 * alignment + 0.5
        board.set_both_motors(left_motor_speed * 2, right_motor_speed * 2)
        sleep(0.01)
        board.stop_motors()
        sleep(0.01)
    except Exception as e:
        board.stop_motors()
        print(e)
        cam.release()
        exit()




