import numpy as np
# from sympy import fwht,ifwht
def embed_encoded_data_into_DCT(encoded_bits,dct_blocks):
    dim = np.array(dct_blocks).shape
    dct_blocks = np.array(dct_blocks).reshape(dim[0]*dim[1],dim[2]*dim[3])
    # print(encoded_data_len)
    converted_blocks = []
    l = 0
    # print(len(encoded_data_len))
    for current_dct_block in dct_blocks:
        if l<len(encoded_bits):
            current_dct_block[0] = int(current_dct_block[0]) & ~1|int(encoded_bits[l])
            l += 1
        converted_blocks.append(current_dct_block)
    # if not(data_complete): raise ValueError("Data didn't fully embed into cover image!")
    converted_blocks = np.array(converted_blocks).reshape(dim[0],dim[1],dim[2],dim[3])
    # print("Converted blocks:\n")
    # print(converted_blocks)
    return converted_blocks