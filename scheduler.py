import asyncio
import threading
import schedule

from scraper.scraper_factory import ScraperFactory
from notifier.discord_notifier import DiscordBot

from queue import Queue
import time
import datetime

def scraper_591():
    scraper = ScraperFactory.get_scraper("rent_house", "591")
    data = scraper.scrape()
    return data

def run_scheduler():
    """負責執行排程（每 10 分鐘執行一次）"""
    schedule.every(10).minutes.do(lambda: asyncio.run(run_scrapers()))
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    message_queue = Queue()
    bot = DiscordBot(message_queue)
    bot.start_in_thread()
    
    # 方法1：等待直到準備就緒
    if bot.wait_until_ready(timeout=10):  # 最多等待30秒
        print("機器人已準備就緒！")
    else:
        print("機器人啟動超時！")
        return  
    
    # 主程式邏輯
    try:
        while True:
            # 確認機器人仍然在運行
            if not bot.is_ready():
                print("機器人已離線！")
                break
                
            print("主程式正在運行...")
            data = scraper_591()
            # print(data)  
            if data['left_nums'] != 0:
                discord_msg = bot.parse_rent591_message(data)
                bot.push_message(discord_msg)
            else:
                bot.push_message('沒找到新的')
                print('沒找到新的')               
            
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("程式正在關閉...")

if __name__ == "__main__":
    main()
