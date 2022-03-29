import bitstring
import numpy as np
from sympy import fwht,ifwht
def embed_encoded_data_into_DCT(encoded_bits,dct_blocks):
    dim = np.array(dct_blocks).shape
    dct_blocks = np.array(dct_blocks).reshape(dim[0]*dim[1],dim[2]*dim[3])
    data_complete = False; encoded_bits.pos = 0
    encoded_data_len = bitstring.pack('uint:8', len(encoded_bits))
    # print(encoded_data_len)
    converted_blocks = []
    t = []
    # print(len(encoded_data_len))
    for current_dct_block in dct_blocks:
        t = np.concatenate((fwht(current_dct_block[:4]),current_dct_block[4:]))
        if not data_complete:
            for i in range(4):
                # print(t[i])
                curr_coeff = np.uint8(t[i])
                pack_coeff = bitstring.pack('uint:8', curr_coeff)
                if (encoded_data_len.pos <= len(encoded_data_len) - 1): pack_coeff[-1] = encoded_data_len.read(1)
                else: pack_coeff[-1] = encoded_bits.read(1)
                if (encoded_bits.pos == len(encoded_bits)): data_complete = True;
                # Replace converted coefficient
                # print(pack_coeff,encoded_bits.pos)
                t[i] = np.float32(pack_coeff.read('uint:8'))
            converted_blocks.append(t)
        else:
            converted_blocks.append(t)
    for blk in converted_blocks:
        blk[:4] = ifwht(np.float32(blk[:4]))
    if not(data_complete): raise ValueError("Data didn't fully embed into cover image!")
    converted_blocks = np.array(converted_blocks).reshape(dim[0],dim[1],dim[2],dim[3])
    # print("Converted blocks:\n")
    # print(converted_blocks)
    return converted_blocks