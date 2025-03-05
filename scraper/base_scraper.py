from abc import ABC, abstractmethod

class BaseScraper(ABC):
    """所有爬蟲的基礎類別"""

    def __init__(self, site_name):
        self.site_name = site_name  # 爬取的網站名稱

    @abstractmethod
    def scrape(self):
        """爬取資料的方法，所有爬蟲必須實作"""
        pass

    @abstractmethod
    def process_data(self, raw_data):
        """後處理數據的方法，讓不同類型的爬蟲有自己的處理邏輯"""
        pass
