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
del retrieved_data[-1]
dim_1 = emp[3][0]
dim_2 = emp[3][1]
ycbcr = np.empty((dim_1,dim_2,3),dtype=float)
for i in range(len(retrieved_data)):
	retrieved_data[i] = retrieved_dict[retrieved_data[i]]
myArray = np.array(np.float32(retrieved_data))
idct_mat = myArray.reshape((3,int(dim_1/8),int(dim_2/8),8,8))
myMat = np.array([])
for i in range(3):
	idct_mat[i] = np.multiply(idct_mat[i],p.QUANT_TABLE)
	for t in range(int(dim_1/8)):
		for l in range(int(dim_2/8)):
			idct_mat[i][t][l] = cv2.idct(np.float32(idct_mat[i][t][l]))
		myMat = np.append(myMat,list(map(list, zip(*idct_mat[i][t]))))
	myMat = myMat.reshape(dim_1,dim_2)
	ycbcr[:,:,i] = myMat
	myMat = np.array([])
# print(ycbcr)
	# myMat = np.array(myMat).ravel()
image_BGR = cv2.cvtColor(np.float32(ycbcr), cv2.COLOR_YCR_CB2BGR)

# Clamp Pixel Values to [0 - 255]
final_image = np.uint8(np.clip(image_BGR, 0, 255))
# print(final_image)

# # Write stego image
cv2.imwrite("./decoders.png", final_image)
# def Prez(root):
# 	# print(freq)
# 	if root.left == None and root.right == None:
# 		print(root.data)
# 		return
# 	# print(root.data)
# 	Prez(root.left)
# 	Prez(root.right)
# Prez(retrieved_tree)