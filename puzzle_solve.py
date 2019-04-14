import argparse
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from find_waldo import find_waldo
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

if __name__ == "__main__":
    main(parse_args())
