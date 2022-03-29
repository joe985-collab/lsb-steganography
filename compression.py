import sys
import cv2
import numpy as np
import prep as p

# cover_image_loc = "./"+str(input("Choose a cover image in PNG format: "))
np.set_printoptions(threshold=sys.maxsize)
cover_image_loc = "./cat.png"
# stego_image_loc = "./"+str(input("Choose name of the stego image: "))
# secret_message = input("Enter your secret message: ");
# print(cover_image_loc)
# print(stego_image_loc)
# print(secret_message)

# Start the operation
read_cover_image = cv2.imread(cover_image_loc,flags = cv2.IMREAD_COLOR)
height = read_cover_image.shape[0]
width = read_cover_image.shape[1]