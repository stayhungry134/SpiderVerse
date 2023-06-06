"""
name: base_wallhaven
create_time: 6/5/2023 8:45 PM
author: Ethan

Description: 
"""
import logging
import os
import requests

chrome_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'


# def get_proxy():
#     return requests.get("http://127.0.0.1:5010/get/").json()
#
#
# def delete_proxy(proxy):
#     requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


class BaseWallHaven:
    """
    WallHaven 壁纸网站的基类
    q: 搜索关键词
    categories: 001: General, 010: Anime, 100: People
    purity: 100: SFW, 110: Sketchy, 111: NSFW
    sorting: relevance, random, date_added, views, favorites, toplist
    order: desc, asc
    ai_art_filter: 0: All, 1: Only Anime, 2: Only People
    start_page: 初始页
    end_page: 结束页
    """

    def __init__(self, q='', categories='001', purity=100, sorting='date_added', order='desc', ai_art_filter=1, start_page=1, end_page=2):
        import socket
        import sqlite3
        self.url = 'https://wallhaven.cc/'
        self.headers = {
            'User-Agent': chrome_agent,
            'Referer': self.url,
        }
        self.q = q
        self.categories = categories
        self.purity = purity
        self.sorting = sorting
        self.order = order
        self.ai_art_filter = ai_art_filter
        self.start_page = start_page
        self.end_page = end_page
        if socket.gethostname() == 'MY-DESKTOP':
            self.save_path = 'E:/Image/WallHaven/'
        elif socket.gethostname() == 'MY-COLORFUL':
            self.save_path = 'D:/Image/WallHaven/'

        # 不存在就创建保存路径
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        # 设置代理
        self.proxy = ''

        # 查看数据库是否存在，不存在就创建
        conn = sqlite3.connect('wallhaven.db')
        cursor = conn.cursor()
        cursor.execute('create table if not exists wallhaven (id integer primary key autoincrement, img_name varchar(255))')
        cursor.close()
        conn.close()

    def parsing_page(self, page=1):
        """解析页面，获得图片详情页的 url"""
        import requests
        from lxml import etree
        # self.proxy = get_proxy().get("proxy")
        logging.info(f"使用代理：{self.proxy}")
        url = f"{self.url}search?" \
              f"&q={self.q}" \
              f"&categories={self.categories}" \
              f"&purity={self.purity}" \
              f"&sorting={self.sorting}" \
              f"&order={self.order}" \
              f"&page={page}"
        response = requests.get(url, headers=self.headers)
        html = etree.HTML(response.text)
        img_detail_urls = html.xpath('//figure/a/@href')
        return img_detail_urls

    def parsing_detail(self, img_detail_url):
        """解析详情页，获得图片的 url"""
        import requests
        from lxml import etree
        response = requests.get(img_detail_url, headers=self.headers)
        html = etree.HTML(response.text)
        try:
            img_url = html.xpath('//img[@id="wallpaper"]/@src')[0]
            return img_url
        except IndexError:
            logging.error(f"图片详情页：{img_detail_url}，没有找到图片的 url")

    def download_img(self, img_url):
        """下载图片"""
        import sqlite3
        import requests
        img_name = img_url.split('/')[-1]
        # 如果图片已经下载过了，就不再下载
        conn = sqlite3.connect('wallhaven.db')
        cursor = conn.cursor()
        cursor.execute('select * from wallhaven where img_name=?', (img_name,))
        if cursor.fetchone():
            print(f"{img_name}已经下载过了！！！")
            return
        response = requests.get(img_url, headers=self.headers)
        with open(self.save_path + img_name, 'wb') as f:
            f.write(response.content)
            print(f"{img_name}下载成功！！！")

    def record_imgs(self, img_names):
        """记录已经下载的图片"""
        import sqlite3
        conn = sqlite3.connect('wallhaven.db')
        cursor = conn.cursor()
        for img_name in img_names:
            cursor.execute('insert into wallhaven (img_name) values (?)', (img_name,))
        conn.commit()
        cursor.close()
        conn.close()

    def run(self):
        """运行"""
        from threading import Thread
        for page in range(self.start_page, self.end_page + 1):
            img_detail_urls = self.parsing_page(page)
            # 多线程下载图片
            threads = []
            img_names = []
            for img_detail_url in img_detail_urls:
                img_url = self.parsing_detail(img_detail_url)
                if not img_url:
                    continue
                img_names.append(img_url.split('/')[-1])
                task = Thread(target=self.download_img, args=(img_url,))
                task.start()
                threads.append(task)
            for task in threads:
                task.join()
            # 记录已经下载的图片
            self.record_imgs(img_names)
            # 记录已经下载的页数
            with open('wallhaven1.txt', 'a') as f:
                f.write(str(page))
                f.write('\n')
            print(f"第{page}页下载完成！！！")
