from PIL import Image

def getLength(message):
    if len(message) == 0:
        print("Message has no contents")
        exit()
    return len(message) * 8

def encodeLength(fileName, length):
    im = Image.open(fileName)
    im = im.rotate(180)
    pix = im.load()
    width, height = im.size
    print("WIDTH: ", width, "HEIGHT: ", height)
    # convert message length into binary string
    if (length//3) > (width*height):
        print("Message too large to fit image")
        exit()
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

def getMessage(fileName):
    # TEST read as binary file
    with open(fileName, 'r') as file:
        fileContents = file.read()
        return fileContents

def getbitString(character):
    bitString = bin(int.from_bytes(character.encode(), 'big'))
    bitString = bitString[2:]
    while(len(bitString) != 8):
        bitString = '0' + bitString
    # pad with leading zeros
    return bitString


def encodeMessage(fileName, message):
    length = getLength(message)
    message_length_mod = length % 3
    length //= 3
    im = Image.open(fileName)
    im = im.rotate(180)
    pix = im.load()
    width, height = im.size
    # convert message length into binary string
    message_counter = 0
    string_index = 0
    x_value = 0
    y_value = 0

    # get starting x and y value
    for x in range(11):
        if x_value > (width - 1):
            x_value = 0
            y_value += 1
        x_value += 1
    bitString = getbitString(message[message_counter])
    message_counter += 1
    # starting at the 12th pixel
    for x in range(1, length + 1):
        if x_value > (width - 1):
            x_value = 0
            y_value += 1
        r, g, b = pix[x_value, y_value]
        # if the value at an RGB is 1 but we want to flip
        if string_index >= 8:
            string_index = 0
            bitString = ''
            bitString = getbitString(message[message_counter])
            message_counter += 1
        if r & 1 == 1 and bitString[string_index] == '0':
            r = r ^ 1
        elif r & 1 == 0 and bitString[string_index] == '1':
            r = r ^ 1
        string_index += 1
        if string_index >= 8:
            string_index = 0
            bitString = ''
            bitString = getbitString(message[message_counter])
            message_counter += 1
        if g & 1 == 1 and bitString[string_index] == '0':
            g = g ^ 1
        elif g & 1 == 0 and bitString[string_index] == '1':
            g = g ^ 1
        string_index += 1
        if string_index >= 8:
            string_index = 0
            bitString = ''
            bitString = getbitString(message[message_counter])
            message_counter += 1
        if b & 1 == 1 and bitString[string_index] == '0':
            b = b ^ 1
        elif b & 1 == 0 and bitString[string_index] == '1':
            b = b ^ 1
        string_index += 1
        pix[x_value, y_value] = (r, g, b)
        x_value += 1

    # mod message length
    if message_length_mod == 1:
        # could possibly be the edge pixel on the right
        if x_value == (width - 1):
            x_value = 0
            y_value += 1
        r, g, b = pix[x_value, y_value]
        if r & 1 == 1 and bitString[string_index] == '0':
            r = r ^ 1
        elif r & 1 == 0 and bitString[string_index] == '1':
            r = r ^ 1
        pix[x_value, y_value] = (r, g, b)
    elif message_length_mod == 2:
        if x_value == (width - 1):
            x_value = 0
            y_value += 1
        r, g, b = pix[x_value, y_value]
        if r & 1 == 1 and bitString[string_index] == '0':
            r = r ^ 1
        elif r & 1 == 0 and bitString[string_index] == '1':
            r = r ^ 1
        string_index += 1
        if g & 1 == 1 and bitString[string_index] == '0':
            g = g ^ 1
        elif g & 1 == 0 and bitString[string_index] == '1':
            g = g ^ 1
        pix[x_value, y_value] = (r, g, b)
    im = im.rotate(180)
    im.save(fileName, "PNG")

def encode(imageFileName, inputFileName):
    # get some input MESSAGE and save as message
    message = getMessage(inputFileName)
    message_length = getLength(message)
    encodeLength(imageFileName, message_length)
    encodeMessage(imageFileName, message)

# main
encode("testimage.PNG", "input.txt")
