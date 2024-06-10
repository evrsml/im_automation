import time
import requests
import json
import logging


'''класс для запросов к ИМ'''
class GetIMdata():

    """получаем список инцидентов по фильтру Без ответа ВК"""
    def get_inc_without_answers(self, token):

        try:
            base_url = 'https://im.gosuslugi.ru/api/inc/incidents/?offset=1&limit=10&ordering=-current_stage_term&current_stage=3&personal=99988&workflow=322'
            response = requests.get(base_url, headers=token)
            data = json.loads(response.text)
            inc_count = data['count']
            current_url = f'https://im.gosuslugi.ru/api/inc/incidents/?offset=0&limit={inc_count}&ordering=-current_stage_term&current_stage=3&personal=99988&workflow=322'
            response = requests.get(current_url, headers=token)
            data = json.loads(response.text)
            #print(data)
            return data
        except KeyError:
            logging.error("Ошибка авторизации", data)

    '''формируем данные для настройки публикации'''
    def publication_setup(self, data):
        base_setup = {"authors": [{"mentions": ["[id614804235|Ekaterina Mazitova]"],"post_url": "","author_id": 1,"is_private": False, "created_in_incident": None }], "accounts": {"VK": -1}, }
        base_setup["authors"][0]['mentions'][0] = data["source_post"]["author"]["social_name"]
        base_setup["authors"][0]["post_url"] = data["source_post"]["url"]
        base_setup["authors"][0]["author_id"] = data["source_post"]["author"]["author_id"]
        return base_setup

    '''get-запрос на получения данных по инциденту'''
    def get_inc(self, inc_num, text, hand_pub_link, token):
        print("Нашел ответ! Провожу в системе...")
        base_url = f'https://im.gosuslugi.ru/api/inc/incidents/{inc_num}'

        payload = {"category": 0,
                   "subcategory": 0,
                   "location": 0,
                   "priority": 589,
                   "report": 0,
                   "source_post_id": 0,
                   "assigned_user": 0,
                   "client_reference": 0,
                   "check_updated": 0}

        try:
            response = requests.get(base_url, headers=token)
            print("GET 0", response.status_code)
            response.raise_for_status()

        except requests.exceptions.ConnectionError as err:
            logging.error(f"Error Connecting: {err}")


        data = response.json()
        payload.update({
                    "category": data["category"],
                   "subcategory": data["subcategory"],
                   "location": data["location"],
                   "priority": 589,
                   "report": data['report'],
                   "source_post_id": data["source_post_id"],
                   "assigned_user": data["assigned_user"],
                   "client_reference": data["client_reference"],
                   "check_updated": data['updated']
        })

        publication_setup = self.publication_setup(data)
        self.update_inc(publication_setup, payload, inc_num, text, hand_pub_link, token)

    """запрос обновленных данных по карточке инциденнта"""
    def get_latest(self, inc_num, token):
        try:
            res = []
            url = f'https://im.gosuslugi.ru/api/inc/responses/latest/{inc_num}/'
            response = requests.get(url=url, headers=token)
            data = json.loads(response.text)
            resp_id = data['id']
            updated = data['updated']
            res.append(resp_id)
            res.append(updated)
            #print("GET latest 3", response.status_code)
            return res
        except Exception as e:
            logging.error("Ошибка GET latest 3", e)

    '''запросы для обновления данных в карточке инцидента (проведение первого ответа)'''
    def update_inc(self, publication_setup, payload, inc_num, text, hand_pub_link, token):

        try:
            url = f"https://im.gosuslugi.ru/api/inc/incidents/{inc_num}/"
            response = requests.put(url, json=payload, headers=token)
            data = json.loads(response.text)
            #print("PUT 1", response.status_code)

            post_payload = {"incident":0,"text":"","next_stage":3,"publication_setup":{"authors": "","accounts":{"VK":-1}},"sticker_id":""}
            post_payload['incident'] = inc_num
            post_payload['text'] = text
            post_payload['publication_setup'] = publication_setup

            post_url = 'https://im.gosuslugi.ru/api/inc/responses/'
            resp = requests.post(url=post_url, json=post_payload, headers=token)
            #print("POST 2", resp.status_code)

            post_publish_url = f'https://im.gosuslugi.ru/api/inc/incidents/{inc_num}/publish/'
            payload_post_publish = {"check_updated":0}
            payload_post_publish["check_updated"] = data['updated']
            resp = requests.post(url=post_publish_url, json=payload_post_publish, headers=token)
            #print("POST 4", resp.status_code)

            get_url = f'https://im.gosuslugi.ru/api/inc/incidents/{inc_num}'
            resp_get = requests.get(url=get_url, headers=token)
            data_get = json.loads(resp_get.text)

            data_latest = self.get_latest(inc_num, token)
            patch_resp_url = f'https://im.gosuslugi.ru/api/inc/responses/{data_latest[0]}/'
            payload_patch = {"text":"","publication_setup":{"authors": [],"accounts":{"VK":-1}},"next_stage":3,"previous_stage":3,"check_updated":"","sticker_id":""}
            payload_patch['text'] = text
            payload_patch["publication_setup"] = publication_setup
            payload_patch['check_update'] = data_latest[1]

            resp = requests.patch(url=patch_resp_url, json=payload_patch, headers=token)
            patch_data_5 = json.loads(resp.text)
            #print("PATCH 5", resp.status_code)

            payload_patch["check_updated"] = patch_data_5["updated"]
            resp = requests.patch(url=patch_resp_url, json=payload_patch, headers=token)
            #print("PATCH 6", resp.status_code)

            put_url = f'https://im.gosuslugi.ru/api/inc/incidents/{inc_num}/'
            put_payload = payload

            put_payload["check_updated"] = data_get["updated"]
            #print(put_payload["check_updated"])
            resp = requests.put(url=put_url, json=put_payload, headers=token)
            put_data = json.loads(resp.text)
            #print("PUT 7", resp.status_code)

            post_url_approve = f'https://im.gosuslugi.ru/api/inc/incidents/{inc_num}/approve/'
            payload_post_appove = {"check_updated":"2024-02-22T13:22:11.126976Z"}
            payload_post_appove["check_updated"] = put_data["updated"]
            resp = requests.post(url=post_url_approve, json=payload_post_appove, headers=token)
            #print("POST 8", resp.status_code)
            time.sleep(4)

            get_handpub_verifi = f'https://im.gosuslugi.ru/api/inc/statuses/?limit=1000&response={data_latest[0]}'

            response_get_handpub_verifi = requests.get(url=get_handpub_verifi, headers=token)
            data_handpub_verifi = json.loads(response_get_handpub_verifi.text)
            #print("GET 9", response_get_handpub_verifi.status_code)
            status_id = data_handpub_verifi["results"][0]["id"]
            #print(status_id)

            patch_handpub = f'https://im.gosuslugi.ru/api/inc/statuses/{status_id}/finish_manually/'

            data_finish_handpub = {'response_link': '',
            'author_link': ''}
            data_finish_handpub['response_link'] = hand_pub_link

            response_patch = requests.patch(url=patch_handpub, json=data_finish_handpub, headers=token)

            #print("PATCH 10", response_patch.status_code)
            if response_patch.status_code == 206:
                print("Ответ проведен успешно! Пошел искать следующий...")
            else:
                print("Произошла ошибка при закрытии ручной публикации")

        except Exception as e:
            logging.error("Произошла ошибка при проведении ответа", e)
            pass












