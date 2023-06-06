"""
name: wallhaven
create_time: 6/5/2023 9:06 PM
author: Ethan

Description: 
"""
from base_wallhaven import BaseWallHaven


# wallhaven = BaseWallHaven(categories='001', purity=100, sorting='date_added', order='desc', ai_art_filter=1, start_page=22, end_page=51)
#
# wallhaven.run()


wallhaven = BaseWallHaven(categories='100', purity=100, sorting='date_added', order='desc', ai_art_filter=1, start_page=1, end_page=50)

wallhaven.run()