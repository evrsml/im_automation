import requests
import json

'''класс для запросов к ИМ'''
class GetIMdata():

        def get_inc(self, token, stage):

            base_url = f'https://im.gosuslugi.ru/api/inc/incidents/?offset=0&limit=10&ordering=-current_stage_term&current_stage={stage}&personal=100737&workflow=322'
            response = requests.get(base_url, headers=token)
            data = json.loads(response.text)
            inc_count = data['count']
            current_url = f'https://im.gosuslugi.ru/api/inc/incidents/?offset=0&limit={inc_count}&ordering=-current_stage_term&current_stage={stage}&personal=100737&workflow=322'
            response = requests.get(current_url, headers=token)
            data = json.loads(response.text)
            #print(data)
            return data


        '''put-запрос для обновления данных в карточке инцидента'''
        def update_inc(self, url, data, token, number):

            response = requests.put(url, json=data, headers=token)
            if response.status_code == 200:
                print(f'Успешно обновил инцидент:{number}')
            else:
                print(f'Ошибка при обновлении инцидента: {number}')
                print(response.status_code)



