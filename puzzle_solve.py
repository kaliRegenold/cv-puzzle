import argparse
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from find_waldo import find_waldo
from find_pieces import find_pieces
from auxiliary import *

def parse_args():
    parser = argparse.ArgumentParser(description="Solve puzzles with computer vision.")
    parser.add_argument("--finished", "-c", help="Path to image of finished puzzle.")
    parser.add_argument("--scattered", "-s", help="Path to image of scattered puzzle.")
    parser.add_argument("--method", "-m", default="convolution", help="Method to solve puzzle. [convolution/test_waldo]")

    return parser.parse_args()

def main(args):
    if args.method == "test_waldo":
        try:
            image = norm(np_from_img(args.finished), 1)
        except FileNotFoundError:
            print("Invalid finished image path: " + args.finished)

        try:
            kernel = norm(np_from_img(args.scattered),2) - 1
        except FileNotFoundError:
            print("Invalid scattered image path: " + args.scattered)

        print(find_waldo(image, kernel))
        return

    if args.method == "test_blob":
        try:
            scattered_image = norm(np_from_img(args.scattered), 255)
        except FileNotFoundError:
            print("Invalid finished image path: " + args.scattered)
        pieces = find_pieces(scattered_image)
        # for p in range(0, len(pieces)):
        #     plt.imshow(pieces[p], cmap="gist_gray")
        #     plt.savefig("piece" + str(p) + ".jpeg")


if __name__ == "__main__":
    main(parse_args())
