import numpy as np
from PIL import Image
import math

def np_from_img(fname):
    return np.asarray(Image.open(fname).convert('L'), dtype=np.float32)

def norm(ar, val):
    temp = ar-np.min(ar)
    return val*(temp/np.max(temp))

def cart_to_polar(x, y):
    radius = math.sqrt((x**2 + y**2))
    angle = -math.degrees(math.atan2(y, x))
    return radius, angle

def polar_to_cart(radius, angle):
    x = math.floor(radius*math.cos(math.radians(angle)))
    y = math.floor(radius*math.sin(math.radians(angle)))
    return x, y

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