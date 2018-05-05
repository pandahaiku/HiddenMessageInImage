from PIL import Image

def getLength(message):
    return len(message) * 8

def encodeLength(fileName, length):
    im = Image.open(fileName)
    im = im.rotate(180)
    pix = im.load()
    width, height = im.size
    print("WIDTH: ", width, "HEIGHT: ", height)
    # convert message length into binary string
    print("Length of the message in bits: ", length)
    length_string = '{0:032b}'.format(length)
    string_index = 0
    x_value = 0
    y_value = 0
    for x in range(10):
        if x_value > (width - 1):
            x_value = 0
            y_value += 1
        r, g, b = pix[x_value, y_value]
        # if the value at an RGB is 1 but we want to flip
        if r & 1 == 1 and length_string[string_index] == '0':
            r = r ^ 1
        elif r & 1 == 0 and length_string[string_index] == '1':
            r = r ^ 1
        string_index += 1
        if g & 1 == 1 and length_string[string_index] == '0':
            g = g ^ 1
        elif g & 1 == 0 and length_string[string_index] == '1':
            g = g ^ 1
        string_index += 1
        if b & 1 == 1 and length_string[string_index] == '0':
            b = b ^ 1
        elif b & 1 == 0 and length_string[string_index] == '1':
            b = b ^ 1
        string_index += 1
        pix[x_value, y_value] = (r, g, b)
        x_value += 1
    # 11th pixel which ignores b value
    r, g, b = pix[x_value, y_value]
    if r & 1 == 1 and length_string[string_index] == '0':
        r = r ^ 1
    string_index += 1
    if g & 1 == 1 and length_string[string_index] == '0':
        g = g ^ 1
    string_index += 1
    pix[x_value, y_value] = (r, g, b)

    im = im.rotate(180)
    im.save(fileName, "PNG")

def encodeMessage(fileName, message, length):
    im = Image.open(fileName)
    im = im.rotate(180)
    pix = im.load()
    width, height = im.size
    print("WIDTH: ", width, "HEIGHT: ", height)
    # convert message length into binary string
    string_index = 0
    x_value = 0
    y_value = 0
    for x in range(length):
        # convert character to 8 bit binary

        if x_value > (width - 1):
            x_value = 0
            y_value += 1
        r, g, b = pix[x_value, y_value]
        # if the value at an RGB is 1 but we want to flip
        if r & 1 == 1 and length_string[string_index] == '0':
            r = r ^ 1
        string_index += 1
        if g & 1 == 1 and length_string[string_index] == '0':
            g = g ^ 1
        string_index += 1
        if b & 1 == 1 and length_string[string_index] == '0':
            b = b ^ 1
        string_index += 1
        pix[x_value, y_value] = (r, g, b)
        x_value += 1

def encode(fileName):
    # get some input MESSAGE and save as message
    # message_length = getLength('security is funs')
    encodeLength(fileName, 96)
    # message = getMessage(fileName)
    # encodeMessage(fileName, message, message_length)

# main
encode("testimage.PNG")
