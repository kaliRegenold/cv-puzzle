import argparse
import matplotlib.pyplot as plt
import numpy as np
import math
import cv2
from PIL import Image
from find_waldo import find_waldo
from find_pieces import find_pieces
from auxiliary import *
from display import *

def parse_args():
    parser = argparse.ArgumentParser(description="Solve puzzles with computer vision.")
    parser.add_argument("--finished", "-c", help="Path to image of finished puzzle.")
    parser.add_argument("--scattered", "-s", help="Path to image of scattered puzzle.")
    parser.add_argument("--method", "-m", default="convolution", help="Method to solve puzzle. [convolution/test_waldo]")

    return parser.parse_args()

def min_angle_between(ang1, ang2):
    angA = ang1 - 180
    angB = ang2 - 180

    diff1 = min(abs(ang1 - ang2), abs(ang2 - ang1))
    diff2 = min(abs(angA - angB), abs(angB - angA))
    angle = min(diff1, diff2)

    if angle > 300:
        if ang1 > ang2:
            ang2 += 360
        elif ang2 > ang1:
            ang1 += 360
        return min_angle_between(ang1, ang2)
    return angle


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
        val,idx = find_waldo(image, kernel)
        print(val,idx)
        display_waldo(image,kernel,idx)
        return

    if args.method == "test_blob":
        try:
            scattered_image = norm(np_from_img(args.scattered), 255)
        except FileNotFoundError:
            print("Invalid finished image path: " + args.scattered)
        pieces = find_pieces(scattered_image)
        for p in range(0, len(pieces)):
            ## Grab the piece's image, invert, show ##
            piece = pieces[p].descriptor
            piece = 1 - np.uint8(piece)
            plt.imshow(piece)
            plt.show()

            ## Center point of the piece's image chunk ##
            shap = np.shape(piece)
            cent_x = shap[0]//2
            cent_y = shap[1]//2 

            ## Find the puzzle piece's contour ##
            contours, h = cv2.findContours(piece, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            contour_cart = contours[0]
            len_contour = np.shape(contour_cart)
            len_contour = len_contour[0]
            contour_pol = np.zeros((len_contour, 2))

            ## Convert from cartesian to polar, also np.shit to np.nice formatting ##
            for i in range(len(contour_cart)):
                x = contour_cart[i][0][0] - cent_x
                y = contour_cart[i][0][1] - cent_y
                contour_pol[i][0] = math.sqrt((x**2 + y**2))
                contour_pol[i][1] = math.atan2(y, x)*360/(2*np.pi) + 180 # (-180, 180) -> (0, 360)

            ## Grab the average radial distance for the contour ##
            avg_dist = 0
            for i in range(0, len_contour-1):
                avg_dist += contour_pol[i][0]
            avg_dist /= len_contour
            min_dist = contour_pol.min(axis=0)
            min_dist = min_dist[0]
            print("Avg dist from center: {0}, min dist from center: {1}".format(avg_dist, min_dist))

            ## Find all points below avg, and above avg ##
            hole_points = []
            bump_points = []
            avg_min_radius = avg_dist - min_dist
            for i in range(0, len_contour-1):
                if contour_pol[i][0] < avg_dist:
                    hole_points.append(contour_pol[i])
                elif contour_pol[i][0] > avg_dist + avg_min_radius:
                    bump_points.append(contour_pol[i])

            ## Find start and end angles/points for each hole ##
            hole_bounds = []
            max_angle_separation = 10
            last_angle = hole_points[0][1]
            for i in range(0, len(hole_points)-1):
                angle_between = min_angle_between(last_angle, hole_points[i][1])#min(abs(last_angle - hole_points[i][1]), abs(hole_points[i][1] - last_angle))
                print("last_angle: {0}, this_angle: {1}, angle_between: {2}".format(last_angle, hole_points[i][1], angle_between))
                if angle_between > max_angle_separation:
                    hole_bounds.append(i)
                last_angle = hole_points[i][1]
            print(hole_bounds)


            hole_count = len(hole_bounds)//2
            hole = 0
            hole_angles = []
            hole_avg = 0
            while hole < hole_count:
                for i in range(hole_bounds[hole*2], hole_bounds[(hole*2)+1]):
                    hole_avg += hole_points[i][1]
                    hole_avg /= 2.0
                print("Found one hole at theta = {0}".format(hole_avg))
                hole += 1



            ## Show shit ##
            piece[cent_x][cent_y] = 0
            plt.imshow(piece)
            plt.show()
            #plt.savefig("piece" + str(p) + ".jpeg")


if __name__ == "__main__":
    main(parse_args())
