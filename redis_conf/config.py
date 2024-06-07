import redis
import logging


class RedisCheck:
    def __init__(self, host='localhost', port=6379, decode_responses=True):
       self.r = redis.Redis(host=host, port=port, decode_responses=decode_responses)

    '''получаем пароль от аккаунта Медиалогии'''
    def get_creds(self, key="intern3"):
       try:
            creds = []
            password = self.r.lindex(key, 1)
            username = self.r.lindex(key, 0)
            creds.append(username)
            creds.append(password)
            return creds

       except redis.exceptions.ConnectionError as e:
           logging.error('Ошибка redis_conf:', e)

    '''проверяем есть ли токен'''
    def get_token(self, key="token"):
        try:
           if self.r.exists(key):
               token = self.r.get(key)
               return token

        except redis.exceptions.ConnectionError as e:
            logging.error('Ошибка redis_conf:', e)

    '''записываем токен в редис с TTL ~ 2 часа'''
    def set_token(self,value, key="token"):
        try:
            self.r.set(key, value, ex=7000)
            return True

        except redis.exceptions.ConnectionError as e:
               logging.error('Ошибка redis_conf:', e)
            return False



rc = RedisCheck()