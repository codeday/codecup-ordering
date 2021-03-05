import gspread
import requests
from dotenv import load_dotenv
import os

load_dotenv()

gc = gspread.service_account('service-account.json')
sheet = gc.open('Codecup shipments')
worksheet = sheet.get_worksheet(0)
def order_codecup(name, address1, address2, city, state, zip, country):
    print(f'Ordering CodeCup to {name}')
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
        "name":str(name),
        "address1":str(address1),
        "address2":str(address2),
        "city":str(city),
        "state":str(state),
        "zip":str(zip),
        "country":str(country)
    }
    }
    quote = requests.post('https://api.scalablepress.com/v2/quote', json=codecup, auth=('',os.getenv("TEST_key")))
    print(f'Their CodeCup will cost {quote.json()["total"]}.. placing order')
    order = requests.post('https://api.scalablepress.com/v2/order', json={'orderToken':quote.json()['orderToken']}, auth=('',os.getenv("TEST_key")))
    if order.status_code == 200:
        print('Ordered!')
        return True
    else:
        print('Non-200 status code... outputting order response')
        print(order.text)
        return False

records = worksheet.get_all_records()


for record in records:
    if record['Status'] == 'pending':
        order_codecup(record['Name'], record['Addrline1'], record['Addrline2'], record['City'], record['State'], record['Zip'], record['Country'])
        row = worksheet.find(str(record['DiscordID'])).row
        worksheet.update_cell(row=row, col=9, value='order placed')