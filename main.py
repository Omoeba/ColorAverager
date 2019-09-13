import numpy
import pyperclip
import shutil
from colored import fg, bg, attr
#import colorsys

ts = shutil.get_terminal_size()

#RESET = '\033[0m'


#def get_color_escape(r, g, b, background=False):
#    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)


helpInfo = (
    "info: inputs and outputs are all in hex (ex. #ffffff), type \"quit\" anywhere to exit. Leave the colors blank to read from clipboard. Type \"help\" to show this again.")
lineSeparater = ("━" * ts.columns)
endIndex = helpInfo.rindex(" ", 0, len(helpInfo))
i = 1
userInput = ""
loopAmount = ""
#errorColor = bg('yellow') + fg('white')
reset = attr('reset')
invalidAmount = 'Invalid amount of colors to calculate'
invalidHex = ('Invalid color hex code')
while True:
    if userInput == "quit":
        break
    if loopAmount == "quit":
        break
    lineIndex = helpInfo.rindex(" ", 0, (ts.columns * i))
    helpInfo = list(helpInfo)
    helpInfo[lineIndex] = '\n'
    helpInfo = "".join(helpInfo)
    if lineIndex == endIndex:
        break
    i = i + 1
print(helpInfo)
while True:
    if userInput == "quit":
        break
    if loopAmount == "quit":
        break
    print(lineSeparater)
    while True:
        loopAmount = input("How many colors do you want to calculate: ")
        if loopAmount == "quit":
            break
        if loopAmount == "help":
            print(lineSeparater)
            print(helpInfo)
            print(lineSeparater)
            continue
        else:
            try:
                loopAmount = int(loopAmount)
                i = 0
            except:
                print(invalidAmount)
                continue
            break
    while True:
        if loopAmount == "quit":
            break
        userInput = input('Color 1: ').lstrip('#')
        if userInput == "quit":
            break
        if userInput == "help":
            print(lineSeparater)
            print(helpInfo)
            print(lineSeparater)
            continue
        if userInput == "":
            userInput = pyperclip.paste().lstrip('#')
            print(userInput + " was pasted from clipboard")
        try:
            colorList = list(int(userInput[i:i + 2], 16) for i in (0, 2, 4))
            break
        except:
            print(invalidHex)
            continue
    if (loopAmount != "quit") and (userInput != "quit"):
        while i < (loopAmount - 1):
            userInput = input("Color" + " " + str(i + 2) + ": ").lstrip('#')
            if userInput == "quit":
                break
            if userInput == "help":
                print(lineSeparater)
                print(helpInfo)
                print(lineSeparater)
            if userInput == "":
                userInput = pyperclip.paste().lstrip('#')
                print(userInput + " was pasted from clipboard")
            try:
                userList = list(int(userInput[i:i + 2], 16) for i in (0, 2, 4))
            except:
                print(invalidHex)
                continue
            colorList = (numpy.array(colorList) + numpy.array(userList))
            i = i + 1
        else:
            colorList = (numpy.array(colorList) / float(loopAmount))
            colorList = [round(x) for x in colorList]
            colorList = [int(x) for x in colorList]
            result = '#%02x%02x%02x' % tuple(colorList)
          #   colorBrightness = list(colorsys.rgb_to_hsv(colorList[0], colorList[1], colorList[2]))
          # if colorBrightness[2] >= 127.5:
          #       foregroundList = [0, 0, 0]
          #   else:
          #       foregroundList = [255, 255, 255]
            pyperclip.copy(result)
 #           print(get_color_escape(foregroundList[0], foregroundList[1], foregroundList[2], True) + get_color_escape(colorList[0], colorList[1], colorList[2], False) + result + " has been copied to your clipboard" + RESET)
            print(result + " has been copied to your clipboard!")
