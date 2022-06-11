import furl
import io
import requests

from PIL import Image


response = requests.get('https://api.vestinp.com/data').json()


for article in response:
	img_url = furl.furl(article['img']).remove(args=True, fragment=True).url
	r = requests.get(img_url)
	try:
		img_bytes = io.BytesIO(r.content)
		im = Image.open(img_bytes)
	except Exception as e:
		print(e)
		print(img_url)
		# print(r.content)
