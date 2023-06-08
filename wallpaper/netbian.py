# 导入相关库
import os
import requests
from threading import Thread
from lxml import etree
import time

# 指定url
url = 'http://pic.netbian.com/4kmeinv/' # 美女
# url = 'http://pic.netbian.com/4kfengjing/'  # 风景
# url = 'https://pic.netbian.com/4kdongman/'  # 动漫
# url = 'https://pic.netbian.com/4kyouxi/'  # 游戏
# url = 'http://pic.netbian.com/4kyingshi/'  # 影视
# url = 'http://pic.netbian.com/4kqiche/'  # 汽车
# url = 'http://pic.netbian.com/4kdongwu/'  # 动物
# url = 'http://pic.netbian.com/4krenwu/'  # 人物
# url = 'http://pic.netbian.com/4kzongjiao/'  # 宗教
# url = 'http://pic.netbian.com/4kbeijing/'  # 背景
# url = 'http://pic.netbian.com/pingban/'  # 平板
# url = 'http://pic.netbian.com/shoujibizhi/'  # 手机

# 进行 UA 伪装
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4400.8 Safari/537.36',
    'Connection': 'close'
}

# 指定保存目录
file_path = 'E:/image/netbian/meinv/'

if not os.path.exists(file_path):
    os.mkdir(file_path)

# 获取图片详情页链接和下一页链接
def get_img_list(net_url):
    # 获取网页数据
    response = requests.get(url=net_url, headers=headers).content.decode('gbk')
    # 解析数据
    html = etree.HTML(response)
    # 解析图片列表
    ls_img = html.xpath('//div[@class="slist"]//li/a/@href')
    next_url = html.xpath('//div[@class="page"]/a/@href')[-1]
    return ls_img, next_url


# 爬取图片
def get_img(href):
    detail_utl = 'http://pic.netbian.com' + href
    img_detail = requests.get(url=detail_utl, headers=headers).content.decode('gbk')
    img_html = etree.HTML(img_detail)
    img_name = img_html.xpath('//h1/text()')[0]
    img_href = img_html.xpath('//div[@class="photo-pic"]//img/@src')[0]
    return img_name, img_href


# 下载图片
def download_img(name, src):
    try:
        img_url = 'http://pic.netbian.com' + src
        img_data = requests.get(url=img_url, headers=headers).content
        img_path = file_path + name + '.jpg'
        with open(img_path, 'wb') as fp:
            fp.write(img_data)
            print(name, "保存成功！")
    except:
        print(name, '保存失败')


# 主程序
def main():
    img_list, next_url = get_img_list(url)
    # 使用多线程
    threads = []
    for img_url in img_list:
        img_name, img_href = get_img(img_url)
        task = Thread(target=download_img, args=(img_name, img_href))
        task.start()
        threads.append(task)

    for task in threads:
        task.join()
    return next_url


for i in range(69):
    next_url = main()
    url = 'http://pic.netbian.com' + next_url
    print("第{}页保存成功！！！".format(i))
