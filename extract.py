import struct
import numpy as np
import start as src
import prep as p
import cv2
# from sympy import fwht
def extract_encoded_data_from_DCT(blocks):
    extracted_data = ""
    count = 0
    init_strg = ""
    myString = ""
    lenString = ""
    lame = 0
    for current in  blocks:
        if count%7 == 0 and count>0:
            count = 0
            if chr(int(init_strg,2)).isnumeric():
                lenString +=  chr(int(init_strg,2))
                init_strg = ""
            else:
                init_strg = ""
                skip = len(lenString)
                lenString = int(lenString)
                break
        count+=1
        init_strg += str(round(current[0])&1)
    
    char_count = 0
    to_skip = 0
    for current in blocks:
        if count%7 == 0 and count>0:
            count = 0
            if char_count==lenString: break
            if to_skip>=skip:
                myString +=  chr(int(init_strg,2))
                # print(myString)
                char_count += 1
            else:
                to_skip+=1
            init_strg = ""
        count+=1
        init_strg += str(round(current[0])&1)
    return myString

    

stego_image = cv2.imread(src.stego_image_loc, flags=cv2.IMREAD_COLOR)
stego_image_f32 = np.float32(stego_image)
height,width = stego_image_f32.shape[:2]
req_dim = height
if height>width: req_dim = width
converted = cv2.cvtColor(stego_image_f32, cv2.COLOR_BGR2YCrCb)
new_mat = [p.split_image(height,width,converted[:,:,0])]
dims = np.array(new_mat[0]).shape
dct_blocks = [[cv2.dct(block) for block in new_mat[0][i]] for i in range(int(req_dim/8))]
dct_quants = [[np.divide(item, p.QUANT_TABLE) for item in dct_blocks[i]] for i in range(int(req_dim/8))]
# print("DCT Quants:\n")
# print(dct_quants)
# print(np.array(dct_quants).shape)
reshaped = np.array(dct_quants).reshape(dims[0]*dims[1],dims[2]*dims[3])
# print(reshaped)
# print(hadamard)
# # s
# dct_quants = [np.divide(item, jpg) for item in dct_blocks]
# # print("dct quants: \n")
# # print(dct_quants) 
# reshaped = np.reshape(dct_quants,(14,64))
# # sorted_coefficients = [zz.zigzag(block) for block in dct_quants]
#
recovered_data = extract_encoded_data_from_DCT(reshaped)
print(recovered_data)
# data_len = int(recovered_data.read('uint:8')/8)
# # print(data_len)
# # print(recovered_data)
# extracted_data = bytes()
# for i in range(data_len): extracted_data += struct.pack('>B', recovered_data.read('uint:8'))

# print(extracted_data.decode('ascii'))