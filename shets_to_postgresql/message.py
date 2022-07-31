from notifiers import get_notifier
import time
from config import token, telegram_id
from main import get_number_order


# while True:
#     what = input('о чём напомнить?\n')
#     if what == 'exit':
#         break
#
#     else:
#         t = input('через сколько?\n')
#         t = int(t) * 60
#         time.sleep(t)


def generator():
    count1 = len(get_number_order())
    while count1 != 0:
        for x in get_number_order():
            string = ''
            string += str(x)
            yield string
            count1 -= 1



s = generator()

m = []
for x in s:
    m.append(x)
i = f'Список просроченных заказов : {m}'
telegram = get_notifier('telegram')
telegram.notify(token=token, chat_id=telegram_id, message=i)

