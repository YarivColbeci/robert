import argparse
import time
import os
import cv2
import numpy as np
from loftr.utils.cvpr_ds_config import default_cfg
from utils import make_query_image, get_coarse_match, make_student_config
import nanocamera as nano
from trtmodel import TRTModel
from extension_board import ExtensionBoard
import time
board = ExtensionBoard()

engine_path = "/home/jetson/Documents/robert/weights/LoFTR_teacher.trt"

def take_topk(mkpts0, mkpts1, mconf, n_top=20):
    indices = np.argsort(mconf)[::-1]
    indices = indices[:n_top]
    mkpts0 = mkpts0[indices, :]
    mkpts1 = mkpts1[indices, :]
    return mkpts0, mkpts1


def main():
    model_cfg = default_cfg

    print('Loading pre-trained network...')
    matcher = TRTModel(engine_path=engine_path)
    print('Successfully loaded TensorRT model.')

    print('Opening camera...')

    img_size = (model_cfg['input_width'], model_cfg['input_height'])
    loftr_coarse_resolution = model_cfg['resolution'][0]

    img1_bgr = cv2.imread('1.jpg')
    img2_bgr = cv2.imread('2.jpg')

    # Convert BGR images to RGB
    img1_rgb = cv2.cvtColor(img1_bgr, cv2.COLOR_BGR2RGB)
    img2_rgb = cv2.cvtColor(img2_bgr, cv2.COLOR_BGR2RGB)
    
    frame0 = make_query_image(img1_rgb, img_size)
    frame1 = make_query_image(img2_rgb, img_size)

    img0 = frame0[None][None] / 255.0
    img1 = frame1[None][None] / 255.0

    conf_matrix = matcher(img0, img1).reshape((1, 1200, 1200))
    mkpts0, mkpts1, mconf = get_coarse_match(conf_matrix, img_size[1], img_size[0], loftr_coarse_resolution)

    mkpts0 = mkpts0.astype(np.int)
    mkpts1 = mkpts1.astype(np.int)

    print('shape', img1_rgb.shape)

    combined_image = np.hstack((img1_rgb, img2_rgb))
    for pt1, pt2 in zip(mkpts0, mkpts1):
        cv2.circle(combined_image, tuple(pt1), 5, (0, 255, 0), -1)
        cv2.circle(combined_image, (pt2[0] + img1_rgb.shape[0], pt2[1]), 5, (0, 255, 0), -1)
        
        # Draw line connecting the points
        cv2.line(combined_image, tuple(pt1), (pt2[0] + img1_rgb.shape[0], pt2[1]), (255, 0, 0), 2)
    cv2.imwrite('matches.png', combined_image)

    
if __name__ == "__main__":
    main()
