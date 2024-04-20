from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.edge.options import Options
import logging
import time
import json

# 創建一個日誌器
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # 或者任何你想要的級別

# 創建一個文件處理器
handler = logging.FileHandler('logfile.log')  # 將日誌訊息寫入 'logfile.log' 文件
handler.setLevel(logging.INFO)  # 或者任何你想要的級別

# 創建一個格式器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 創建一個流處理器
stream_handler = logging.StreamHandler()

# 為流處理器設置格式器
stream_handler.setFormatter(formatter)

# 為日誌器添加流處理器
logger.addHandler(stream_handler)

class WebDriver:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--enable-features=SameSiteByDefaultCookies")
        options.add_argument("--log-level=3")
        self.driver = webdriver.Edge(options=options)

    def get_page(self, url):
        self.driver.get(url)
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def quit(self):
        self.driver.quit()

class Scraper:
    def __init__(self, driver):
        self.driver = driver
        self.data = []

    def scrape(self, url):
        soup = self.driver.get_page(url)
        time.sleep(5)
        self.process_elements(soup)

class ScraperNews(Scraper):
    def process_data(self, a_tag, date=None):
        logging.info("正在處理新聞資訊")
        href = self.get_href(a_tag)
        img_src = self.get_img_src(a_tag)
        title = self.get_title(a_tag)
        source, time = self.get_source_and_time(a_tag)

        if href and img_src and title and source and time:
            data = {
                'name': title,
                'webURL': href,
                'imgURL': img_src,
                'source': source,
                'time': time
            }
            self.data.append(data)
            logging.info("成功添加新聞資訊")
        else:
            logging.error('缺少數據: href=%s, img_src=%s, title=%s, source=%s, time=%s', href, img_src, title, source, time)
    
    def get_href(self, a_tag):
        href = a_tag.get('href')
        if href is None:
            logging.error('找不到 href')
        return href

    def get_img_src(self, a_tag):
        img_tag = a_tag.find('img', {'class': 'img-news lazy'})
        img_src = img_tag.get('src') if img_tag else None
        if img_src is None:
            logging.error('找不到 img_src')
        return img_src

    def get_title(self, a_tag):
        title_div = a_tag.find('div', {'class': 'recent-title'})
        title = title_div.get_text() if title_div else None
        if title is None:
            logging.error('找不到 title')
        return title
    
    def get_source_and_time(self, a_tag):
        time_up_div = a_tag.find('div', {'class': 'time-up'})
        if time_up_div:
            spans = time_up_div.find_all('span')
            if len(spans) >= 2:
                source_span, time_span = spans[:2]
                source = source_span.get_text().replace('資源: ', '') if source_span else None
                time = time_span.get_text() if time_span else None
                return source, time
        logging.error('找不到 time_up_div')
        return None, None
        
    def compare_date(self, soup, date):
        # 獲取 "nav-link active" 的 a 標籤
        nav_link_active_a = soup.find('a', {'class': 'nav-link active'})

        # 如果找不到 "nav-link active" 的 a 標籤，則返回 False
        if not nav_link_active_a:
            logging.info('找不到 "nav-link active" 的 a 標籤')
            return False

        # 從 "nav-link active" 的 a 標籤中獲取 span
        nav_link_active_span = nav_link_active_a.find('span')
        nav_link_active_date = nav_link_active_span.get_text() if nav_link_active_span else None

        # 比較日期
        if date and nav_link_active_date != date:
            logging.info('日期不匹配: %s != %s', nav_link_active_date, date)
            return False

        return True
    
    def scrape_date_page(self, date, difficulty, url):
        logging.info(f"現在正在讀取難度為{difficulty}的網站\n網站的URL為:{url}")
        soup = self.driver.get_page(url)
        logging.info("已經成功獲取網頁內容")
        time.sleep(5)

        # 先確認日期是否正確
        if not self.compare_date(soup, date):
            logging.error(f"頁面日期不匹配，期望的日期是 {date}")
            raise ValueError(f"頁面日期不匹配，期望的日期是 {date}")

        a_tags = soup.find_all('a', {'class': 'item-recent'})
        logging.info(f"找到了 {len(a_tags)} 個 'item-recent' 標籤")
        for a_tag in a_tags:
            self.process_data(a_tag, date)
            if self.data:
                logging.info(f'新聞標題: {self.data[-1]["name"]}')
            else:
                logging.info("未能成功處理新聞資訊")

    def save_data_to_json(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

difficulty = 'easy'  # 或 'normal'
news_url = f'https://easyjapanese.net/news/{difficulty}/all?hl=zh-TW'

if __name__ == "__main__":
    driver = WebDriver()
    scraper = ScraperNews(driver)
    scraper.scrape_date_page("Apr 18", "easy", news_url)  # 假設您想要爬取特定日期的新聞
    scraper.save_data_to_json(r'./EasyJapan_news.json')
    driver.quit()