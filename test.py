import numpy as np
import sys
import cv2
from sympy import fwht,ifwht
import bitstring
import struct
from prep import QUANT_TABLE as jpg

#msg = "What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills."
msg = "Hello!"
tst =   [[20,  0, -1,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0], [20, 0, -1, -1,  0, 0,  0, 0,  0, 0, 0,  0,  0,
       0,  0,  0,  0, 0,  0, 0, 0,  0,  0,  0,  0, 0,
        0,  0,  0, 0,  0,  0, 0, 0,  0, 0, 0, 0,  0,
       0, 0, 0, 0,  0, 0,  0, 0, 0, 0, 0,  0, 0,
        0,  0, 0, 0,  0,  0, 0,  0,  0,  0, 0,  0], [20, 0, -1, 0, 0,  0, 0, 0, 0, 0, 0,  0, 0,
       0, 0, 0,  0, 0,  0, 0, 0,  0, 0,  0, 0, 0,
        0, 0, 0,  0, 0,  0,  0, 0, 0, 0,  0, 0,  0,
        0, 0, 0, 0,  0,  0,  0, 0,  0,  0,  0,  0, 0,
        0, 0, 0,  0,  0, 0, 0, 0,  0,  0, 0,  0], [20, 0, -1, 0,  0,  0,  0, 0, 0, 0, 0,  0,  0,
        0,  0, 0, 0,  0, 0, 0, 0,  0, 0,  0, 0, 0,
        0,  0,  0, 0,  0,  0, 0, 0,  0,  0,  0, 0, 0,
        0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0,  0,  0,
        0, 0, 0, 0,  0, 0,  0,  0,  0, 0,  0, 0], [20,  1, -1, 0, -1, 0, 0,  0, 0, 0, 0,  0, 0,
       0,  0,  0,  0,  0, 0, 0, 0, 0,  0,  0,  0, 0,
        0,  0,  0, 0, 0, 0,  0,  0,  0, 0, 0,  0,  0,
        0, 0,  0, 0,  0,  0,  0,  0, 0, 0, 0,  0, 0,
       0,  0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0], [20,  0, -1,  0,  0,  0,  0,  0, 0, 0, 0,  0, 0,
       0, 0, 0,  0,  0, 0, 0, 0,  0,  0, 0, 0, 0,
        0, 0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0,
        0, 0,  0, 0,  0, 0, 0, 0, 0,  0,  0, 0,  0,
        0, 0,  0, 0,  0,  0,  0, 0,  0, 0, 0,  0], [20, -1, -1, 0, 0, 0,  0,  0,  0, 0, 0,  0, 0,
       0,  0, 0,  0,  0,  0, 0,  0, 0,  0,  0, 0, 0,
        0,  0,  0,  0,  0, 0,  0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0,  0, 0,  0, 0,  0,  0,  0, 0, 0,
       0,  0,  0, 0,  0,  0, 0, 0, 0, 0,  0, 0], [21, -1, -2, 0,  0, -1,  0,  0,  0,  0, 0, 0,  0,
       0, 0,  0,  0, 0,  0, 0, 0, 0,  0, 0,  0, 0,
       0,  0, 0,  0, 0, 0, 0, 0,  0, 0, 0,  0,  0,
        0,  0, 0, 0,  0, 0,  0, 0, 0, 0, 0,  0,  0,
        0, 0,  0,  0,  0,  0, 0, 0,  0, 0, 0, 0]
        , [21, 0, -2, 0,  0,  0, 0,  0,  0, 0, 0,  0,  0,
        0,  0, 0,  0,  0, 0, 0, 0, 0,  0, 0, 0, 0,
       0,  0, 0, 0, 0,  0,  0, 0,  0, 0,  0,  0, 0,
        0,  0, 0, 0, 0,  0,  0,  0,  0, 0,  0,  0, 0,
       0,  0, 0,  0,  0,  0, 0,  0,  0,  0,  0,  0], [21,  0, -1, -1, -1,  0, 0, 0,  0, 0, 0,  0,  0,
        0, 0, 0, 0,  0, 0,  0,  0, 0, 0,  0, 0, 0,
        0, 0,  0,  0, 0,  0,  0, 0, 0, 0,  0, 0,  0,
       0,  0, 0, 0, 0, 0, 0, 0, 0,  0, 0,  0, 0,
       0,  0, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0], [22, -1, -1, -1,  0,  0, 0,  0,  0, 0, 0, 0, 0,
        0,  0, 0, 0, 0, 0, 0, 0,  0,  0,  0,  0,  0,
       0, 0, 0,  0,  0,  0,  0,  0, 0, 0,  0,  0, 0,
       0, 0, 0,  0, 0, 0,  0,  0, 0,  0,  0, 0,  0,
        0, 0,  0,  0,  0, 0,  0, 0, 0,  0,  0,  0], [23,  0, 0, -2, 0, -1,  0,  0, 0,  0, 0,  0,  0,
        0,  0,  0, 0, 0, 0,  0, 0,  0, 0, 0, 0,  0,
       0, 0,  0, 0,  0, 0, 0,  0, 0, 0,  0, 0,  0,
        0,  0,  0, 0, 0,  0, 0, 0,  0,  0, 0,  0,  0,
        0, 0,  0, 0,  0,  0,  0,  0, 0, 0, 0,  0], [22,  0, 0, -1, 0, 0,  0,  0, 0, 0,  0, 0,  0,
        0,  0,  0, 0, 0, 0,  0, 0, 0, 0, 0,  0,  0,
        0,  0, 0,  0, 0, 0,  0,  0, 0, 0,  0,  0, 0,
       0, 0,  0,  0, 0,  0,  0,  0,  0, 0,  0, 0, 0,
        0, 0, 0, 0,  0, 0, 0, 0, 0,  0,  0,  0], [23, -2, -1,  0,  1, 0,  0, 0, 0, 0,  0, 0,  0,
       0, 0,  0,  0,  0,  0, 0, 0, 0,  0, 0, 0, 0,
       0, 0, 0,  0,  0, 0,  0,  0,  0,  0, 0, 0, 0,
       0,  0, 0, 0,  0,  0, 0,  0, 0,  0,  0, 0,  0,
        0,  0, 0,  0, 0,  0, 0,  0, 0, 0, 0,  0]]

hum = np.reshape(tst,(14,8,8))
# print(hum)
kool = [np.multiply(item,jpg) for item in hum]
x = [cv2.idct(blk) for blk in np.float32(kool)]
# print("Initial IDCT: \n")
# print(x)
secret_data = ""
for char in msg.encode('ascii'): secret_data += bitstring.pack('uint:8', char)
# embedded_dct_blocks   = stego.embed_encoded_data_into_DCT(secret_data, sorted_coefficients)
print(secret_data)



def embed_encoded_data_into_DCT(encoded_bits,dct_blocks):
    data_complete = False; encoded_bits.pos = 0
    encoded_data_len = bitstring.pack('uint:8', len(encoded_bits))
    converted_blocks = []
    t = []
    # print(len(encoded_data_len))
    print(np.array(dct_blocks).shape)
    for current_dct_block in dct_blocks:
        t = np.concatenate((fwht(current_dct_block[:4]),current_dct_block[4:]))
        for i in range(4):
            # print(t[i])
            curr_coeff = np.uint8(t[i])
            pack_coeff = bitstring.pack('uint:8', curr_coeff)
            if (encoded_data_len.pos <= len(encoded_data_len) - 1): pack_coeff[-1] = encoded_data_len.read(1)
            else: pack_coeff[-1] = encoded_bits.read(1)
            if (encoded_bits.pos == len(encoded_bits)): data_complete = True;
            # Replace converted coefficient
            print(pack_coeff,encoded_bits.pos)
            t[i] = np.float32(pack_coeff.read('uint:8'))
        converted_blocks.append(t)
    for blk in converted_blocks:
        blk[:4] = ifwht(np.float32(blk[:4]))
    if not(data_complete): raise ValueError("Data didn't fully embed into cover image!")
    print("Converted blocks shape: "+str(np.array(converted_blocks).shape))
    return converted_blocks


lum = np.reshape(embed_encoded_data_into_DCT(secret_data,tst),(14,8,8))
# print(hum)
pool = [np.multiply(item,jpg) for item in lum]
y = [cv2.idct(blk) for blk in np.float32(pool)]
# print("Second IDCT: \n")
# print(y)
def extract_encoded_data_from_DCT(blocks):
    extracted_data = ""
    for current in  blocks:
        # print(current)
        for bits in current:
            # print(round(bits))
            curr_coeff = round(bits)
            extracted_data += bitstring.pack('uint:1',  np.uint8(curr_coeff)&0x01)
    return extracted_data

dct_blocks = [cv2.dct(block) for block in y] 

dct_quants = [np.divide(item, jpg) for item in dct_blocks]
# print("dct quants: \n")
# print(dct_quants) 
reshaped = np.reshape(dct_quants,(14,64))
# sorted_coefficients = [zz.zigzag(block) for block in dct_quants]
hadamard = [fwht(blk[:4])for blk in reshaped]
# print(hadamard)
recovered_data = extract_encoded_data_from_DCT(hadamard)
print(recovered_data)
data_len = int(recovered_data.read('uint:8') / 8)

extracted_data = bytes()
for i in range(data_len): extracted_data += struct.pack('>B', recovered_data.read('uint:8'))

print(extracted_data.decode('ascii'))