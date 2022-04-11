# string = "BCAADDDCCACACAC"

class Node:

	def __init__(self,data,left = None, right = None):
		self.left = left
		self.right = right
		self.data = data


def huffManTree(string):
	codefreq = {}

	for chars in string:
		if chars in codefreq:
			codefreq[chars] += 1
		else:
			codefreq[chars] = 1

	myVals = list(codefreq.values())

	pQueue = [Node(myVals[i]) for i in range(len(myVals))]
	while len(pQueue)>1:
		pQueue.sort(key=lambda x:x.data)
		z = Node(data=None)
		sumz = pQueue[0].data+pQueue[1].data
		# print(pQueue[0].data,pQueue[1].data)
		z.left = pQueue[0]
		pQueue.pop(0)
		z.right = pQueue[0]
		pQueue.pop(0)
		z.data = sumz
		pQueue = [z]+pQueue
	return pQueue[0],codefreq


# myTree = huffManTree()[0]
huffman_dict = {}
huffman_dict1 = {}
def PreOrder(root,freq,s=''):
	# print(freq)
	if root.left == None and root.right == None:
		# print(str(root.data)+" : "+s)
		for key,val in freq.items():
			if root.data == val: 
				huffman_dict[s] = key
				huffman_dict1[key] = s
				del freq[key]
				break
		# huffman_dict[list(freq.keys())[list(freq.values()).index(root.data)]] = s
		return
	# print(root.data)
	PreOrder(root.left,freq,s+'0')
	PreOrder(root.right,freq,s+'1')
	return huffman_dict,huffman_dict1
# code_dict = PreOrder(myTree)
# print(code_dict)

