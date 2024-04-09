from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.edge.options import Options
import requests
import deepl
from opencc import OpenCC

def translate_to_chinese(text):
    auth_key = '7f5065f2-fff4-4068-87bd-e5d4ab57bd9f:fx'  # 你的 DeepL API key
    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang="ZH")

    # 將簡體中文轉換為繁體中文
    cc = OpenCC('s2t')
    traditional_chinese = cc.convert(result.text)
    
    return traditional_chinese


# JLPT Sensei N3 單字列表的 URL
web_url = 'https://jlptsensei.com/jlpt-n3-vocabulary-list/'

# 你的 Discord Webhook URL
DiscordWebhook_url = 'https://discord.com/api/webhooks/1227308005834358855/57JuMT04KF0-ispObr4jgGVR2goj58jd2oqQeu-msmu89pn8EGprH5TC-BA3CwMV2qiA'

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
for word in words[:1]:
    # 從每一個單字中找到單元格
    kanji = word.find('td', {'class': 'jl-td-vr align-middle'}).text
    hiragana = word.find('a', {'class': 'jl-link'}).text
    english = word.find('td', {'class': 'jl-td-vm align-middle'}).text

    # 翻譯英文解釋
    chinese = translate_to_chinese(english)

    # 將單字添加到 vocab 列表中
    vocab.append({
        '漢字': hiragana,
        '平假名': kanji,
        '中文翻譯': chinese
    })

# 印出前五個單字
for v in vocab:
    print(v)
    # 將詞彙資訊格式化為一個漂亮的字串
    vocab_str = '\n'.join(f'{key}: {value}' for key, value in v.items())
    # 發送訊息到 Discord
    requests.post(DiscordWebhook_url,
        json={
            'content': vocab_str
        }
    )

# 關閉 webdriver 物件
driver.quit()