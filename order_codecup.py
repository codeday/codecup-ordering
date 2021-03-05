import gspread

import requests
from dotenv import load_dotenv
import os

load_dotenv()


def order_codecup(name, address1, city, state, zip, country, address2 = ''):
    codecup = {
    "type": "mug",
    "designId":"5f63b5f7f7e6355f5a68b56c",
    "products": [
        {
            "id": "beverage-mug",
            "color":"White",
            "size":"15oz",
            "quantity": 1
        }
    ],
    "address": {
        "name":name,
        "address1":address1,
        "address2":address2,
        "city":city,
        "state":state,
        "zip":zip,
        "country":country
    }
    }
    quote = requests.post('https://api.scalablepress.com/v2/quote', json=codecup, auth=('',os.getenv("TEST_key")))
    print(quote.text)
    order = requests.post('https://api.scalablepress.com/v2/order', json={'orderToken':quote.json()['orderToken']}, auth=('',os.getenv("TEST_key")))
    print(order.text)

order_codecup('Lola Egherman', '2925 Rutland Ave', 'Des Moines', 'Iowa', '50311', 'US')