import requests
import unittest
import json
from pprint import pprint

class TestSendNews(unittest.TestCase):
    def test_post_request(self):
        data = {
        "embeds": [
            {
                "title": "Apr 19 - Easy Japanesse新聞",
                "fields": [
                    {
                        "name": "1.テイラー・スウィフトさんの新アルバム、ＳＮＳ上に「リーク」か物議醸す",
                        "value": "[テイラー・スウィフトさんの新アルバム、ＳＮＳ上に「リーク」か物議醸す](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e90563?hl=zh-TW)"
                    },
                    {
                        "name": "2.ボーイング社のエンジニア機体製造不正を議会で証言",
                        "value": "[ボーイング社のエンジニア機体製造不正を議会で証言](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e554ca?hl=zh-TW)"
                    },
                    {
                        "name": "3.ゾウが街をウロウロサーカスから逃げ出し…アメリカ・モンタナ州",       
                        "value": "[ゾウが街をウロウロサーカスから逃げ出し…アメリカ・モンタナ州](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e54512?hl=zh-TW)"
                    },
                    {
                        "name": "4.「ロシア兵の死者数は5万人超」英BBC",
                        "value": "[「ロシア兵の死者数は5万人超」英BBC](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e551bb?hl=zh-TW)"
                    },
                    {
                        "name": "5.「クチコミを消してほしい」医者などがグーグルを訴えた",
                        "value": "[「クチコミを消してほしい」医者などがグーグルを訴えた](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e4fe6d?hl=zh-TW)"
                    },
                    {
                        "name": "6.中東・ドバイで記録的大雨半日で1年分の降水量…空港は冠水し湖のように",
                        "value": "[中東・ドバイで記録的大雨半日で1年分の降水量…空港は冠水し湖のように](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e54157?hl=zh-TW)"
                    },
                    {
                        "name": "7.中東ドバイで記録的な大雨洪水で空港が“湖”に",
                        "value": "[中東ドバイで記録的な大雨洪水で空港が“湖”に](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e50ae2?hl=zh-TW)"
                    },
                    {
                        "name": "8.鹿児島県の奄美大島夜になると光る小さいきのこ",
                        "value": "[鹿児島県の奄美大島夜になると光る小さいきのこ](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e4ff2c?hl=zh-TW)"
                    },
                    {
                        "name": "9.スタジオジブリがカンヌ国際映画祭の「名誉パルムドール」受賞へ団体での受賞は初",
                        "value": "[スタジオジブリがカンヌ国際映画祭の「名誉パルムドール」受賞へ団体での受賞は初](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e5347e?hl=zh-TW)"
                    },
                    {
                        "name": "10.英政府が香港問題の報告書を発表「国際人権法に反する」中国は反発",   
                        "value": "[英政府が香港問題の報告書を発表「国際人権法に反する」中国は反発](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e51544?hl=zh-TW)"
                    },
                    {
                        "name": "11.インドネシアのルアング火山が大規模噴火住民ら避難しけが人なし",     
                        "value": "[インドネシアのルアング火山が大規模噴火住民ら避難しけが人なし](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e52779?hl=zh-TW)"
                    },
                    {
                        "name": "12.ユリアさんが「世界で最も影響力のある100人」にタイム誌が発表",      
                        "value": "[ユリアさんが「世界で最も影響力のある100人」にタイム誌が発表](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e51e22?hl=zh-TW)"
                    },
                    {
                        "name": "13.傾いた9階建てビルの解体終わる建物内の猫やニワトリも“救出”台湾地震",
                        "value": "[傾いた9階建てビルの解体終わる建物内の猫やニワトリも“救出”台湾地震](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e53706?hl=zh-TW)"
                    },
                    {
                        "name": "14.「世界に影響がある100人」に宮崎駿さんなどが選ばれた",
                        "value": "[「世界に影響がある100人」に宮崎駿さんなどが選ばれた](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e3fb3a?hl=zh-TW)"
                    },
                    {
                        "name": "15.山形県水の中から木が生えているような湖でカヌーを楽しむ",
                        "value": "[山形県水の中から木が生えているような湖でカヌーを楽しむ](https://easyjapanese.net/detail/7e65ea6a82a181037fde0c8268e4003b?hl=zh-TW)"
                    }
                ]
            }
        ]
    }   

        webhook_url = r'https://discord.com/api/webhooks/1231946584372281426/5_RF3l1P_ECzXxd-1kJdlfkhAPBCuhfPWZ9ICPS5bzPQiMKU-B_wVIsGLAF0SzpcLM08'
        headers = {"Content-Type": "application/json"}
        response = requests.post(webhook_url, json=data, headers=headers)
        self.assertEqual(response.status_code, 204)


    def test_convert_data(self):
        with open('D:/GitHub/JLPT_VocabularyToDiscord/app/utils/EasyJapan_news.json', 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        date = 'Apr 19'
    
        # 建立一個 embed 物件
        embed = {
            "title": f"{date} - Easy Japanesse新聞",
            "fields": []
        }

        # 為每條新聞添加一個 field
        for i, news_item in enumerate(news_data, start=1):
            for news in news_item['news']:
                # 將 name 翻譯為中文
                name = f"{news['name']}".replace('\u3000', '').replace(' ', '')

                # # 將 name 翻譯為中文
                # translated_name = translate_to_chinese(name)
                # translated_name= translated_name
                # print(f"Translated name: {translated_name}")

                jp_name = f"{i}.{name}"
                value = f"[{name}]({news['webURL']})"
                # print(f"Value: {value}")
                
                embed["fields"].append({
                    "name": jp_name,
                    "value": value
                })

        # 將 embed 物件轉換為 JSON 字串
        for field in embed["fields"]:
            field["name"] = field["name"]
            field["value"] = field["value"]
            # 檢查欄位長度
            if len(field["name"]) > 1024 or len(field["value"]) > 1024:
                print(f"Field '{field['name']}' or its value is too long.")

        # 將 embed 物件轉換為 JSON 字串
        data = {"embeds": [embed]}

        print("Sending the following data:")
        print(json.dumps(data, ensure_ascii=False, indent=4))  
        webhook_url = r'https://discord.com/api/webhooks/1231946584372281426/5_RF3l1P_ECzXxd-1kJdlfkhAPBCuhfPWZ9ICPS5bzPQiMKU-B_wVIsGLAF0SzpcLM08'
        headers = {"Content-Type": "application/json"}
        response = requests.post(webhook_url, json=data, headers=headers)
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()
