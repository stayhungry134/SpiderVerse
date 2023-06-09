"""
name: word_base
create_time: 2023/5/24
author: Ethan

Description: 
"""
import json
import os
import pyaml

from .config import BASE_DIR
from .base import ShanBay


def parse_data(data):
    """解析数据"""
    import execjs
    with open(f'{BASE_DIR}/base/bays4.js', 'r', encoding='utf-8') as f:
        shell = f.read()
    return execjs.compile(shell).call('kmno4_decode', data)


class BaseWords(ShanBay):
    """单词基类"""

    def __init__(self, page=1, api='today_learning_items', params=None):
        self.page = page
        self.api = api
        self.params = params
        self.current = 0
        self.total = 50
        base_url = 'https://apiv3.shanbay.com/wordsapp/user_material_books/buqwfz/learning/words/'
        api_url = base_url + self.api
        super().__init__(api_url, params)
        self.words_dic = {}

    def get_words(self):
        """获取单词"""
        words_dic = {}
        while self.total > self.current:
            self.params['page'] = self.current // 10 + 1
            words_dic.update(self.extract_word())
        self.words_dic = words_dic
        return words_dic

    def verify_response(self):
        """获取cookies"""
        if self.get_data().status_code != 200:
            result = self.set_cookie()
            if result:
                response = self.get_data()
                print('cookies更新成功！')
            else:
                raise Exception('获取cookies失败！')
        else:
            response = self.get_data()
        words_data = response.json().get('data')
        words_json = json.loads(parse_data(words_data))
        words = words_json.get('objects')
        self.total = words_json.get('total')
        self.current += 10
        return words

    def extract_word(self):
        """提取单词"""
        words = self.verify_response()
        words_list = [word_item['vocab_with_senses'] for word_item in words]
        words_dic = {word_item['word']: {'word': word_item['word'],
                                         'definition': [f"{definition['pos']} {definition['definition_cn']}" for
                                                        definition in word_item['senses']],
                                         'uk_audio': word_item['sound']['audio_uk_urls'][0],
                                         'us_audio': word_item['sound']['audio_us_urls'][0], }
                     for word_item in words_list}
        return words_dic

    def save_word(self):
        """保存单词"""
        import datetime
        today = datetime.date.today()
        words_dic = self.words_dic or self.get_words()
        with open(f'{BASE_DIR}/../0_files/word_json/{today.isoformat()}.json', 'w', encoding='utf-8') as f:
            json.dump(words_dic, f, ensure_ascii=False, indent=4)
        with open(f'{BASE_DIR}/../0_files/word_text/{today.isoformat()}.txt', 'w', encoding='utf-8') as f:
            for word in words_dic.keys():
                f.write(word.replace('\'', ''))
                f.write('\n')
        print('保存成功！')


class TodayWords(BaseWords):
    """今日单词"""
    def __init__(self, page=1, api='today_learning_items'):
        self.page = page
        params = {
            'ipp': 10,
            'page': self.page,
            'type_of': 'NEW'
        }
        with open(f'{BASE_DIR}/base/config.yaml', 'r', encoding='utf-8') as f:
            config = pyaml.yaml.safe_load(f)
        self.put_url = config.get('put_url')
        super().__init__(page, api, params)

    def upload_words(self):
        """将今日的单词上传到服务器"""
        import os
        import datetime
        import requests
        # 如果目录中有今日的单词文件，则上传
        today = datetime.date.today().isoformat()
        if os.path.exists(f'{BASE_DIR}/../0_files/word_json/{today}.json'):
            with open(f'{BASE_DIR}/../0_files/word_json/{today}.json', 'r', encoding='utf-8') as f:
                words_dic = json.load(f)
        else:
            words_dic = self.words_dic or self.get_words()
        print(self.put_url)
        response = requests.post(self.put_url, json=words_dic)
        print(response.text)
        return response.text

    def upload_article(self):
        """将今日的文章上传到服务器"""
        import re
        import requests
        import openai
        words_dic = self.words_dic or self.get_words()
        words = ', '.join(words_dic.keys())
        system_content = "You are a useful assistant. You can generate an article title based on the words given by " \
                         "the user and return the format {title:, content:}"
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': 'system', 'content': system_content},
                {'role': 'user', 'content': words},
            ]
        )

        article = completion.choices[0].message.content
        title = re.findall(r'[tT]itle:\W*(.*)\n*[Cc]ontent:', article)[0]
        content = re.findall(r'[cC]ontent:.*\n*(.*)', article)[0]
        data = {
            'title': title,
            'content': content
        }
        requests.post(self.url, data=data)


class ReviewWords(BaseWords):
    """复习单词"""
    def __init__(self, page=1, api='today_learning_items'):
        self.page = page
        params = {
            'ipp': 10,
            'page': self.page,
            'type_of': 'REVIEW'
        }
        super().__init__(page, api, params)


class LearnedWords(BaseWords):
    """已学单词"""
    def __init__(self, page=1, api='learning_items', order_by='CREATED_AT', order='DESC'):
        # 排序方式：CREATED_AT为按时间排序，FAMILIARITY为按熟悉程度排序
        order_by_list = ['CREATED_AT', 'FAMILIARITY']
        # 排序方式：ASC为升序，DESC为降序
        order_list = ['ASC', 'DESC']
        if order_by not in order_by_list:
            raise ValueError(f"Invalid value for order_by. Available options are: {order_by_list}")
        if order not in order_list:
            raise ValueError(f"Invalid value for order. Available options are: {order_list}")

        self.page = page
        self.order_by = order_by
        self.order = order

        params = {
            'ipp': 10,
            'page': self.page,
            'order_by': self.order_by,
            'order': self.order
        }
        super().__init__(page, api, params)

    def extract_word(self):
        """重写提取单词方法，因为已学单词中有熟悉程度"""
        words = self.verify_response()
        words_dic = {word_item['vocab_with_senses']['word']:
                         {'word': word_item['vocab_with_senses']['word'],
                          'definition': [f"{definition['pos']} {definition['definition_cn']}" for
                                         definition in word_item['vocab_with_senses']['senses']],
                          'familiarity': word_item['familiarity'],
                          'uk_audio': word_item['vocab_with_senses']['sound']['audio_uk_urls'][0],
                          'us_audio': word_item['vocab_with_senses']['sound']['audio_us_urls'][0], }
                     for word_item in words}
        return words_dic


class SimpleWords(BaseWords):
    """简单词"""
    def __init__(self, page=1, api='simple_learned_items', order='DESC'):
        # 首次学习时间排序方式：ASC为升序，DESC为降序
        order_list = ['ASC', 'DESC']
        if order not in order_list:
            raise ValueError(f"Invalid value for order. Available options are: {order_list}")

        self.page = page
        self.order = order
        params = {
            'ipp': 10,
            'page': self.page,
            'order': self.order
        }
        super().__init__(page, api, params)
