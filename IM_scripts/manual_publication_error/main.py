import pickle
import pprint
import time
import csv
from IM_scripts.manual_publication_error.IM_api import GetToken, GetIMdata

def token_keeper():
    get_token = GetToken("rbintern.03@gmail.com", "p3XpbBVi")
    token = get_token.get_token()
    with open('token.pickle', 'wb') as f:
        pickle.dump(token, f)

    stages = [3, 5, 6, 10]
    res_inc = []
    for stage in stages:
        time.sleep(2)
        res = unfinished_pub_get(stage)
        res_inc.extend(res)
    res_inc.sort()

    #print('Завершил все стадии')
    #pprint.pprint(res_inc)

    with open('ошибка публикации.txt', 'w', newline='', encoding='utf-8') as csvfile:

        writer = csv.writer(csvfile)

        for element in res_inc:
            writer.writerow([element])

    return res_inc


def unfinished_pub_get(stage):
    with open('token.pickle', 'rb') as f:
        token = pickle.load(f)

    get_data = GetIMdata()
    data = get_data.get_inc(token, stage)

    all_inc = []
    for i in range(len(data['results'])):
        if data['results'][i]['last_response']["status"] == "UNFINISHED_PUBLICATION":
            last_name = data['results'][i]["assigned_user_info"]["last_name"]
            first_name = data['results'][i]["assigned_user_info"]["first_name"]
            inc_id = data['results'][i]['id']
            link = f'https://im.gosuslugi.ru/#/incidents/stage/{stage}?incident={inc_id}'
            full_line = f'{last_name} {first_name}: {link}'
            all_inc.append(full_line)
        continue

    return all_inc



