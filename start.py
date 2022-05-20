# Required Libraries
import sys
import cv2
import embed
from timeit import default_timer as timer
import numpy as np
import prep as p
from PIL import Image
# from scipy.fftpack import dct,idct
# cover_image_loc = "./"+str(input("Choose a cover image in PNG format: "))
# start = timer()
np.set_printoptions(threshold=sys.maxsize)
# cover_image_loc = "./public/Maltese.bmp"
# stego_image_loc = "./public/malteses.bmp"
# cover_image_loc = "./public/bees.png"
# stego_image_loc = "./public/beegies.png"
cover_image_loc = "./public/Lenna.png"
stego_image_loc = "./public/lennaz.png"
# msg = "Meet me at this place at 9 am"
msg = "This is a secret message."
msg_length = len(msg)
msg1 = str(msg_length)+msg
binary_msg = ' '.join(format(ord(x), 'b') if int(ord(x))>63 else '0'+format(ord(x), 'b')  for x in msg1).replace(" ","")
secret_data = binary_msg

# Start the operation
read_cover_image = cv2.imread(cover_image_loc,flags = cv2.IMREAD_COLOR)
# print(read_cover_image)
height = read_cover_image.shape[0]
width = read_cover_image.shape[1]


# Pad the image to be 8x8 compliant
if height%8: height+=(8-height%8)
if width%8: width+=(8-width%8)
# The required dimension will be the larger number
# iters = 0
new_valid_dim = (width,height)
padded_image = cv2.resize(read_cover_image,new_valid_dim)
cover_image_float = np.float32(padded_image)
converted = cv2.cvtColor(cover_image_float,cv2.COLOR_BGR2YCrCb)

# split the matrix into different channels of YCrCb
new_operable_mat = [p.split_image(height,width,converted[:,:,0]),p.split_image(height,width,converted[:,:,1]),p.split_image(height,width,converted[:,:,2])]
req_dim = np.array(new_operable_mat).shape[1]
# print(np.array(new_operable_mat).shape)
stego_image_float = np.empty_like(cover_image_float)



#Now starts the meat and potatoes of the program

for channels in range(3):
    # Forward 2-D DCT on the converted Image blocks
    dct_2 = [[cv2.dct(x) for x in new_operable_mat[channels][i]] for i in range(req_dim)]
    # print(np.block(dct_2).shape)
    # while(stego_image_float[:,:,channels].shape != np.block(dct_2).shape):
    #     if iters>1: break
    #     req_dim = not_req_dim
    #     dct_2 = [[cv2.dct(x) for x in new_operable_mat[channels][i]] for i in range(int(req_dim/8))]
    #     iters += 1
    # for i in range(135):
    #     print(np.array(new_operable_mat[channels][i]).shape)
    # Quantization stage
    quantized = [[np.around(np.divide(x,p.QUANT_TABLE)) for x in dct_2[i]] for i in range(req_dim)]

    transformed = embed.embed_encoded_data_into_DCT(secret_data,quantized)

    # DeQuantization stage
    dequantized = [[np.multiply(x,p.QUANT_TABLE) for x in transformed[i]] for i in range(req_dim)]
    #Apply IDCT
    idct_blocks = [[cv2.idct(np.float32(x)) for x in dequantized[i]] for i in range(req_dim)]
     # Rebuild full image channel into the stego image
    # print(np.array(idct_blocks).shape)
    stego_image_float[:,:,channels] = np.asarray(p.orig_dim_image(idct_blocks))



# print("Initial")
# print(stego_image_float)
# Convert back to RGB (BGR) Colorspace
# if iters>1:
#     print("The image is not suitable for steganography")
# else:    
stego_image_BGR = cv2.cvtColor(stego_image_float, cv2.COLOR_YCR_CB2BGR)
#Clamp Pixel Values to [0 - 255]
final_stego_image = np.uint8(np.clip(stego_image_BGR, 0, 255))
#Write stego image
cv2.imwrite(stego_image_loc, final_stego_image)
# end = timer()
# print(end - start)
# cv2.imwrite(stego_image_loc, stego_image_BGR)
# jaks = cv2.cvtColor(np.float32(stego_image_BGR),cv2.COLOR_BGR2YCrCb)
# print("After conversion")
# print(jaks)



