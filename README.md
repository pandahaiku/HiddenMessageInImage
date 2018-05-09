# HiddenMessageInImage
hiding messages in the least significant bits of RGB values in pixels

Requirements:
1. Python 3 must be installed
2. Image and input text file must be in the same directory as the python scripts
3. Input file must be named "input.txt"
4. Image file must be named "testImage.png"

Instructions:

Encoding message into image:
1. run python encode.py

Decoding message from image:
1. run python decode.py

Notes:
1. the message contents of decode.py will be outputted to "output.txt"
2. When encoding, the image file will be saved as a PNG file to avoid data loss
3. Non UTF-8 characters will not be recognized and cause the program to hang
