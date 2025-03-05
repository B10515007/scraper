import requests
import os
from bs4 import BeautifulSoup
from scraper.base_scraper import BaseScraper

class RentHouseScraper(BaseScraper):
    """租屋爬蟲基類"""

    def scrape(self):
        """子類別應該實作不同網站的爬取邏輯"""
        pass

    def process_data(self, raw_data):
        """統一的數據處理方式，例如轉換價格格式"""
        processed_data = []
        for item in raw_data:
            price = item.get("price", "0").replace(",", "")  # 移除千位符號
            item["price"] = int(price)
            processed_data.append(item)
        return processed_data


class Scraper591(RentHouseScraper):
    """爬取 591 租屋網"""

    def post_process(self, data):
        id_path = './rent_house/591_id.txt'
        os.makedirs("./rent_house", exist_ok=True)
        exist_id = set()
        if os.path.isfile(id_path):
            with open(id_path,"r",  encoding="utf-8") as f:
                for line in f.readlines():
                    exist_id.add(line.strip())
        newFound = {'total':data['total'], 'left_nums':0, 'rooms': []}

        for room in data['rooms']:
            id = room[1].split('/')[-1]
            if id in exist_id:
                continue
            roomInfo = {'id':id, 'title':room[0], 'link':room[1], 'type':room[2]}
            newFound['rooms'].append(roomInfo)
            exist_id.add(id)

        newFound['left_nums'] = len(newFound['rooms'])
        print('過濾後剩下:' + str(len(newFound['rooms'])) + '間')

        # Update new id to the file. 
        with open(id_path, "w",  encoding="utf-8") as f:
            for id in exist_id:
                f.write(id+'\n')
        
        return newFound

    def scraping(self, params):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Referer": "https://rent.591.com.tw/",
        }
        data = {'total':0, 'rooms':[]} 
        for params in params:
            page = 1
            while True:
                url = 'https://rent.591.com.tw/list?region={}&section={}'\
                      '&price={}&layout={}&notice={}&page={}'.format(params['region'],
                                                           params['section'],
                                                           params['price'],
                                                           params['layout'],
                                                           params['notice'],
                                                           page)
                response = requests.get(url, headers=headers)

                if response.status_code == 200:  
                    soup = BeautifulSoup(response.content, "html.parser")
                    titles = soup.select("a.link.v-middle")
                    rooms = soup.find_all('div', class_='item-info')
                    num_of_room = len(rooms)
                    print("第"+ str(page)+"頁，總共找到:" + str(num_of_room) + '間')
                    roomList = []
                    for room in rooms:
                        roomInfo = []
                        roomInfo.append(room.find('a', class_="link v-middle")['title'])
                        roomInfo.append(room.find('a', class_="link v-middle")['href'])
                        # room type, like 2房1廳
                        roomInfo.append(room.find('span', class_="line").get_text())
                        roomList.append(roomInfo)
                    
                    data['total'] += num_of_room
                    data['rooms'].extend(roomList)
                    page += 1
                    # one page max room is 30
                    if num_of_room < 30:
                        break
                        
                else:
                    print("請求失敗，可能被封鎖", response.status_code)
                    break

        result = self.post_process(data)
        return result
    
    def scrape(self):       
        params = [{
                    "region": 3,   # 1: 台北市
                    "section": "27",  # 10:內湖區 11: 南港區
                    "layout": "4",
                    "notice": "not_cover",
                    "price": "10000_20000"
                 }]
        
        # params = [{
        #             "region": 3,   # 1: 台北市
        #             "section": "27",  # 10:內湖區 11: 南港區
        #             "layout": 4,
        #             "price": '10000_20000,20000_30000'
        #          },
        #          {
        #             "region": 1,   # 1: 台北市
        #             "section": '10,11',  # 10:內湖區 11: 南港區
        #             "layout": 1,
        #             "price": '10000_20000,20000_30000'
        #          }]

        result = self.scraping(params)

        return result
