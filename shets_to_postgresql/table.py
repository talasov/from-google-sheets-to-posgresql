import httplib2
import apiclient
from config import scope, CREDINTIAL_FILE, spreadsheet_id, spreadsheet_id2
from oauth2client.service_account import ServiceAccountCredentials
from convert import get_dollar_price


def find_table(cred_file=CREDINTIAL_FILE):
    ''' Подключается к таблице google '''

    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    return service


def take_data(range_='A1:D1000', spreadsheet_id=spreadsheet_id):
    ''' Извлекает данные из таблицы '''

    value = find_table().spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_,
        majorDimension='COLUMNS'
    ).execute()
    return value.get('values')


def take_column():
    ''' Создаёт колонку <Стоимость,₽> '''

    heading = ['Стоимость,₽']
    usd_column = [float(item) for item in take_data()[2][1:]]

    price_in_rub = [int(get_dollar_price(item)) for item in usd_column]

    return heading + price_in_rub


def clear_table():
    ''' Очистищаешь данные из google sheets '''

    value = find_table().spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id2,
        range='A1:Z1000'
    ).execute()


def create_table():
    ''' Создаёт копию таблицы с новой колонкой <Стоимость,₽> '''

    clear_table()

    column_a, column_b, column_c, column_d = take_data()
    column_e = take_column()

    value = find_table().spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id2,
        body={
            'valueInputOption': 'RAW',
            'data': [
                {'range': 'A1:A1000',
                 'majorDimension': 'COLUMNS',
                 'values': [column_a]},
                {'range': 'B1:B1000',
                 'majorDimension': 'COLUMNS',
                 'values': [column_b]},
                {'range': 'C1:C1000',
                 'majorDimension': 'COLUMNS',
                 'values': [column_c]},
                {'range': 'D1:D1000',
                 'majorDimension': 'COLUMNS',
                 'values': [column_d]},
                {'range': 'E1:E1000',
                 'majorDimension': 'COLUMNS',
                 'values': [column_e]}
            ]
        }
    ).execute()
    return value


def equality_check():
    ''' Проверяет изменения в таблице'''

    return take_data() == take_data(spreadsheet_id=spreadsheet_id2)
