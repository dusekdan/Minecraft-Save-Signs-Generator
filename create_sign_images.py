import json
import re
import unicodedata

from PIL import Image, ImageDraw, ImageFont

INPUT_SIGN_FILE = "./signs.json"

minecraft_font = ImageFont.truetype('./res/font.otf', size=20)
color = 'rgb(0,0,0)'

INCLUDED_CATEGORIES = ["nonempty"] # "empty", "nonempty", "plugin-related"

def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.

    Source: https://stackoverflow.com/a/31607735
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def adjust_for_centering(word):
    START_X_OFFSET = 8
    char_shift = 7
    chars_per_line = 15

    actual_length = len(word)
    if actual_length > chars_per_line:
        actual_length = 15

    left_offset = (chars_per_line - actual_length) * char_shift
    return START_X_OFFSET + left_offset

def generate_sign_image(sign_object, filename):
    """
    Uses extremely advanced mathematics (trial-and-error guess work) to position
    the text in the sign image to somewhat centered position.
    """
    LINE1_Y = 5
    LINE2_Y = 27
    LINE3_Y = 49
    LINE4_Y = 71
    
    image = Image.open('./res/sign.png')
    draw = ImageDraw.Draw(image)

    draw.text(
        (adjust_for_centering(sign_object["line1"]), LINE1_Y), 
        strip_accents(sign_object["line1"]), 
        fill=color, 
        font=minecraft_font
    )

    draw.text(
        (adjust_for_centering(sign_object["line2"]), LINE2_Y), 
        strip_accents(sign_object["line2"]), 
        fill=color, 
        font=minecraft_font
    )

    draw.text(
        (adjust_for_centering(sign_object["line3"]), LINE3_Y), 
        strip_accents(sign_object["line3"]), 
        fill=color, 
        font=minecraft_font
    )

    draw.text(
        (adjust_for_centering(sign_object["line4"]), LINE4_Y), 
        strip_accents(sign_object["line4"]), 
        fill=color, 
        font=minecraft_font
    )

    image.save(f'./{filename}')


with open(INPUT_SIGN_FILE, 'r') as f:
    data = json.load(f)

i = 0 
for sign in data:
    # TODO: Check category here.
    if sign["category"] in INCLUDED_CATEGORIES:
        generate_sign_image(sign, f"{i}.png")
        i += 1