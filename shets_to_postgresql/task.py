import asyncio
from table import equality_check
from main import update_db
from convert import get_dollar_price
from notifiers import get_notifier
from config import token, telegram_id
from main import get_number_order


async def control_table():
    ''' Проверяет изменения в таблице,
     если они есть - вносит корректировку в db'''

    while equality_check():
        await asyncio.sleep(3)

    update_db()
    await control_table()


async def change_course():
    ''' Проверяет изменение курса,
    если курс изменился, переписывает данные в db'''

    res_1 = get_dollar_price(1)

    await asyncio.sleep(1 * 60)
    res_2 = get_dollar_price(1)

    if res_2 + 1 < res_1 or res_2 - 1 > res_1:
        update_db()

        await change_course()
    else:
        await change_course()


def generate_order():
    ''' Формирует просроченные заказы '''

    count_ = len(get_number_order())
    while count_ != 0:
        for x in get_number_order():
            string = ''
            string += str(x)
            yield string
            count_ -= 1


async def telegram_message():
    ''' Отправка уведомлений  telegram боту'''

    orders = generate_order()
    numbers_order = []
    for order in orders:
        numbers_order.append(order)

    if len(numbers_order) > 0:
        message = f'Список просроченных заказов : {numbers_order}'

        telegram = get_notifier('telegram')
        telegram.notify(token=token, chat_id=telegram_id, message=message)
    await asyncio.sleep(60*12)
    await telegram_message()


async def start():
    ''' Запускает задачи '''

    task1 = asyncio.create_task(control_table())
    task2 = asyncio.create_task(change_course())
    task3 = asyncio.create_task(telegram_message())
    await task1
    await task2
    await task3


asyncio.run(start())
