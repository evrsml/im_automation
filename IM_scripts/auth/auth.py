from redis_conf.config import rc as Redis
import json
import requests

class GetToken:

    def check_token(self):
        pass

    def get_creds(self):
        creds = Redis.get_creds()
        self.issue_token(creds[0], creds[1])


    def issue_token(self, username, password):
        url_token = 'https://im.gosuslugi.ru/api/token-auth/'

        data = {"username": f'{username}', "password": f'{password}'}
        response = requests.post(url_token, data=data)
        token_data = json.loads(response.text)
        print(token_data)
        token = token_data['access']['token']
        headers = {"Authorization": f'Token {token}',
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                   'Content-Type': 'application/json'}

        return headers