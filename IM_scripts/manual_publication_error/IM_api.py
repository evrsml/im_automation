import requests
import json


'''класс для запросов к ИМ'''
class GetIMdata():

    '''получаем json со всеми инцидентами, где есть ошибка публикации'''
    def get_inc(self, token, stage):

        try:
            base_url = f'https://im.gosuslugi.ru/api/inc/incidents/?offset=0&limit=10&ordering=-current_stage_term&current_stage={stage}&personal=64452&workflow=322'
            response = requests.get(base_url, headers=token)
            data = json.loads(response.text)
            inc_count = data['count']
            current_url = f'https://im.gosuslugi.ru/api/inc/incidents/?offset=0&limit={inc_count}&ordering=-current_stage_term&current_stage={stage}&personal=64452&workflow=322'
            response = requests.get(current_url, headers=token)
            data = json.loads(response.text)
            return data

        except KeyError:
            return data



