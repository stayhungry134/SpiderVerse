"""
name: temporary.py
create_time: 2023/5/24
author: Ethan

Description: 
"""
import json
import os

# 遍历读取 0_files 文件夹下的文件
files = os.listdir('../0_files')
for file in files:
    if file == 'word_text':
        continue
    with open(f'../0_files/{file}', 'r', encoding='utf-8') as f:
        files = json.load(f)
        for word in files.keys():
            with open(f'../0_files/word_text/{file.split(".")[0]}.txt', 'a', encoding='utf-8') as f:
                f.write(word.replace('\'', ''))
                f.write('\n')
