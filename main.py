import numpy
import pyperclip
import shutil
# from colored import fg, bg, attr
import colorsys
from threading import Thread



invalidAmount = 'Invalid number'
invalidHex = 'Invalid color hex code'
noResult = 'No colors calculated'

# RESET = '\033[0m'

def termsize():
    while True:
        global ts
        ts = shutil.get_terminal_size()
        global lineSeparater
        lineSeparater = ("━" * ts.columns)


# def get_color_escape(r, g, b, background=False):
#    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

cmyk_scale = 100


def rgb_to_cmyk(r, g, b):
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / 255.
    m = 1 - g / 255.
    y = 1 - b / 255.

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c * cmyk_scale, m * cmyk_scale, y * cmyk_scale, k * cmyk_scale

def masterHelpPrinter():
    i = 1
    masterHelp = "Type \"refresh\" at any input to show it again, this might be useful when you change the window size. Type \"quit\" to exit the program. Type \"help\" to show this again (help will also refresh inputs). "
    endIndex = masterHelp.rindex(" ", 0, len(masterHelp))
    while True:
        lineIndex = masterHelp.rindex(" ", 0, (ts.columns * i))
        masterHelp = list(masterHelp)
        if lineIndex == endIndex:
            break
        else:
            masterHelp[lineIndex] = '\n'
            masterHelp = "".join(masterHelp)
        i = i + 1
    masterHelp = list(masterHelp)
    masterHelp.pop()
    masterHelp = "".join(masterHelp)
    return masterHelp


def helpPrinter():
    i = 1
    helpInfo = "Inputs and outputs are all in hex (ex. #ffffff), type \"quit\" to return to mode selection. Leave the colors blank to read from clipboard. Special values \"lum\" and \"br\" can be used the get the luminosity and brownness of the previous result. Type \"help\" to show this again. "
    endIndex = helpInfo.rindex(" ", 0, len(helpInfo))
    while True:
        lineIndex = helpInfo.rindex(" ", 0, (ts.columns * i))
        helpInfo = list(helpInfo)
        if lineIndex == endIndex:
            break
        else:
            helpInfo[lineIndex] = '\n'
            helpInfo = "".join(helpInfo)
        i = i + 1
    helpInfo = list(helpInfo)
    helpInfo.pop()
    helpInfo = "".join(helpInfo)
    print(helpInfo)


def promptPrinter():
    i = 1
    prompt = "Do you want to calculate the average of multiple colors (type \"1\"), get the brightness of one color (type \"2\") or get the brownness of one color (type \"3\")\n:  "
    endIndex = prompt.rindex(" ", 0, len(prompt))
    while True:
        lineIndex = prompt.rindex(" ", 0, (ts.columns * i))
        prompt = list(prompt)
        if lineIndex == endIndex:
            break
        else:
            prompt[lineIndex] = '\n'
            prompt = "".join(prompt)
        i = i + 1
    prompt = list(prompt)
    prompt.pop()
    prompt = "".join(prompt)
    return prompt

def lumHelpPrinter():
    i = 1
    lumHelp = "Inputs are in hex, outputs are integers from 0 to 255. Type \"quit\" to return to mode selection. Type \"help\" to show this again. "
    endIndex = lumHelp.rindex(" ", 0, len(lumHelp))
    while True:
        lineIndex = lumHelp.rindex(" ", 0, (ts.columns * i))
        lumHelp = list(lumHelp)
        if lineIndex == endIndex:
            break
        else:
            lumHelp[lineIndex] = '\n'
            lumHelp = "".join(lumHelp)
        i = i + 1
    lumHelp = list(lumHelp)
    lumHelp.pop()
    lumHelp = "".join(lumHelp)
    return lumHelp

def brownHelpPrinter():
    i = 1
    brown = "Brownness is measured in CBU, which stands for Composite Brownness Units. A color's CBU is calculated using its yellow content and brightness. Type \"quit\" to return to mode selection. Type \"help\" to show this again. "
    endIndex = brown.rindex(" ", 0, len(brown))
    while True:
        lineIndex = brown.rindex(" ", 0, (ts.columns * i))
        brown = list(brown)
        if lineIndex == endIndex:
            break
        else:
            brown[lineIndex] = '\n'
            brown = "".join(brown)
        i = i + 1
    brown = list(brown)
    brown.pop()
    brown = "".join(brown)
    return brown



def ColorAverager():
    userInput = ""
    loopAmount = ""
    # errorColor = bg('yellow') + fg('white')
    # reset = attr('reset')
    print(lineSeparater)
    helpPrinter()
    while True:
        if userInput == "quit":
            break
        if loopAmount == "quit":
            break
        while True:
            print(lineSeparater)
            loopAmount = input("How many colors do you want to calculate: ")
            if loopAmount == "quit":
                break
            elif loopAmount == "lum":
                try:
                    lum = luminenceCalculator((result.lstrip("#")), True)
                    pyperclip.copy((str(lum)))
                    print(lineSeparater)
                    print("Brightness: " + str(lum))
                    continue
                except:
                    print(lineSeparater)
                    print(noResult)
                    continue
            elif loopAmount == "br":
                try:
                    br = brownessCalculator(colorList[0], colorList[1], colorList[2], result.lstrip("#"))
                    pyperclip.copy((str(br)))
                    print(lineSeparater)
                    print("Brownness: " + str(br))
                    continue
                except:
                    print(lineSeparater)
                    print(noResult)
                    continue
            elif loopAmount == "help":
                print(lineSeparater)
                helpPrinter()
                continue
            elif loopAmount == "refresh":
                continue
            else:
                try:
                    loopAmount = int(loopAmount)
                    i = 0
                except:
                    print(lineSeparater)
                    print(invalidAmount)
                    continue
                break
        while True:
            if loopAmount == "quit":
                break
            print(lineSeparater)
            userInput = input('Color 1: ').lstrip('#')
            if userInput == "quit":
                break
            elif userInput == "help":
                print(lineSeparater)
                helpPrinter()
                continue
            elif userInput == "lum":
                try:
                    lum = luminenceCalculator((result.lstrip("#")), True)
                    pyperclip.copy((str(lum)))
                    print(lineSeparater)
                    print("Brightness: " + str(lum))
                    continue
                except:
                    print(lineSeparater)
                    print(noResult)
                    continue
            elif userInput == "br":
                try:
                    br = brownessCalculator(colorList[0], colorList[1], colorList[2], result.lstrip("#"))
                    pyperclip.copy((str(br)))
                    print(lineSeparater)
                    print("Brownness: " + str(br))
                    continue
                except:
                    print(lineSeparater)
                    print(noResult)
                    continue
            elif userInput == "":
                print(userInput + " was pasted from clipboard")
                userInput = pyperclip.paste().lstrip('#')
            elif userInput == "refresh":
                continue
            try:
                colorList = list(int(userInput[i:i + 2], 16) for i in (0, 2, 4))
                break
            except:
                print(lineSeparater)
                print(invalidHex)
                continue
        if (loopAmount != "quit") and (userInput != "quit"):
            while i < (loopAmount - 1):
                print(lineSeparater)
                userInput = input("Color" + " " + str(i + 2) + ": ").lstrip('#')
                if userInput == "quit":
                    break
                elif userInput == "help":
                    print(lineSeparater)
                    helpPrinter()
                    continue
                elif userInput == "lum":
                    try:
                        lum = luminenceCalculator((result.lstrip("#")), True)
                        pyperclip.copy((str(lum)))
                        print(lineSeparater)
                        print("Brightness: " + str(lum))
                        continue
                    except:
                        print(lineSeparater)
                        print(noResult)
                        continue
                elif userInput == "br":
                    try:
                        br = brownessCalculator(colorList[0], colorList[1], colorList[2], result.lstrip("#"))
                        pyperclip.copy((str(br)))
                        print(lineSeparater)
                        print("Brownness: " + str(br))
                        continue
                    except:
                        print(lineSeparater)
                        print(noResult)
                        continue
                elif userInput == "":
                    print(userInput + " was pasted from clipboard")
                    userInput = pyperclip.paste().lstrip('#')
                elif userInput == "refresh":
                    continue
                try:
                    userList = list(int(userInput[i:i + 2], 16) for i in (0, 2, 4))
                except:
                    print(lineSeparater)
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
                print(lineSeparater)
                print(result + " has been copied to your clipboard!")



def luminenceCalculator(stubInput, stub=False):
    if stub == False:
        print(lineSeparater)
        print(lumHelpPrinter())
        while True:
            print(lineSeparater)
            userInput = input("Color: ").lstrip("#")
            if userInput == "quit":
                break
            elif userInput == "help":
                print(lineSeparater)
                print(lumHelpPrinter())
                continue
            elif userInput == "":
                print(lineSeparater)
                print(userInput + " was pasted from clipboard")
                userInput = pyperclip.paste().lstrip('#')
            elif userInput == "refresh":
                continue
            try:
                userList = list(int(userInput[i:i + 2], 16) for i in (0, 2, 4))
                brightnessList = list(colorsys.rgb_to_hls(userList[0], userList[1], userList[2]))
                brightness = str(int(round(brightnessList[1])))
                pyperclip.copy(brightness)
                print("Brightness is: " + brightness)
                continue
            except:
                print(lineSeparater)
                print(invalidHex)
                continue
    if stub == True:
        userList = list(int(stubInput[i:i + 2], 16) for i in (0, 2, 4))
        brightnessList = list(colorsys.rgb_to_hls(userList[0], userList[1], userList[2]))
        brightness = str(int(round(brightnessList[1])))
        return(int(brightness))


def brownessCalculator(color1, color2, color3, hex, interactive = False):
    if interactive == True:
        print(lineSeparater)
        print(brownHelpPrinter())
        while True:
            print(lineSeparater)
            userInput = input("Color: ").lstrip("#")
            if userInput == "quit":
                break
            elif userInput == "help":
                print(lineSeparater)
                print(brownHelpPrinter())
                continue
            elif userInput == "":
                print(lineSeparater)
                print(userInput + " was pasted from clipboard")
                userInput = pyperclip.paste().lstrip('#')
            elif userInput == "refresh":
                continue
            try:
                userList = list(int(userInput[i:i + 2], 16) for i in (0, 2, 4))
                yellow = int(round(list(rgb_to_cmyk(userList[0], userList[1], userList[2]))[2]))
                luminence = int(round(((abs(luminenceCalculator(userInput, True) - 255)) / 255) * 100))
                print(str(yellow * luminence) + " CBU")
                continue
            except:
                print(lineSeparater)
                print(invalidHex)
                continue
    else:
        yellow = int(round(list(rgb_to_cmyk(color1, color2, color3))[2]))
        luminence = int(round(((abs(luminenceCalculator(hex, True) - 255)) / 255) * 100))
        return yellow * luminence


def main():
    print(lineSeparater)
    print(masterHelpPrinter())
    while True:
        print(lineSeparater)
        mode = input(promptPrinter())
        if mode == "quit":
            break
        elif mode == "2":
            luminenceCalculator(0)
        elif mode == "1":
            ColorAverager()
        elif mode == "3":
            brownessCalculator(0, 0, 0, 0, True)
        elif mode == "help":
            print(lineSeparater)
            print(masterHelpPrinter())
        elif mode == "refresh":
            continue
        else:
            print(lineSeparater)
            print(invalidAmount)
            continue

t1 = Thread(target=termsize)
t1.daemon = True
t2 = Thread(target=main)
t1.start()
t2.start()
