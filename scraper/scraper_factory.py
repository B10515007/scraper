from scraper.rent_house_scraper import Scraper591
from scraper.forum_scraper import DcardScraper
# from scraper.stock_scraper import YahooFinanceScraper

class ScraperFactory:
    """爬蟲工廠，負責選擇正確的爬蟲"""

    @staticmethod
    def get_scraper(category, site_name):
        scrapers = {
            "rent_house": {"591": Scraper591},
            "forum": {"dcard": DcardScraper},
            # "stock": {"yahoo": YahooFinanceScraper},
        }
        if category in scrapers and site_name in scrapers[category]:
            return scrapers[category][site_name](site_name)
        else:
            raise ValueError(f"❌ 未知的爬蟲類型或網站: {category}/{site_name}")
