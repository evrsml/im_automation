import requests
import json

'''класс для получения токена для запросов к ИМ'''


'''класс для запросов к ИМ'''
class GetIMdata():

    def get_inc(self, token, stage):

        base_url = f'https://im.gosuslugi.ru/api/inc/incidents/?offset=0&limit=10&ordering=-current_stage_term&current_stage={stage}&personal=64452&workflow=322'
        response = requests.get(base_url, headers=token)
        data = json.loads(response.text)
        print(data)
        inc_count = data['count']
        #print(inc_count)
        current_url = f'https://im.gosuslugi.ru/api/inc/incidents/?offset=0&limit={inc_count}&ordering=-current_stage_term&current_stage={stage}&personal=64452&workflow=322'
        response = requests.get(current_url, headers=token)
        data = json.loads(response.text)
        #print(data)
        return data

