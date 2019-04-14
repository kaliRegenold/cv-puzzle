import matplotlib.pyplot as plt
import numpy as np
from scipy import signal as sg
from auxiliary import *


def find_waldo(image, kernel):
    k = kernel
    rot0 = sg.correlate(image, k, "valid")
    k = np.rot90(k)
    rot1 = sg.correlate(image, k, "valid")
    k = np.rot90(k)
    rot2 = sg.correlate(image, k, "valid")
    k = np.rot90(k)
    rot3 = sg.correlate(image, k, "valid")

    rots = [rot0, rot1, rot2, rot3]
    matches = [np.max(r) for r in rots]
    best_match = rots[matches.index(max(matches))]

    return (np.max(best_match), np.unravel_index(best_match.argmax(), best_match.shape))
