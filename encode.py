from PIL import Image

#######################################################
# gets the legth of the message in bits
# @param message - the message to encode
# @return - the length of the message in bits
#######################################################
def getLength(message):

    # check if the message is empty
    if len(message) == 0:
        print("Message has no contents")
        exit()

    return len(message) * 8


############################################################
# encodes the length of the message on the first 11 pixels
# @param imageFileName - the path to the image file
# @param length - the length of the message
# @return - none
############################################################
def encodeLength(imageFileName, length):
    # open the image and rotate 180 degrees
    # convert to 'RGB' for compatability
    im = Image.open(imageFileName).convert('RGB')
    im = im.rotate(180)
    pix = im.load()
    width, height = im.size
    print("WIDTH: ", width, "HEIGHT: ", height)

    # convert message length into binary string and check for
    # extremely large messages that won't fit the image
    if (length//3) > (width*height):
        print("Message too large to fit image")
        exit()
    print("Length of the message in bits: ", length)

    # convert the length to a binary string of 32 bits
    length_string = '{0:032b}'.format(length)
    string_index = 0
    x_value = 0
    y_value = 0

    # loop through the first 10 pixels
    for x in range(10):

        # check for edge of image and increment y if needed
        if x_value > (width - 1):
            x_value = 0
            y_value += 1

        r, g, b = pix[x_value, y_value]

        # check if the least sig bit of R is what we want
        # if NOT then R = flip the least sig bit
        if (r & 1) != int(length_string[string_index]):
            r = r ^ 1
        string_index += 1

        # same but for G
        if (g & 1) != int(length_string[string_index]):
            g = g ^ 1
        string_index += 1

        # same but for B
        if (b & 1) != int(length_string[string_index]):
            b = b ^ 1
        string_index += 1

        # write the correct RGB value at the right position
        pix[x_value, y_value] = (r, g, b)
        x_value += 1

    # 11th pixel which ignores b value
    if x_value > (width - 1):
        x_value = 0
        y_value += 1

    r, g, b = pix[x_value, y_value]

    # same process as above but for ONLY r and g
    if (r & 1) != int(length_string[string_index]):
        r = r ^ 1
    string_index += 1
    if (g & 1) != int(length_string[string_index]):
        g = g ^ 1
    string_index += 1
    pix[x_value, y_value] = (r, g, b)

    # revert the image to it's original orientation
    im = im.rotate(180)
    im.save(imageFileName, "PNG")


#######################################################
# loads the message from an input file
# @param inputFileName - path to the input file
# @return - contents of the file as a string
#######################################################
def getMessage(inputFileName):
    # TEST read as binary file
    with open(inputFileName, 'r') as file:
        fileContents = file.read()
        return fileContents


########################################################################
# converts a character to an 8 bit binary string
# @param character - signle character
# @return - 8 bit binary string corresponding to the right character
########################################################################
def getbitString(character):
    bitString = bin(int.from_bytes(character.encode(), 'big'))

    # remove '0b' from the string
    bitString = bitString[2:]

    # pad with leading zeros
    while(len(bitString) != 8):
        bitString = '0' + bitString

    return bitString


#######################################################
# encodes the message onto the image
# @param imageFileName - path to the input file
# @param message - the message to encode
# @return - none
#######################################################
def encodeMessage(imageFileName, message):
    # get length and convert to amount of pixels
    # mod handles uneven situations
    length = getLength(message)
    message_length_mod = length % 3
    length //= 3

    # open image and rotate 180 degrees
    im = Image.open(imageFileName)
    im = im.rotate(180)
    pix = im.load()
    width, height = im.size

    # message_counter indexes which character
    # is currently being written
    message_counter = 0
    string_index = 0
    x_value = 0
    y_value = 0

    # loop through first 11 pixels to get starting x and y value
    for x in range(11):
        # check for possible edge pixel
        if x_value > (width - 1):
            x_value = 0
            y_value += 1
        x_value += 1

    # convert character at message_counter to 8 bit binary string
    bitString = getbitString(message[message_counter])
    message_counter += 1

    # starting at the 12th pixel
    for x in range(1, length + 1):
        if x_value > (width - 1):
            x_value = 0
            y_value += 1

        r, g, b = pix[x_value, y_value]

        # check if a full 8 bit string has been written
        # then reset values and get the next 8 bits
        if string_index >= 8:
            string_index = 0
            bitString = ''
            bitString = getbitString(message[message_counter])
            message_counter += 1

        # check if the least sig bit of R is what we want
        # if NOT then R = flip the least sig bit
        if (r & 1) != int(bitString[string_index]):
            r = r ^ 1
        string_index += 1

        if string_index >= 8:
            string_index = 0
            bitString = ''
            bitString = getbitString(message[message_counter])
            message_counter += 1

        # same for G
        if (g & 1) != int(bitString[string_index]):
            g = g ^ 1
        string_index += 1

        if string_index >= 8:
            string_index = 0
            bitString = ''
            bitString = getbitString(message[message_counter])
            message_counter += 1

        # same for B
        if (b & 1) != int(bitString[string_index]):
            b = b ^ 1
        string_index += 1

        # write R G B values and continue to next pixel
        pix[x_value, y_value] = (r, g, b)
        x_value += 1

    # check for uneven cases
    if message_length_mod == 1:
        # check for edge pixel
        if x_value > (width - 1):
            x_value = 0
            y_value += 1
        r, g, b = pix[x_value, y_value]

        # check if the least sig bit of R is what we want
        if (r & 1) != int(bitString[string_index]):
            r = r ^ 1
        pix[x_value, y_value] = (r, g, b)

    elif message_length_mod == 2:
        # check for edge pixel
        if x_value > (width - 1):
            x_value = 0
            y_value += 1
        r, g, b = pix[x_value, y_value]

        # check if least sig bit of R is what we want
        if (r & 1) != int(bitString[string_index]):
            r = r ^ 1
        string_index += 1

        # same for G
        if (g & 1) != int(bitString[string_index]):
            g = g ^ 1
        pix[x_value, y_value] = (r, g, b)

    # revert the image to it's original orientation
    im = im.rotate(180)
    im.save(imageFileName, "PNG")


# main
if __name__ == '__main__':
    message = getMessage("input.txt")
    message_length = getLength(message)
    encodeLength("testimage.PNG", message_length)
    encodeMessage("testimage.PNG", message)
