import time
from rpi_ws281x import *
import argparse
import math

characters = {
    # --- UPPERCASE LETTERS ---
    "A": ["-*-", "*-*", "*-*", "*-*", "***", "*-*", "*-*", "*-*"],
    "B": ["**-", "*-*", "*-*", "*-*", "***", "*-*", "*-*", "**-"],
    "C": ["***", "*--", "*--", "*--", "*--", "*--", "*--", "***"],
    "D": ["**-", "*-*", "*-*", "*-*", "*-*", "*-*", "*-*", "**-"],
    "E": ["***", "*--", "*--", "***", "*--", "*--", "*--", "***"],
    "F": ["***", "*--", "*--", "***", "*--", "*--", "*--", "*--"],
    "G": ["***", "*-*", "*--", "***", "*-*", "*-*", "*-*", "***"],
    "H": ["*-*", "*-*", "*-*", "***", "*-*", "*-*", "*-*", "*-*"],
    "I": ["***", "-*-", "-*-", "-*-", "-*-", "-*-", "-*-", "***"],
    "J": ["--*", "--*", "--*", "--*", "--*", "*-*", "*-*", "-*-"],
    "K": ["*-*", "*-*", "*--", "**-", "**-", "*--", "*-*", "*-*"],
    "L": ["*--", "*--", "*--", "*--", "*--", "*--", "*--", "***"],
    "M": ["*-*", "***", "***", "*-*", "*-*", "*-*", "*-*", "*-*"],
    "N": ["*-*", "*-*", "**-", "**-", "*-*", "*-*", "*-*", "*-*"],
    "O": ["-*-", "*-*", "*-*", "*-*", "*-*", "*-*", "*-*", "-*-"],
    "P": ["**-", "*-*", "*-*", "**-", "*--", "*--", "*--", "*--"],
    "Q": ["-*-", "*-*", "*-*", "*-*", "*-*", "*-*", "*-*", "-**"],
    "R": ["**-", "*-*", "*-*", "**-", "**-", "*--", "*-*", "*-*"],
    "S": ["-**", "*-*", "*--", "-*-", "--*", "*-*", "*-*", "**-"],
    "T": ["***", "-*-", "-*-", "-*-", "-*-", "-*-", "-*-", "-*-"],
    "U": ["*-*", "*-*", "*-*", "*-*", "*-*", "*-*", "*-*", "***"],
    "V": ["*-*", "*-*", "*-*", "*-*", "*-*", "*-*", "-*-", "-*-"],
    "W": ["*-*", "*-*", "*-*", "*-*", "*-*", "***", "***", "*-*"],
    "X": ["*-*", "*-*", "*-*", "-*-", "-*-", "*-*", "*-*", "*-*"],
    "Y": ["*-*", "*-*", "*-*", "-*-", "-*-", "-*-", "-*-", "-*-"],
    "Z": ["***", "--*", "--*", "-*-", "-*-", "*--", "*--", "***"],

    # --- LOWERCASE LETTERS ---
    "a": ["---", "---", "-**", "--*", "-**", "*-*", "*-*", "-**"],
    "b": ["*--", "*--", "*--", "**-", "*-*", "*-*", "*-*", "**-"],
    "c": ["---", "---", "---", "-**", "*--", "*--", "*--", "-**"],
    "d": ["--*", "--*", "--*", "-**", "*-*", "*-*", "*-*", "-**"],
    "e": ["---", "---", "---", "-*-", "*-*", "***", "*--", "-**"],
    "f": ["--*", "-*-", "***", "-*-", "-*-", "-*-", "-*-", "-*-"],
    "g": ["---", "---", "-**", "*-*", "-**", "--*", "*-*", "-**"],
    "h": ["*--", "*--", "*--", "**-", "*-*", "*-*", "*-*", "*-*"],
    "i": ["-*-", "---", "-*-", "-*-", "-*-", "-*-", "-*-", "-*-"],
    "j": ["--*", "---", "--*", "--*", "--*", "--*", "*-*", "-*-"],
    "k": ["*--", "*--", "*--", "*-*", "**-", "**-", "*-*", "*-*"],
    "l": ["-*-", "-*-", "-*-", "-*-", "-*-", "-*-", "-*-", "-*-"],
    "m": ["---", "---", "---", "***", "***", "*-*", "*-*", "*-*"],
    "n": ["---", "---", "---", "**-", "*-*", "*-*", "*-*", "*-*"],
    "o": ["---", "---", "---", "-*-", "*-*", "*-*", "*-*", "-*-"],
    "p": ["---", "---", "**-", "*-*", "**-", "*--", "*--", "*--"],
    "q": ["---", "---", "-**", "*-*", "-**", "--*", "--*", "--*"],
    "r": ["---", "---", "---", "*--", "**-", "*--", "*--", "*--"],
    "s": ["---", "---", "---", "-**", "*--", "-*-", "--*", "**-"],
    "t": ["-*-", "-*-", "***", "-*-", "-*-", "-*-", "-*-", "--*"],
    "u": ["---", "---", "---", "*-*", "*-*", "*-*", "*-*", "-**"],
    "v": ["---", "---", "---", "*-*", "*-*", "*-*", "-*-", "-*-"],
    "w": ["---", "---", "---", "*-*", "*-*", "*-*", "***", "***"],
    "x": ["---", "---", "---", "*-*", "-*-", "-*-", "-*-", "*-*"],
    "y": ["---", "---", "*-*", "*-*", "-**", "--*", "*-*", "-**"],
    "z": ["---", "---", "---", "***", "--*", "-*-", "*--", "***"],

    # --- NUMBERS ---
    "0": ["-*-", "*-*", "*-*", "*-*", "*-*", "*-*", "*-*", "-*-"],
    "1": ["-*-", "**-", "-*-", "-*-", "-*-", "-*-", "-*-", "***"],
    "2": ["***", "--*", "--*", "-*-", "-*-", "*--", "*--", "***"],
    "3": ["***", "--*", "--*", "-**", "--*", "--*", "--*", "***"],
    "4": ["*-*", "*-*", "*-*", "***", "--*", "--*", "--*", "--*"],
    "5": ["***", "*--", "*--", "**-", "--*", "--*", "--*", "**-"],
    "6": ["-**", "*--", "*--", "**-", "*-*", "*-*", "*-*", "-*-"],
    "7": ["***", "--*", "--*", "-*-", "-*-", "-*-", "-*-", "-*-"],
    "8": ["-*-", "*-*", "*-*", "-*-", "*-*", "*-*", "*-*", "-*-"],
    "9": ["-*-", "*-*", "*-*", "-**", "--*", "--*", "--*", "**-"],
    " ": ["---", "---", "---", "---", "---", "---", "---", "---"]
}

codes = ["n"]

# LED strip configuration:
LED_COUNT      = 256      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 2    # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/500.0)

def letterToString(letter):
    # each letter is 24 pixels (8x3)
    # The led panel works in a snaking pattern, so the translations are a bit messy
    letterString = ""
    for i in range(1, 24 + 1):
        c = (math.floor(i / 8.01)) + 1 # column

        r = 0 # row
        if (i % 16 <= 8):
            r = (i % 16)
        else:
            r = 17 - (i % 16)
        
        if (r == 16 or r == 0):
            r = 1   
        
        # print("i: " + str(i) + " column: " + str(c) + " row: " + str(r))
        
        # if this spot in the letter is *, turn on the pixel, otherwise leave it off
        pixelOn = characters[letter][r - 1][c - 1] == "*"
        if(pixelOn):
            letterString += "1"
        else:
            letterString += "0"

    return letterString

def translateSentence(sentence):
    lines = []
    sentenceString = ""
    nextIsCode = False
    for letterIdx in range(len(sentence)): # for each letter
        letter = sentence[letterIdx]
        if letter == "/":
            nextIsCode = True

        elif nextIsCode:
            nextIsCode = False
            if letter in codes:
                if letter == "n":
                    lines.append(sentenceString)
                    sentenceString = ""
            else:
                print("Invalid code at letterIdx: " + str(letterIdx) + " letter: " + letter)

        elif letter in characters:
            letterString = letterToString(letter)
            letterString += "<------>"
            sentenceString += letterString

        else: 
            print("Invalid character at letterIdx: " + str(letterIdx) + " letter: " + letter)

    lines.append(sentenceString)
    return lines

def displayString(translatedString):
    for i in range(len(translatedString)):
        if translatedString[i] == "1":
            strip.setPixelColor(i, Color(255, 255, 255))
        else:
            strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def displaySentence(sentence, delay_ms=2000):
    lines = translateSentence(sentence)
    for i in range(len(lines)):
        displayString(lines[i])
        time.sleep(delay_ms/1000.0)

# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    displaySentence("Hello World", 2000)

    try:
        while True:
            continue

    except KeyboardInterrupt:
        colorWipe(strip, Color(0,0,0), 0)


