import numpy as np
import start as src
import prep as p
import cv2
from timeit import default_timer as timer
start = timer()
# from sympy import fwht
def extract_encoded_data_from_DCT(blocks):
    extracted_data = ""
    count = 0
    init_strg = ""
    myString = ""
    lenString = ""
    lame = 0
    # Store length of message in lenString
    for current in  blocks:
        # print(current[0])
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
        init_strg += str(int(current[0])&1)
        # print(init_strg,current[0])
    # print(lenString)
    char_count = 0
    to_skip = 0
    # Store the actual message in myString
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
# print(stego_image)
# print(stego_image)
# stego_image_f32 = np.float32(stego_image)
stego_image_f32 = stego_image
# print(cv2.subtract(stego_image,src.final_stego_image))
height,width = stego_image_f32.shape[:2]
# req_dim = height
# if height>width: req_dim = width
# not_req_dim = width
# if height>width: 
#     req_dim = width
#     not_req_dim = height
converted = cv2.cvtColor(np.float32(stego_image_f32), cv2.COLOR_BGR2YCrCb)
# print(converted)
# converted = src.stego_image_float
new_mat = [p.split_image(height,width,converted[:,:,0]),p.split_image(height,width,converted[:,:,1]),p.split_image(height,width,converted[:,:,2])]
req_dim = np.array(new_mat).shape[1]
# print(np.array(new_mat[0]).shape)
dims = np.array(new_mat[0]).shape
# print(dims)
dct_blocks = [[cv2.dct(block) for block in new_mat[0][i]] for i in range(req_dim)]
# while(np.block(new_mat[0]).shape != np.block(dct_blocks).shape):
#         # print(np.block(dct_blocks).shape)
#         req_dim = not_req_dim
#         dct_blocks = [[cv2.dct(x) for x in new_mat[0][i]] for i in range(int(req_dim/8))]
quantized = [[np.around(np.divide(x,p.QUANT_TABLE)) for x in dct_blocks[i]] for i in range(req_dim)]
reshaped = np.array(quantized).reshape(dims[0]*dims[1],dims[2]*dims[3])

recovered_data = extract_encoded_data_from_DCT(reshaped)
print(recovered_data)
# end = timer()
# print(end - start)