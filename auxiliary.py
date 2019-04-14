import numpy as np
from PIL import Image

def np_from_img(fname):
    return np.asarray(Image.open(fname).convert('L'), dtype=np.float32)

def norm(ar, val):
    temp = ar-np.min(ar)
    return val*(temp/np.max(temp))
