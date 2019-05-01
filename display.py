#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
from piece import Piece
from matplotlib.patches import Rectangle

def display_final(pieces, scattered_image, solved_image):
	scattered_x = np.array([piece.img_x for piece in pieces])
	scattered_y = np.array([piece.img_y for piece in pieces])
	solved_x = np.array([piece.solved_x for piece in pieces])
	print(solved_x)
	solved_x = solved_x + scattered_image.shape[1]
	solved_y = np.array([piece.solved_y for piece in pieces])

	both_images = np.concatenate((scattered_image,solved_image),1)
	plt.imshow(both_images)

	plt.plot(scattered_x,scattered_y,'ro')
	plt.plot(solved_x,solved_y,'ro')

	for i in range(0, len(scattered_x)):
		plt.plot((scattered_x[i],solved_x[i]),(scattered_y[i],solved_y[i]),'-r')
	
	plt.show()

def display_waldo(image, kernel, kernel_idx):
    fig,ax = plt.subplots(1)
    ax.imshow(image)
    ax.add_patch(Rectangle((kernel_idx[1],kernel_idx[0]),kernel.shape[1],kernel.shape[0],linewidth=2,edgecolor='r',facecolor='none'))
    plt.figure()
    plt.imshow(kernel)
    plt.show()


if __name__ == "__main__":
	num_points = 30
	
	img1 = mpimg.imread('images/bork_and_bun.jpeg')
	img2 = mpimg.imread('images/bork_and_bun.jpeg')

	offset = img2.shape[1]

	x_left = np.random.randint(0,img1.shape[1],num_points)
	y_left = np.random.randint(0,img1.shape[0],num_points)

	x_right = x_left #np.random.randint(0,img1.shape[1],num_points)
	y_right = y_left #np.random.randint(0,img1.shape[0],num_points)

	pieces = []

	print(x_left)
	print(x_right)

	for i in range(0,num_points-1):
		pieces.append(Piece(3,x_left[i],y_left[i],x_right[i],y_right[i]))

	display_final(pieces,img1,img2)

