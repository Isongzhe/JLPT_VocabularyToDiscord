import deepl
from opencc import OpenCC
import configparser
import re


config = configparser.ConfigParser()
config.read('config.ini')

#deepl API key
auth_key = config['DEFAULT']['DEEPL_AUTH_KEY']

def translate_to_chinese(text):

    # 使用 deepl API 來翻譯文本
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang="ZH") #輸入語言自動偵測，翻譯成中文

    # 將簡體中文轉換為繁體中文
    cc = OpenCC('s2t')
    traditional_chinese = cc.convert(result.text)
    
    return traditional_chinese

def split_hiragana_and_romaji(word):
    romaji, hiragana = re.split(r'([a-z]+)(.*)', word['平假名'])[1:3]
    return {
        '漢字': word['漢字'],
        '平片假名': hiragana,
        '羅馬拼音': romaji,
        '英文翻譯': word['英文翻譯']
    }

