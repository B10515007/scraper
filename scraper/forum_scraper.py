import requests
import json
# from bs4 import BeautifulSoup
from scraper.base_scraper import BaseScraper

class ForumScraper(BaseScraper):
    """論壇爬蟲基類"""

    def scrape(self):
        pass

    def process_data(self, raw_data):
        """過濾廣告或整理留言"""
        return [item for item in raw_data if not item["title"].startswith("廣告")]

class DcardScraper(ForumScraper):
    """爬取 Dcard 熱門文章"""

    def scrape(self):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        resp = requests.get('https://www.dcard.tw/service/api/v2/posts?popular=false', headers)
        # json_resp = json.loads(resp.text)
        print(resp, resp.text)
        # with open('Dcard_articles.json', 'w', encoding='utf-8') as f:
        #     json.dump(json_resp, f, indent=2,
        #             sort_keys=True, ensure_ascii=False)

        # return self.process_data(raw_data)
