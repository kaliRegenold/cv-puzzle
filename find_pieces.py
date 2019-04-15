import cv2
import numpy as np
from piece import Piece

def find_pieces(scattered_image, threshold = (255/2)):
    params = cv2.SimpleBlobDetector_Params()
    params.filterByConvexity = True
    params.minConvexity = 0.1

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(scattered_image.astype(np.uint8))

    pieces = []
    for k in keypoints:
        radius = int((k.size/2) * 1.4)
        x, y = int(k.pt[0]), int(k.pt[1])
        print(radius, x, y)
        piece = np.ones((radius*2, radius*2))
        indices = scattered_image[y-radius:y+radius, x-radius:x+radius] < threshold
        piece[indices] = 0
        pieces.append(Piece(piece, x, y))

    return pieces
