import os

from deta import Deta

deta = Deta(os.environ['DETA_PROJECT_KEY'])

db = deta.Base('items')


all_items = db.fetch().items

print(all_items)
# keys = [x['key'] for x in all_items]

# for key in keys:
#     db.delete(key)

