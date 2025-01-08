"""
name: wallhaven
create_time: 6/5/2023 9:06 PM
author: Ethan

Description: 
"""
from base_wallhaven import BaseWallHaven


# wallhaven = BaseWallHaven(categories='001', purity=100, sorting='date_added', order='desc', ai_art_filter=1, start_page=22, end_page=50)
#
# wallhaven.run()

# https://wallhaven.cc/search?categories=010&purity=100&atleast=1920x1080&sorting=date_added&order=desc&ai_art_filter=1&page=4
def get_anime():
    wallhaven = BaseWallHaven(categories='010',
                              purity=100,
                              atleast='2560x1440',
                              sorting='date_added',
                              order='desc',
                              ai_art_filter=1,
                              start_page=1,
                              end_page=50)

    wallhaven.run()


def get_chinese_anime():
    # q=Chinese%20animation&categories=100&purity=100&sorting=relevance&order=desc&ai_art_filter=1&page=5
    wallhaven = BaseWallHaven(q='Chinese%20animation',
                              categories='100',
                              purity=100,
                              sorting='relevance',
                              order='desc',
                              ai_art_filter=1,
                              start_page=1,
                              end_page=5,
                              save_path='D:/Image/chinese_anime/')
    wallhaven.run()


get_chinese_anime()