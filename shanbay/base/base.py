"""
name: base
create_time: 2023/5/22
author: Ethan

Description: 
"""
import pyaml
import requests
import subprocess
from functools import partial
# 目录路径
from .config import BASE_DIR

# 这样设置之后导入 execjs 才能正确执行
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
from datas.global_data import chrome_agent


def get_cookies():
    """获取cookies"""
    with open(f'{BASE_DIR}/base/cookies.yaml', 'r', encoding='utf-8') as f:
        cookies = pyaml.yaml.safe_load(f)
        return cookies


class ShanBay:
    """扇贝单词"""

    def __init__(self, api_url, params):
        self.url = 'https://www.shanbay.com/'
        self.headers = {
            'Origin': 'https://web.shanbay.com',
            'Referer': 'https://web.shanbay.com/',
            'User-Agent': chrome_agent,
        }
        self.api_url = api_url
        self.params = params

    def get_cookie(self):
        """获取cookie和data"""
        import os
        os.system('python get_cookies.py')

    def get_data(self):
        """获取数据"""
        response = requests.get(url=self.api_url, headers=self.headers, params=self.params, cookies=get_cookies())
        # 如果登录失效
        if response.status_code != 200:
            if response.status_code == 401:
                return 401
            else:
                print(response.status_code, response.text)
        else:
            return response