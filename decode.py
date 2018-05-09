from PIL import Image
import sys

##################################################
# Returns the legnth of the message
# @param im - python pillow image file
# @return - integer lenght of message in bits
##################################################
def getLength(im):

    # load the image and initialize variables
    # Image will already be rotated 180 degrees
    pix = im.load()
    width, height = im.size
    length_string = ""

    # x and y value are the coordinates of the pixels
    x_value = 0
    y_value = 0

    # loop through first 10 pixels
    for x in range(10):

        # check for edge of image and increment y if needed
        if x_value > (width - 1):
            x_value = 0
            y_value += 1

        # set r, g, b to be the least significant bit
        r, g, b = pix[x_value, y_value]
        r = r & 1
        g = g & 1
        b = b & 1
        length_string += str(r)
        length_string += str(g)
        length_string += str(b)
        x_value += 1

    # exclude B in 11th pixel
    if x_value > (width - 1):
        x_value = 0
        y_value += 1
    r, g, b = pix[x_value, y_value]
    r = r & 1
    g = g & 1
    length_string += str(r)
    length_string += str(g)

    # convert binary string to integer
    length_string = int(length_string, base = 2)
    print("Length of message in bits: ", length_string)

    # handle error if message does not exist
    if length_string == 0:
        print("Message length is zero")
        exit()

    return length_string


###########################################################################
# Writes the contents of the message to a file
# @param message - the decoded message
# @param outputFileName - the path to the output file to write the message
# @return - none
###########################################################################
def writeToFile(message, outputFileName):
    with open(outputFileName, 'w') as file:

        # read message_string byte by byte and convert each byte
        # to a character, then write each character to a file
        message_byte = ""
        for x in range(len(message)):

            # check if a full byte has been loaded
            if x % 8 == 0 and x != 0:

                # converts the 8 bit string to an binary integer
                message_byte = int(message_byte, base=2)
                file.write((chr(message_byte)))
                message_byte = ""

            # keep adding characters until a byte is filled
            message_byte += message[x]

        # print final character
        message_byte = int(message_byte, base=2)
        file.write((chr(message_byte)))
        print("Decoded message written to: ", outputFileName)


#######################################################
# gets the contents of the message
# @param imageFileName - the path to the image file
# @return - decoded message
#######################################################
def decode(imageFileName):
        # open image and rotate 180 degrees
        im = Image.open(imageFileName)
        rotateim = im.rotate(180)
        pix = rotateim.load()

        # message_length_mod handles uneven situations
        # where we might not need the G or B pixels
        width, height = rotateim.size
        print("WIDTH: ", width, "HEIGHT: ", height)
        message_length = getLength(rotateim)
        message_string = ""
        message_length_mod = message_length % 3

        # convert message_length into number of pixels
        message_length //= 3
        y_value = 0
        x_value = 0

        # loop through message length and message
        for x in range(message_length + 11):
            if x_value > (width - 1):
                x_value = 0
                y_value += 1
            r, g, b = pix[x_value, y_value]
            r = r & 1
            g = g & 1
            b = b & 1

            # only start adding to the message when the
            # 12th pixel has been encountered
            if x > 10:
                message_string += str(r)
                message_string += str(g)
                message_string += str(b)
            x_value += 1

        # check if extra characters need to be accounted for
        if message_length_mod == 1:

            # check for the edge pixel
            if x_value > (width - 1):
                x_value = 0
                y_value += 1

            # account ONLY for r
            r, g, b = pix[x_value, y_value]
            r = r & 1
            message_string += str(r)

        # chekc if extra characters need to be accounted for
        elif message_length_mod == 2:

            # check for the edge pixel
            if x_value > (width - 1):
                x_value = 0
                y_value += 1

            # account for r and g but NOT b
            r, g, b = pix[x_value, y_value]
            r = r & 1
            g = g & 1
            message_string += str(r)
            message_string += str(g)

        return message_string

# main
def main():

    # make sure that all the arguments have been provided
    if len(sys.argv) < 2:
        print("USAGE: " + sys.argv[0] + "<IMAGE FILE NAME>")
        exit(-1)

    # The image file
    imageFileName = sys.argv[1]

    # decode message from the image file
    decodedMessage = decode(imageFileName)

    # write the decoded message to output.txt
    writeToFile(decodedMessage, "output.txt")

### Call the main function ###
if __name__ == "__main__":
	main()
