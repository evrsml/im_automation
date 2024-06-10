import pickle
import time
import csv
from IM_api import GetToken, GetIMdata
from VK_api import comment_link_parse

def token_keeper():
    get_token = GetToken("rbintern.03@gmail.com", "p3XpbBVi")
    token = get_token.get_token()
    with open('token.pickle', 'wb') as f:
        pickle.dump(token, f)

    ids_links_getter()

def ids_links_getter():
    with open('token.pickle', 'rb') as f:
        token = pickle.load(f)

    get_im = GetIMdata()

    data = get_im.get_inc_without_answers(token)

    inc_ids = []
    urls = []

    for i in range(len(data['results'])):
        id = data['results'][i]["id"]
        #print(id)
        url = data['results'][i]['source_post']['url']
        #print(url)
        if id not in inc_ids and url not in urls:
            inc_ids.append(id)
            urls.append(url)
        else:
            continue
    print('Количество инцидентов без ответа:', len(inc_ids))
    print('Поиск ответов в комментариях...')

    return selector(inc_ids, urls, token)

def selector(inc_ids, urls, token):
    url_report = []
    for url, id in zip(urls, inc_ids):
        data_answer = comment_link_parse(url)
        time.sleep(0.5)
        if data_answer is not None and data_answer[0] != '' and data_answer[1] != '':
            get_im = GetIMdata()
            get_im.get_inc(id, data_answer[0], data_answer[1], token)
            url_for_report = f'https://im.gosuslugi.ru/#/incidents/stage/3?incident={id}'
            url_report.append(url_for_report)
        continue
        #print('Пропускаем инц')

    print('Все ответы проведены!\nКоличество первичек проведено:', len(url_report))
    print(url_report)

    with open('отчет по первичным ответам.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write each element of the list as a new row in the CSV file
        for element in url_report:
            writer.writerow([element])


token_keeper()