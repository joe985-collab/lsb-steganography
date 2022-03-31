import pickle
import numpy as np
import prep as p
import sys
import cv2
import bitstring
np.set_printoptions(threshold=sys.maxsize)

myObjects = open("encoded1.txt","rb")
emp = pickle.load(myObjects)
retrieved_data = emp[2].split(" ")
retrieved_dict = emp[1]
print(retrieved_dict)
print(retrieved_data)
del retrieved_data[-1]
ycbcr = np.empty((816,832,3),dtype=float)
# for i in range(len(retrieved_data)):
# 	retrieved_data[i] = retrieved_dict[retrieved_data[i]]
# myArray = np.float32(np.array(retrieved_data))
# idct_mat = myArray.reshape((3,102,104,8,8))
# for i in range(3):
# 	print(idct_mat[i])
# 	idct_mat[i] = np.multiply(idct_mat[i],p.QUANT_TABLE)
# 	for t in range(102):
# 		for l in range(104):
# 			idct_mat[i][t][l] = cv2.idct(np.float32(idct_mat[i][t][l]))
	# print(idct_mat[i].shape)
	# flat = idct_mat[i].reshape(816,832)
	# ycbcr[:,:,i] = flat

# image_BGR = cv2.cvtColor(np.float32(ycbcr), cv2.COLOR_YCR_CB2BGR)

# # Clamp Pixel Values to [0 - 255]
# final_image = np.uint8(np.clip(image_BGR, 0, 255))
# print(final_image)

# # Write stego image
# cv2.imwrite("./decoded.png", final_image)
# def Prez(root):
# 	# print(freq)
# 	if root.left == None and root.right == None:
# 		print(root.data)
# 		return
# 	# print(root.data)
# 	Prez(root.left)
# 	Prez(root.right)
# Prez(retrieved_tree)