# Douglas Galm




# HiddenMessageInImage


hiding messages in the least significant bits of RGB values in pixels

# Requirements:
1. Python 3 must be installed
2. Image and input text file must be in the same directory as the python scripts

# Instructions:

Encoding message into image:
1. run python encode.py <IMAGE FILE NAME> <INPUT FILE NAME>
2. where: <IMAGE FILE NAME> = name of the image to manipulate
          <INPUT FILE NAME> = name of the file with the message contents
                    
    Example: $python encode.py testimage.PNG input.txt

Decoding message from image:
1. run python decode.py <IMAGE FILE NAME>
2. where: <IMAGE FILE NAME> = name of the image to decode
   
    Example: $python decode.py testimage.PNG

# Notes:
1. the message contents of decode.py will be outputted to "output.txt"
2. When encoding, the image file will be saved as a PNG file to avoid data loss
3. Non UTF-8 characters will not be recognized and cause the program to hang

# Architecture:
For both encoding and decoding, I found it was easier to rotate the image 180
degrees and iterate through the image from left to right, top to bottom; yielding
the same result. Then, it simply reads/writes RGB value's least significant bits
and uses bitwise operations to change those values. I also accounted for certain
edge cases like there being no message, or a message that was too big to fit the
image. 

