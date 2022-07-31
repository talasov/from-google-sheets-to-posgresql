import requests
from bs4 import BeautifulSoup
from config import dollar_url, headers


def get_dollar_price(rub):
    ''' Курс доллара по ЦБ РФ'''

    full_page = requests.get(dollar_url, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll('div', {'class': 'col-md-2 col-xs-9 _right mono-num'})

    dollar_price = float(convert[1].text[:5].replace(',', '.'))
    return dollar_price * rub




