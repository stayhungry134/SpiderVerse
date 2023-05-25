"""
name: test
create_time: 2023/5/24
author: Ethan

Description: 
"""
import requests
from base.word_base import TodayWords

today_words = TodayWords()
words = {'charge': {'word': 'charge', 'definition': ['n. 要价，费用；指控；谴责；掌管；电荷；突然猛冲；任务',
                                                     'v. 要（价），收（费）；把…记在账上；控告；谴责；猛冲；使…承担责任；给…充电；（枪）填弹；使充满（…情绪）；向…冲去'],
                    'uk_audio': 'https://media-audio1.baydn.com/abc_pub_audio/4e027617b74d579f73ffe5801f0fb007.60b926999b0463abb1d6661c5c698b21.mp3',
                    'us_audio': 'https://media-audio1.baydn.com/abc_pub_audio/21ca4ff1aaa591d758a275a427f9260e.fd6dce0783dd991c97b6cae32f17bca4.mp3'},
         'major': {'word': 'major',
                   'definition': ['adj. 严重, 主要的, 重要的, 大的', 'n. 少校, 专业课, 主修课程, 主修学生',
                                  'v. 〈美口〉主修'],
                   'uk_audio': 'https://media-audio1.baydn.com/abc_pub_audio/721d59041bf1f6041d78b200af95b9b7.b4113d7b6e5899d24faeb888aa3e97ef.mp3',
                   'us_audio': 'https://media-audio1.baydn.com/abc_pub_audio/107e9b270e631f79526cc0f00dab65bd.9ff4ed325ab60d20f5f0365d87acbff0.mp3'},
         }

url = 'http://127.0.0.1:8000/api/ebbinghaus/put_words/'

response = requests.post(url, json=words)

print(response.text)
