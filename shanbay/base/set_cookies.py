"""
name: get_cookies
create_time: 2023/5/23
author: Ethan

Description: 
"""
import time
import platform

import pyaml
from .config import BASE_DIR
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def read_user():
    with open(f'{BASE_DIR}/base/user.yaml', encoding='utf-8') as f:
        user = pyaml.yaml.safe_load(f)
    return user


def write_cookies(cookies):
    with open(f'{BASE_DIR}/base/cookies.yaml', encoding='utf-8', mode='w') as f:
        pyaml.yaml.safe_dump(cookies, f)


def operate_chrome():
    user = read_user()

    options = Options()

    WINDOW_SIZE = "1920, 1080"
    # 不打开浏览器(无头模式, 无界面模式)
    options.add_argument("--headless")
    # 设置浏览器分辨率（窗口大小）
    options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # 禁用Chrome浏览器的沙盒模式。沙盒模式是Chrome浏览器的一种安全机制，它会限制Chrome浏览器的一些功能，从而防止恶意软件利用Chrome浏览器来破坏或窃取用户的数据。
    options.add_argument('--no-sandbox')
    # 禁用Chrome浏览器中与自动化控制相关的Blink特性。这个参数通常用于绕过一些网站对自动化工具（如Selenium）的检测。
    options.add_argument('--disable-blink-features=AutomationControlled')
    # 禁用Chrome浏览器的扩展功能。这个参数可以防止一些扩展插件对浏览器行为的影响。
    options.add_argument("--disable-extensions")
    # 设置Chrome浏览器是否使用自动化扩展。将其设置为False可以禁用自动化扩展。
    options.add_experimental_option('useAutomationExtension', False)
    # 排除指定的Chrome浏览器启动选项。在这个例子中，排除了"enable-automation"选项，这可以帮助规避一些网站对自动化工具的检测。
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://web.shanbay.com/web/main')
    # 登录
    driver.implicitly_wait(15)
    login = driver.find_element(By.CLASS_NAME, 'sign')
    login.click()
    driver.implicitly_wait(15)
    account = driver.find_element(By.XPATH, '//input[@name="account"]')
    password = driver.find_element(By.XPATH, '//input[@name="password"]')
    account.send_keys(user['account'])
    password.send_keys(user['password'])
    driver.implicitly_wait(15)
    login_btn = driver.find_element(By.XPATH, '//button[text()="登录"]')
    login_btn.click()
    driver.implicitly_wait(15)
    word_card = driver.find_element(By.XPATH, '//div[@id="task-1"]')
    word_card.click()
    driver.implicitly_wait(15)
    word_table = driver.find_element(By.XPATH, '//a[contains(text(), "词表")]')
    word_table.click()
    driver.implicitly_wait(15)
    time.sleep(15)
    all_cookie = driver.get_cookies()
    cookie_list = ['csrftoken', 'auth_token', 'amp_a0683b', '_gat', 'amp_a0683b', '_ga', '_gid', 'sessionid']
    cookies = {cookie['name']: cookie['value'] for cookie in all_cookie if cookie['name'] in cookie_list}
    write_cookies(cookies)


def main():
    operate_chrome()


if __name__ == '__main__':
    main()