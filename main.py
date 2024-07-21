import time
from extension_board import ExtensionBoard

#board = ExtensionBoard()
#
#board.buzz(1)
#time.sleep(1)
#board.buzz(0)
#
#board.rotate_left(255)
#time.sleep(10)

count = 0

import numpy as np
import cv2
original = np.load("original.npz.npy")
frame = np.load(f"{count}.npz.npy")

pts0 = np.load(f"{count}-mkpts0.npz.npy").astype(np.int)
pts1 = np.load(f"{count}-mkpts1.npz.npy").astype(np.int)

combined_image = np.hstack((original, frame))
for pt1, pt2 in zip(pts0, pts1):
    cv2.circle(combined_image, tuple(pt1), 5, (0, 255, 0), -1)
    cv2.circle(combined_image, (pt2[0] + frame.shape[1], pt2[1]), 5, (0, 255, 0), -1)
    
    # Draw line connecting the points
    cv2.line(combined_image, tuple(pt1), (pt2[0] + frame.shape[1], pt2[1]), (255, 0, 0), 2)
    # cv2.line(concat_img, (pts0[0], pts1[0] + frame.shape[1]), (pts0[1], pts1[1]), (255, 0, 0), 2)
cv2.imwrite('matches.png', combined_image)

print(pts0.shape)
print(pts0)


import matplotlib.pyplot as plt
plt.imsave("temp.jpg", frame)

