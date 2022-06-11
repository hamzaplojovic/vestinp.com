#!/usr/bin/python3
import furl
import io
import requests
import textwrap

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from instagrapi import Client
from instagrapi.types import StoryLink
from pathlib import Path

from bs4 import BeautifulSoup

USERNAME = 'vesti_np'
PASSWORD = 'Ba%qNQ5z^X!D@$73'

FONT1 = ImageFont.truetype("insta/Roboto-Regular.ttf", size=20)
FONT2 = ImageFont.truetype("insta/Roboto-Regular.ttf", size=30)

# TODO: implement a layer of black color with reduced opacity for contrast


def process_image(link, text):
    # request image
    img_url = furl.furl(link).remove(args=True, fragment=True).url
    r = requests.get(img_url)

    # load image
    try:
        im = Image.open(io.BytesIO(r.content))
    except Exception as e:
        print(e)
        return None
    # draw over image
    img = draw(im, text)

    # save image
    size = (1080, 1080)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save('output.jpg')
    return 'output.jpg'


def draw(img, text):

    draw = ImageDraw.Draw(img)
    click = "Klikni za više!"

    width, height = img.size

    textwidth, textheight = draw.textsize(click, font=FONT1)
    x = width - textwidth - 36
    y = height - textheight -  36

    draw.rectangle((x+textwidth + 4, y+textheight+4, x-4, y), fill=(255, 255, 255, 5),outline='black')
    draw.text((x, y), click, font=FONT1, align='center', fill=(255, 0, 0), stroke_fill=(0, 0, 0), stroke_width=1)  # , font=FONT,
    lines = textwrap.wrap(text, width=33)

    y_new = 36
    textwidth, textheight = draw.textsize(lines[0], font=FONT2)
    x = (width - textwidth) / 8
    for line in lines:
        draw.text((x, y_new), line, font=FONT2, stroke_width=1, stroke_fill=(0, 0, 0), align='center')
        y_new += 36


    return img


process_image('https://rtvnp.rs/wp-content/uploads/2022/06/800x450-1-800x445.jpg', 'U ovom tekstu ima jako puno dugackog texta nije vise ko pre ')
# r = requests.get('https://rtvnp.rs/wp-content/uploads/2022/06/800x450-1-800x445.jpg')
# img_bytes = io.BytesIO(r.content)
# task(img_bytes)
