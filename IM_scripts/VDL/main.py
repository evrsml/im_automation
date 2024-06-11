import time
from IM_scripts.VDL.IM_api import GetIMdata


inc_done = []

'''стартовый скрипт, просматривает три стадии инцидента'''
def start_vdl(token):

    stages = [3, 5, 10]

    for s in stages:
        inc_loop(s, token)

    total = sum(inc_done)
    return f"✅ Всего инцидентов обработано: {total}"


def inc_loop(stage, token):

    get_data = GetIMdata()
    data = get_data.get_inc(token, stage)

    if data:

        inc_done.append(int(len(data['results'])))

        for i in range(len(data['results'])):
            updated_data = {"source_post_id": 0, "report": 0, "location": 0, "category": 0,
                            "priority": 589,
                            "client_reference": [{"id": 6091, "title_id": 584}]}
            inc_id = data['results'][i]['id']
            url = f'https://im.gosuslugi.ru/api/inc/incidents/{inc_id}/'
            updated_data["source_post_id"] = data['results'][i]['source_post']['id']
            updated_data["report"] = data['results'][i]['report']
            updated_data["location"] = data['results'][i]['location']
            updated_data["category"] = data['results'][i]['category']
            number = data['results'][i]['number']
            time.sleep(0.5)
            get_data.update_inc(url, updated_data, token, number)



    


