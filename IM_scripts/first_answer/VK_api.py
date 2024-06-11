from IM_scripts.first_answer.id_list import gospublic_list
import json
import requests
import re
import os
from dotenv import load_dotenv
import logging

load_dotenv()

TOKEN = os.environ.get('VK_TOKEN')


'''парсер ссылки'''
def comment_link_parse(link):
   if 'topic' not in link and 'msgid' not in link:
        res_id = ['','', None, '']
        pattern_comment = r"_r+\d+|reply=\d+|&thread=\d+"
        pattern_post = r"-?\d+_\d+"
        res_post = re.findall(pattern_post, link)
        res_comment = re.findall(pattern_comment, link)
        result_id_account = res_post[0].split('_')
        #print(res_comment)
        #print(res_post)
        if len(res_comment) == 0:
            result_id = res_post[0].split('_')
            res_id[0] = int(result_id[0])
            res_id[1] = int(result_id[1])
            #print("post", res_id)
            return request_to_api(res_id)
        else:
            thread = list(filter(lambda x: '&thread' in x, res_comment))
            #print(result_id_account)
            if thread:
                result_id_thread = res_comment[1].split('&thread=')
                result_id_rep = res_comment[0].split('reply=')
                res_id[0] = int(result_id_account[0])
                res_id[1] = int(result_id_account[1])
                res_id[2] = int(result_id_thread[1])
                res_id[3] = int(result_id_rep[1])
                #print("thread", res_id)
                return request_to_api(res_id)
            else:
                result_id_rep = res_comment[0].split('reply=')
                res_id[0] = int(result_id_account[0])
                res_id[1] = int(result_id_account[1])
                res_id[2] = int(result_id_rep[1])
                res_id[3] = int(result_id_rep[1])
                #print("reply", res_id)
                return request_to_api(res_id)
   else:
        pass

'''узнаем, айди жителя, который обратился'''
def get_user_id(url):
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        #print("User id", data)
        user_id = data['response']['items'][0]['from_id']
        return user_id
    except KeyError:
        logging.error("Ошибка определения id жителя", data)

'''запросы к ВК апи'''
def request_to_api(url):
    '''получаем ветку комментариев и айди жителя из комментария-обращения'''
    if url[2] is not None:
        url_com = f"https://api.vk.com/method/wall.getComments?owner_id={url[0]}&comment_id={url[2]}&v=5.199&access_token={TOKEN}"
        user_id = f"https://api.vk.com/method/wall.getComment?owner_id={url[0]}&comment_id={url[3]}&v=5.199&access_token={TOKEN}"
        user = get_user_id(user_id)
        #print('post with comments')
        return comment_check(url_com, user)
    else:
        url_without_comment = f"https://api.vk.com/method/wall.getComments?owner_id={url[0]}&post_id={url[1]}&v=5.199&access_token={TOKEN}"
        #print("post without comments")
        return comment_check(url_without_comment)

'''проверям список комментариев на наличие в них ответов заявителю от госпабликов'''
def comment_check(url, user_id=None):
    response = requests.get(url)
    data = json.loads(response.text)
    if 'error' not in data:
        #print(data)
        items_count = len(data['response']['items'])
        #print('items count', items_count)
        if items_count != 0:
            answers = ['','']
            #print(user_id)
            for i in range(items_count):
                item = data['response']['items'][i]
                if item['from_id'] in gospublic_list and f'id{user_id}' in item['text']:
                    owner_id = item["owner_id"]
                    post_id = item["post_id"]
                    id = item["id"]
                    url = f"https://vk.com/wall{owner_id}_{post_id}?reply={id}"
                    answers[0] = item['text']
                    answers[1] = url

                else:
                    pass
                    #print('Аккаунт не в списке')
            #print('текст который верну', answers)

            return answers
        else:
            return None

    else:
        return None




