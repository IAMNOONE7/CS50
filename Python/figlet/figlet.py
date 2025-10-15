from pyfiglet import Figlet
import sys
import random

def main():
    figlet = Figlet()
    fonts = figlet.getFonts()

    if len(sys.argv) == 1:
        random_font = random.choice(fonts)
        figlet.setFont(font = random_font)


    elif len(sys.argv) == 3 and sys.argv[1] in ["-f", "--font"]:
        if sys.argv[2] not in fonts:
            sys.exit("Invalid Font Name")

        figlet.setFont(font = sys.argv[2])

    else:
        sys.exit("Invalid usage")

    text = input("Input: ")
    print(figlet.renderText(text))


main()
