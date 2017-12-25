import sqlite3
import time
import vk_api

vk = vk_api.VkApi(token='1c1941ce7895fc6c6dbd0da1890c3e06d5689cc7b5d5e7af2546d6da2327179fe956a5baa2f1f2f131691')
vk._auth_token()

def send_message(user_id, s):
    vk.method('messages.send', {'user_id':user_id, 'message':s})

values = {'out': 0,'count':100, 'time_offset':60}
vk.method('messages.get', values)
days = ('понедельник', 'вторник', 'среда', 'четверг', 'пятница')
notdays = ('суббота', 'воскресенье')
hello = """
        &#127794; &#127794; &#127794;
        Хо-хо-хо! Привет, меня называют Толстым Фермером. \n
        Я живу в селе Молочное и иногда, когда студенты заблуждаются в моих землях,
        я показываю им дорогу до корпуса или до аудитории. \n
        Пока я только нахожусь в тестовом режиме и мне доступны не все знания, но 
        я стараюсь быстро учиться. На данный момент я умею подсказывать только предметы
        в один из дней недели и только 633 группе (и только на второй неделе). Просто отправь мне день недели, в который хочешь узнать расписание занятий \n
        Например: среда

"""

while True:
    resp = vk.method('messages.get', values)
    if resp['items']:
        values['last_message_id'] = resp['items'][0]['id']
    for item in resp['items']:
        if item['body'].lower() in days:
            conn = sqlite3.connect('vk.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT lesson,prepod,aud FROM Moloko WHERE date='{}'".format(item['body'].title()))
            results = cursor.fetchall()
            print(results)
            if len(results) == 3:
                msg = str(results[0][0]) + '\n' + str(results[1][0]) + '\n' + str(results[2][0])
            elif len(results) == 2:
                msg = str(results[0][0]) + '\n' + str(results[1][0])
            elif len(results) == 4:
                msg = str(results[0][0]) + '\n' + str(results[1][0]) + str(results[2][0]) + str(results[3][0])
            send_message(item[u'user_id'], msg)
            conn.close()
        elif item['body'].lower() in notdays:
            send_message(item[u'user_id'], 'Ты явно хотел пошутить надо мной! Все знают, что в эти дни студенты не учатся, а пьют!')
        elif item['body'].lower() == 'привет':
             send_message(item[u'user_id'], hello)
        else:
            send_message(item[u'user_id'],u'не работает')
    time.sleep(1)