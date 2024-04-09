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
    
kanji = 'Konnichiwa​'
# 翻譯英文解釋
# chinese = translate_to_chinese(kanji)
# print(chinese)



vocab = {'漢字': '明かり', '平假名': 'akariあかり', '中文翻譯': '光；照明；發光；熠熠生輝'}

# 將詞彙資訊格式化為一個漂亮的字串
vocab_str = '\n'.join(f'{key}: {value}' for key, value in vocab.items())

# 你的 Discord Webhook URL
webhook_url = 'https://discord.com/api/webhooks/1227308005834358855/57JuMT04KF0-ispObr4jgGVR2goj58jd2oqQeu-msmu89pn8EGprH5TC-BA3CwMV2qiA'

# 發送訊息到 Discord
requests.post(
    webhook_url,
    json={
        'content': vocab_str
    }
)