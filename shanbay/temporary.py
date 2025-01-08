"""
name: temporary.py
create_time: 2023/5/24
author: Ethan

Description: 
"""
from base.word_base import LearnedWords

today_words = LearnedWords(page=1)
today_words.save_word()