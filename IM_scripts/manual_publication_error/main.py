import time
import csv
from IM_scripts.manual_publication_error.IM_api import GetIMdata
from IM_scripts.auth.auth import GetAuth

'''функция запуска и перебора всех стадий инцидента'''
def start_handpub_error(token):

    stages = [3, 5, 6, 10]
    res_inc = []
    for stage in stages:
        time.sleep(2)
        res = unfinished_pub_get(stage, token)
        if res:
            res_inc.extend(res)
            res_inc.sort()
        break

    #записываем текстовый файл, где все исполнители по алфавитному порядку
    with open('ошибка публикации.txt', 'w', newline='', encoding='utf-8') as csvfile:

        writer = csv.writer(csvfile)

        for element in res_inc:
            writer.writerow([element])

    return res_inc

def unfinished_pub_get(stage, token):
    #авторизуемся и получаем токен

    get_data = GetIMdata()
    data = get_data.get_inc(token, stage)

    #собираем список с названиями испольнителей и ссылками на карточку инцидента

    all_inc = []
    for i in range(len(data['results'])):
        if data['results'][i]['last_response']["status"] == "UNFINISHED_PUBLICATION" or data['results'][i]['last_response']["status"] == "UNCONFIRMED_MANUAL_PUBLICATION":
            last_name = data['results'][i]["assigned_user_info"]["last_name"]
            first_name = data['results'][i]["assigned_user_info"]["first_name"]
            inc_id = data['results'][i]['id']
            link = f'https://im.gosuslugi.ru/#/incidents/stage/{stage}?incident={inc_id}'
            full_line = f'{last_name} {first_name}: {link}'
            all_inc.append(full_line)
        continue

    return all_inc







