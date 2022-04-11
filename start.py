# Required Libraries
import sys
import cv2
import embed
import numpy as np
import prep as p
# cover_image_loc = "./"+str(input("Choose a cover image in PNG format: "))
np.set_printoptions(threshold=sys.maxsize)
cover_image_loc = "./cat.png"
stego_image_loc = "./cat_message.png"
# msg = "Meet me at this place at 9 am"
msg = "Meet me at XYZ by 9 am sharp tomorrow."
msg_length = len(msg)
msg1 = str(msg_length)+msg
# print(msg1[1].isnumeric())
binary_msg = ' '.join(format(ord(x), 'b') if int(ord(x))>63 else '0'+format(ord(x), 'b')  for x in msg1).replace(" ","")
secret_data = binary_msg
# print(binary_msg)
# for i in range(0,len(binary_msg),7):
#     tst =  binary_msg[i:i+7]
#     secret_data += chr(int(tst,2))
# stego_image_loc = "./"+str(input("Choose name of the stego image: "))
# secret_message = input("Enter your secret message: ");
# print(cover_image_loc)
# print(stego_image_loc)
# print(secret_message)

# Start the operation
read_cover_image = cv2.imread(cover_image_loc,flags = cv2.IMREAD_COLOR)
height = read_cover_image.shape[0]
width = read_cover_image.shape[1]
# print(height)
# print(width)

#Pad the image to be 8x8 compliant
if height%8: height+=(8-height%8)
if width%8: width+=(8-width%8)
# width = height
req_dim = height
if height>width: req_dim = width
new_valid_dim = (width,height)
padded_image = cv2.resize(read_cover_image,new_valid_dim)
cover_image_float = np.float32(padded_image)
converted = cv2.cvtColor(cover_image_float,cv2.COLOR_BGR2YCrCb)

# split the matrix into different channels of YCrCb
new_operable_mat = [p.split_image(height,width,converted[:,:,0]),p.split_image(height,width,converted[:,:,1]),p.split_image(height,width,converted[:,:,2])]
# print(new_operable_mat)
# print(np.array(new_operable_mat).shape)
stego_image_float = np.empty_like(cover_image_float)
# dims = np.array(new_operable_mat).shape
# print(new_operable_mat[0])
# new_operable_mat = np.array(new_operable_mat).reshape(dims[0],dims[1]*dims[2],dims[3],dims[4])
# print(new_operable_mat.shape)

# secret_data = ""
# for char in msg.encode('ascii'): secret_data += bitstring.pack('uint:8', char)
# embedded_dct_blocks   = stego.embed_encoded_data_into_DCT(secret_data, sorted_coefficients)
# print(secret_data)


#Now starts the meat and potatoes of the program

for channels in range(3):
    # Forward 2-D DCT on the converted Image blocks
    dct_2 = [[cv2.dct(x) for x in new_operable_mat[channels][i]] for i in range(int(req_dim/8))]
    # Quantization stage
    quantized = [[np.around(np.divide(x,p.QUANT_TABLE)) for x in dct_2[i]] for i in range(int(req_dim/8))]
    # print(quantized[0][0].shape)
    # print(dct_2)
    transformed = embed.embed_encoded_data_into_DCT(secret_data,quantized)


    # DeQuantization stage
    dequantized = [[np.multiply(x,p.QUANT_TABLE) for x in transformed[i]] for i in range(int(req_dim/8))]
    #Apply IDCT
    idct_blocks = [[cv2.idct(np.float32(x)) for x in dequantized[i]] for i in range(int(req_dim/8))]
     # Rebuild full image channel into the stego image
    stego_image_float[:,:,channels] = np.asarray(p.orig_dim_image(idct_blocks))
# Convert back to RGB (BGR) Colorspace
stego_image_BGR = cv2.cvtColor(stego_image_float, cv2.COLOR_YCR_CB2BGR)

# # Clamp Pixel Values to [0 - 255]
final_stego_image = np.uint8(np.clip(stego_image_BGR, 0, 255))
# print(final_stego_image)
# # Write stego image
cv2.imwrite(stego_image_loc, final_stego_image)

