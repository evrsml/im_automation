import requests
import json

'''класс для получения токена для запросов к ИМ'''
class GetToken:

    url_token = 'https://im.gosuslugi.ru/api/token-auth/'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_token(self):

        data = {"username": f'{self.username}', "password": f'{self.password}'}
        response = requests.post(self.url_token, data=data)
        token_data = json.loads(response.text)
        print(token_data)
        token = token_data['access']['token']
        headers = {"Authorization": f'Token {token}',
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36", 'Content-Type': 'application/json'}

        return headers

'''класс для запросов к ИМ'''
class GetIMdata():

        def get_inc(self, token, stage):

            base_url = f'https://im.gosuslugi.ru/api/inc/incidents/?offset=0&limit=10&ordering=-current_stage_term&current_stage={stage}&personal=64452&workflow=322'
            response = requests.get(base_url, headers=token)
            data = json.loads(response.text)
            inc_count = data['count']
            #print(inc_count)
            current_url = f'https://im.gosuslugi.ru/api/inc/incidents/?offset=0&limit={inc_count}&ordering=-current_stage_term&current_stage={stage}&personal=64452&workflow=322'
            response = requests.get(current_url, headers=token)
            data = json.loads(response.text)
            #print(data)
            return data

