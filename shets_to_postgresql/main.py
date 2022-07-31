from config import CREDINTIAL_FILE, scope
from config import host, dbname, password, user
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import psycopg2
from itertools import islice
from table import create_table

''' connect bd '''
connect = psycopg2.connect(
    database=dbname,
    user=user,
    host=host,
    password=password
)
cursor = connect.cursor()


def get_table(title):
    ''' Получает данные из google sheets '''

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDINTIAL_FILE, scope)
    client = gspread.authorize(credentials)
    sheet = client.open(title).sheet1
    return sheet


def clear_db():
    ''' Очищает db для перезаписи данных '''

    cursor.execute('TRUNCATE google_sheets;')
    connect.commit()


def get_number_order():
    ''' Получаем номера просроченных заказов из db '''

    lst = []
    db_request = 'SELECT заказ_№ FROM google_sheets WHERE срок_поставки < CURRENT_DATE; '
    cursor.execute(db_request)
    numbers = cursor.fetchall()

    for number in numbers:
        for item in number:
            lst.append(item)
    return lst


def update_db():
    ''' Добавляет данные в db из google sheets '''

    clear_db()

    create_table()

    iterable_results = iter(get_table("Retail_Transactions2").get_all_values())
    next(iterable_results)

    for i, value in islice(enumerate(iterable_results), None, None):
        if not value[0]:
            continue
        number = value[0]
        order = "" if not value[1] else value[1]
        price_in_dollars = "" if not value[2] else value[2]
        date = "" if not value[3] else value[3]
        price_in_rub = "" if not value[4] else value[4]

        query = (
            "INSERT INTO google_sheets (№, заказ_№, стоимость$, срок_поставки, стоимость₽)"
            "VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(query, (
            number, order, price_in_dollars, date, price_in_rub))
        connect.commit()
