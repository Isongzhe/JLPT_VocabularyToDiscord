from scraper_grammer import WebDriver, Scraper
import json
from urllib.parse import quote

def scrape_data(level, encoded_url, end_page):
    driver = WebDriver()
    scraper = Scraper(driver)

    try:
        scraper.scrape_pages(level=level, url=encoded_url, end_page=end_page)
        # data_json = json.dumps(scraper.data, ensure_ascii=False) # Convert the data to json format, and set ensure_ascii to False to display Chinese/Japanese characters
        # print(data_json)
    finally:
        driver.quit()

    return scraper.data

def save_articles_to_file(articles, filename, level):
    with open(filename, 'w', encoding='utf-8') as f:
        for article in articles:
            article['level'] = level
            article['number'] = 0
        json.dump(articles, f, ensure_ascii=False, indent=4)

def load_articles_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

levels_and_numbers = [
    ('26/高級（N1）', 7),
    ('25/中高級（N2）', 7),
    ('24/中級（N3）', 11),
    ('23/初級（N4）', 12),
    ('22/入門（N5）', 6)
]

for level_path, endpage in levels_and_numbers:
    # 轉換網址為UTF-8格式
    base_url = f'https://colanekojp.com.tw/classroom/{level_path}'
    encoded_url = quote(base_url, safe='/:')
    # 取出文章難度
    level = level_path.split('（')[-1].strip('）')  # Extract level from level_path
    #呼叫爬蟲函數，並取得文章
    articles = scrape_data(level, encoded_url, endpage)
    # 儲存文章json至檔案位置
    filename = f'D:\\GitHub\\JLPT_VocabularyToDiscord\\scraper_file\\{level}_grammer.json'
    # print(f'URL:{encoded_url}   難度: {level}\n')
    save_articles_to_file(articles, filename, level)
