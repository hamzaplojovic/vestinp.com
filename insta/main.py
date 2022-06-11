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

# TODO: implement a layer of black color with reduced opacity for contrast
def process_image(link, information):
    img_url = furl.furl(link).remove(args=True, fragment=True).url

    r = requests.get(img_url)

    try:
        im = Image.open(io.BytesIO(r.content))
    except:
        return None
    draw = ImageDraw.Draw(im)
    text = "Klikni za vise!"

    font = ImageFont.truetype("Roboto-Regular.ttf", 35)

    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    width, height = im.size

    textwidth, textheight = draw.textsize(text)
    x = (width - textwidth) / 2
    y = (height - textheight) / 2

    # draw.rectangle([(0, 0), im.size], fill=(0, 0, 0, 240))

    draw.text((x - 30, y), text, font=font, fill=(255, 0, 0), stroke_fill=(0, 0, 0), stroke_width=2)
    lines = textwrap.wrap(information, width=33)
    y_text = 15

    for line in lines:
        draw.text((width // 4, y_text), line, font=font, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2)
        y_text += 35
    # Setting the points for cropped image
    newsize = (1080, 1080)
    new_img = im.resize(newsize)
    # Shows the image in image viewer
    new_img.save('output.jpg')
    return 'output.jpg'


cl = Client()
cl.login(USERNAME, PASSWORD)


# process_image('https://rtvnp.rs/wp-content/uploads/2022/06/800x450-1-800x445.jpg', 'Postovani ovo je test vest za vas!')
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
