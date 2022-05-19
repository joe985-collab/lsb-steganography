# lsb-steganography
This is inspired by from the project by Mason Edgar. link: https://github.com/MasonEdgar/DCT-Image-Steganography
I have instead used DC coefficients of all channels for lsb substitution. Also added encoder and decoder code to roughly demonstrate the encoding and decoding process.

# To use the program
1. Open start.py in an editor and specify the cover image location, stego image location and the message within the strings.
2. Execute start.py. Stego Image will be generated.
3. Execute extract.py to recover the secret message.
