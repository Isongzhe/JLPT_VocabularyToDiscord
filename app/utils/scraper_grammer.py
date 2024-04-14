from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.edge.options import Options
import re
import time

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

    def process_elements(self, soup):
        rows = soup.find_all('div', {'class': 'ig13 row'})
        for row in rows:
            self.process_row(row)
        
        pics = soup.find_all(class_='pic bg-cover')
        for pic in pics:
            self.process_pic(pic)

    def process_row(self, row):
        # Find all a tags(usually are superlinks) in the row
        a_tags = row.find_all('a')
        for a_tag in a_tags:
            self.process_data(a_tag)

    def process_data(self, a_tag):
        # Get the href and title from the a tag
        href = a_tag.get('href')
        title = a_tag.get('title')

        if href and title:
            data = {'name': title, 'webURL': href}
            self.data.append(data)
        else:
            print('Error: No href or title found.')

    def process_pic(self, pic):
        style = pic.get('style')
        if not style:
            return print('Error: No style found.')
        
        # Use regular expression to find the image url (background-image:url(image.jpg))
        match = re.search(r"background-image:url\((.+?)\)", style)
        if not match:
            return print('Error: No match found.')
        
        # Get the image url from the style attribute 
        img_url = match.group(1) # get image.jpg
        for data in self.data:
            if 'imageURL' not in data:
                data['imageURL'] = img_url
                break

    def scrape_pages(self, level, url, end_page):
        print(f"現在正在讀取難度為{level}的網站\n網站的URL為:{url}")
        # 都從第一頁開始
        start_page=1
        for page in range(start_page, end_page + 1):
            web_url = f'{url}&page={page}'
            print(f'開始讀取第{page}頁....')
            self.scrape(web_url)
            print(f'結束讀取第{page}頁!')
            if self.data:
                print(f'第{page}頁最後一筆文章標題為: {self.data[-1]["name"]}')
            print('=' * 50)



    