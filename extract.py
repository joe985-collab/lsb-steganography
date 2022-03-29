import struct
import bitstring
import numpy as np
import start as src
import prep as p
import cv2
from sympy import fwht
def extract_encoded_data_from_DCT(blocks):
    count = 0
    store = 999
    sets = True
    extracted_data = ""
    for current in  blocks:
        # print(current)
        for bits in current:
            # print(round(bits))
            if count==3 and sets:
                store = int(extracted_data.read('uint:8')/4)
                extracted_data.pos = 0
                sets = False
            curr_coeff = round(bits)
            extracted_data += bitstring.pack('uint:1',  np.uint8(curr_coeff)&0x01)
        count+=1
        if(count>store+1):
            return extracted_data

stego_image     = cv2.imread(src.stego_image_loc, flags=cv2.IMREAD_COLOR)
stego_image_f32 = np.float32(stego_image)
height,width = stego_image_f32.shape[:2]
converted = cv2.cvtColor(stego_image_f32, cv2.COLOR_BGR2YCrCb)
new_mat = [p.split_image(height,width,converted[:,:,0])]
dims = np.array(new_mat[0]).shape
dct_blocks = [[cv2.dct(block) for block in new_mat[0][i]] for i in range(int(width/8))]
dct_quants = [[np.divide(item, p.QUANT_TABLE) for item in dct_blocks[i]] for i in range(int(width/8))]
# print("DCT Quants:\n")
# print(dct_quants)
# print(np.array(dct_quants).shape)
reshaped = np.array(dct_quants).reshape(dims[0]*dims[1],dims[2]*dims[3])
# print(reshaped)
hadamard = [fwht(blk[:4])for blk in reshaped]
# print(hadamard)
# # s
# dct_quants = [np.divide(item, jpg) for item in dct_blocks]
# # print("dct quants: \n")
# # print(dct_quants) 
# reshaped = np.reshape(dct_quants,(14,64))
# # sorted_coefficients = [zz.zigzag(block) for block in dct_quants]
#
# # print(hadamard)
recovered_data = extract_encoded_data_from_DCT(hadamard)
data_len = int(recovered_data.read('uint:8')/8)
# print(data_len)
# print(recovered_data)
extracted_data = bytes()
for i in range(data_len): extracted_data += struct.pack('>B', recovered_data.read('uint:8'))

print(extracted_data.decode('ascii'))