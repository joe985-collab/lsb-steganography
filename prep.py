#Import Libraries
import cv2
import numpy as np


#DCT Quantiztion Table given by JPEG

QUANT_TABLE = 			np.asarray([
                                        [16, 11, 10, 16,  24, 40,   51,  61],
                                        [12, 12, 14, 19,  26, 58,   60,  55],
                                        [14, 13, 16, 24,  40, 57,   69,  56],
                                        [14, 17, 22, 29,  51, 87,   80,  62],
                                        [18, 22, 37, 56,  68, 109, 103,  77],
                                        [24, 36, 55, 64,  81, 104, 113,  92],
                                        [49, 64, 78, 87, 103, 121, 120, 101],
                                        [72, 92, 95, 98, 112, 100, 103,  99]
                                      ],
                                      dtype = np.float32)








# Splits an image into 8x8 blocks
def split_image(h,w,image):
    splitted = np.split(image,int(h/8),axis=0)
    blks = [np.split(k,int(w/8),axis=1) for k in splitted]
    return blks

# Converts the image matrix to its original dimensions (stego image)
def orig_dim_image(image):
    return np.block(image)

