import sys
import cv2
import numpy as np
import prep as p
import HuffManCoding as hcoding

# cover_image_loc = "./"+str(input("Choose a cover image in PNG format: "))
np.set_printoptions(threshold=sys.maxsize)
uncompressed_image = "./cat_secret.png"
# stego_image_loc = "./"+str(input("Choose name of the stego image: "))
# secret_message = input("Enter your secret message: ");
# print(cover_image_loc)
# print(stego_image_loc)
# print(secret_message)

# Start the operation
read_cover_image = cv2.imread(uncompressed_image,flags = cv2.IMREAD_COLOR)
height = read_cover_image.shape[0]
width = read_cover_image.shape[1]
if height%8: height+=(8-height%8)
if width%8: width+=(8-width%8)
# width = height
req_dim = height
if height>width: req_dim = width
new_valid_dim = (width,height)
padded_image = cv2.resize(read_cover_image,new_valid_dim)
# cover_image_float = np.float32(padded_image)
cover_image_float = np.float32(padded_image)
converted = cv2.cvtColor(cover_image_float,cv2.COLOR_BGR2YCrCb)

# split the matrix into different channels of YCrCb
new_operable_mat = [p.split_image(height,width,converted[:,:,0]),p.split_image(height,width,converted[:,:,1]),p.split_image(height,width,converted[:,:,2])]
huffman_list = []

for channels in range(3):
    dct_2 = [[cv2.dct(x) for x in new_operable_mat[channels][i]] for i in range(int(height/8))]
    # Quantization stage
    quantized = [[np.around(np.divide(x,p.QUANT_TABLE)) for x in dct_2[i]] for i in range(int(height/8))]
    items = np.array(quantized).flatten()
    # print(items)
    for m in items:
    	huffman_list.append(str(m))

# print(huffman_list)
myHuffmanTree = hcoding.huffManTree(huffman_list)
mySymbols = hcoding.PreOrder(myHuffmanTree[0],myHuffmanTree[1])
print(mySymbols)

