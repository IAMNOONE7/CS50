import sys
import os
from PIL import Image, ImageOps

VALIDIMAGES = {".jpg", ".jpeg", ".png"}

def main():
    if len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    elif len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")

    in_file = sys.argv[1]
    out_file = sys.argv[2]

    in_img = os.path.splitext(in_file)[1].lower()
    out_img= os.path.splitext(out_file)[1].lower()

    if in_img not in VALIDIMAGES or out_img not in VALIDIMAGES:
        sys.exit("Invalid input")

    if in_img != out_img:
        sys.exit("Input and output have different extensions")


    with Image.open(in_file) as _image:
        shirt = Image.open("shirt.png")
        _fit = ImageOps.fit(_image, shirt.size)
        _fit.paste(shirt, shirt)
        _fit.save(out_file)



main()
