from redis_conf.config import rc as Redis
import json
import requests


class TokenError(Exception):
    pass

class GetAuth:

    '''проверям есть ли валидный токен в редисе'''
    def check_token(self):
        token = Redis.get_token()
        if token:
            return self.get_headers(token)
        else:
            print("запускаем get_creds")
            try:
                return self.get_creds()
            except TokenError:
                return False

    '''получаем данные для авторизации'''

    def get_creds(self):
        creds = Redis.get_creds()
        print(creds)
        self.issue_token(creds[0], creds[1])

    '''получаем токен и заголовки для запросов к API'''
    def issue_token(self, username, password):
        url_token = 'https://im.gosuslugi.ru/api/token-auth/'

        try:
            data = {"username": f'{username}', "password": f'{password}'}
            response = requests.post(url_token, data=data)
            token_data = json.loads(response.text)
            token = token_data['access']['token']
            #записываем токен для переиспользования
            Redis.set_token(token)
            headers = self.get_headers(token)
            print(token)
            print(token_data)
            return headers

        except KeyError:
            raise TokenError


    '''получаем заголовки вместе с токеном'''

    def get_headers(self, token):
        headers = {"Authorization": f'Token {token}',
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                   'Content-Type': 'application/json'}

        return headers