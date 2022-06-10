import io
import requests
import textwrap

from base64 import decode
from base64 import encode

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from instagrapi import Client
from instagrapi.types import StoryBuild
from instagrapi.types import StoryLink
from instagrapi.types import StoryMention
from pathlib import Path

from bs4 import BeautifulSoup
from numpy.core.arrayprint import IntegerFormat

USERNAME = 'vesti_np'
PASSWORD = 'Ba%qNQ5z^X!D@$73'


def process_image(link, information):
    r = requests.get(link)

    try:
        im = Image.open(io.BytesIO(r.content))
    except:
        return None
    draw = ImageDraw.Draw(im)
    text = "Klikni za vise!"

    font = ImageFont.truetype("arial.ttf", 30)

    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    width, height = im.size

    textwidth, textheight = draw.textsize(text)
    x = (width - textwidth) / 2
    y = (height - textheight) / 2

    draw.text((x, y), text, font=font, fill=(255, 0, 0))
    lines = textwrap.wrap(information, width=33)
    y_text = 15

    for line in lines:
        draw.text((width//4, y_text), line, font=font, fill=(255, 0, 0))
        y_text += 35
    # Setting the points for cropped image
    newsize = (1080, 1080)
    new_img = im.resize(newsize)
    # Shows the image in image viewer
    new_img.save('output.jpg')
    return 'output.jpg'


cl = Client()
cl.login(USERNAME, PASSWORD)


response = requests.get('https://api.vestinp.com/data/today/top/').json()
for article in response:

    try:
        cl.photo_upload_to_story(
            Path(process_image(article['img'], BeautifulSoup(article['title'], 'lxml').get_text())),
            links=[StoryLink(webUri=article['url'])]
        )
    except:
        pass
print('Finished!')
