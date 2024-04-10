from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.edge.options import Options
import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

auth_key = config['DEFAULT']['DEEPL_AUTH_KEY']
DiscordWebhook_url = config['DEFAULT']['DISCORD_WEBHOOK_URL']


# JLPT Sensei N3 單字列表的 URL
web_url = 'https://jlptsensei.com/jlpt-n3-vocabulary-list/'

# 創建一個 Options 物件
options = Options()

# 將無頭模式選項添加到 Options 物件中
options.add_argument("--headless")

# 啟用第三方 cookie
options.add_argument("--enable-features=SameSiteByDefaultCookies")

# 設置日誌級別
options.add_argument("--log-level=3")

# 創建一個 WebDriver 物件，並將 Options 物件作為參數傳入
driver = webdriver.Edge(options=options)

# 使用 webdriver 物件來獲取網頁內容
driver.get(web_url)

# 使用 BeautifulSoup 來解析網頁內容
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 等待 5 秒讓網頁載入
time.sleep(5)

# 找到單字列表
word_list = soup.find('table', {'id': 'jl-vocab'})


if word_list is None:
    print("Didn't find the word list.")
else:
    words = word_list.find_all('tr', {'class': 'jl-row'})

# 創建一個空列表來存儲單字
vocab = []

# 遍歷前1個單字
for word in words[:]:
    # 從每一個單字中找到單元格
    hiragana = word.find('td', {'class': 'jl-td-vr align-middle'}).text
    kanji = word.find('a', {'class': 'jl-link'}).text
    english = word.find('td', {'class': 'jl-td-vm align-middle'}).text

    # # 翻譯英文解釋
    # chinese = translate_to_chinese(english)
    chinese = None

    if chinese == None:
        vocab.append({
        '漢字': kanji,
        '平假名': hiragana,
        '英文翻譯': english
        })
    else:
        # 將單字添加到 vocab 列表中
        vocab.append({
            '漢字': kanji,
            '平假名': hiragana,
            '中文翻譯': chinese
        })

# 印出前五個單字
for v in vocab:
    print(v)
    # 將詞彙資訊格式化為一個漂亮的字串
    vocab_str = '|'.join(f'{key}: {value}' for key, value in v.items())
    # # 發送訊息到 Discord
    # requests.post(DiscordWebhook_url,
    #     json={
    #         'content': vocab_str
    #     }
    # )

# 關閉 webdriver 物件
driver.quit()

