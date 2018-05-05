from PIL import Image

# returns the length of the strings
def getLength(im):
    pix = im.load()
    width, height = im.size
    length_string = ""
    x_value = 0
    y_value = 0
    for x in range(10):
        if x_value > (width - 1):
            x_value = 0
            y_value += 1
        r, g, b = pix[x_value, y_value]
        r = r & 1
        g = g & 1
        b = b & 1
        length_string += str(r)
        length_string += str(g)
        length_string += str(b)
        x_value += 1
    # exclude B in 11th pixel
    r, g, b = pix[x_value, y_value]
    r = r & 1
    g = g & 1
    length_string += str(r)
    length_string += str(g)
    # returns the length of the string as an integer
    length_string = int(length_string, base = 2)
    print("Length of message in bits: ", length_string)
    return length_string


# returns the decoded message
def decode(fileName):
    # open image file
    im = Image.open(fileName)
    rotateim = im.rotate(180)
    pix = rotateim.load()
    width, height = rotateim.size
    print("WIDTH: ", width, "HEIGHT: ", height)
    message_length = getLength(rotateim)
    message_string = ""
    message_length_mod = message_length % 3
    # convert message_length into number of pixels
    message_length //= 3
    y_value = 0
    x_value = 0
    for x in range(message_length + 11):
        if x_value > (width - 1):
            x_value = 0
            y_value += 1
        r, g, b = pix[x_value, y_value]
        r = r & 1
        g = g & 1
        b = b & 1
        if x > 10:
            message_string += str(r)
            message_string += str(g)
            message_string += str(b)
        x_value += 1

    # check if extra characters need to be accounted for
    if message_length_mod == 1:
        # could possibly be the edge pixel on the right
        if x_value == (width - 1):
            x_value = 0
            y_value += 1
        r, g, b = pix[x_value, y_value]
        r = r & 1
        message_string += str(r)
    elif message_length_mod == 2:
        if x_value == (width - 1):
            x_value = 0
            y_value += 1
        r, g, b = pix[x_value, y_value]
        r, g, b = pix[x_value, y_value]
        r = r & 1
        g = g & 1
        message_string += str(r)
        message_string += str(g)

    message_byte = ""
    for x in range(len(message_string)):
        if x % 8 == 0 and x != 0:
            message_byte = int(message_byte, base=2)
            print(chr(message_byte), end='')
            message_byte = ""
        message_byte += message_string[x]
    # print final character
    message_byte = int(message_byte, base=2)
    print(chr(message_byte), end='')

# main
decode("testimage.PNG")
