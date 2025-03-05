import discord
import asyncio
import configparser
import os

from threading import Thread, Event
from queue import Queue

class DiscordBot:
    def __init__(self, aMessage_queue):
        config = configparser.ConfigParser()
        # 獲取當前 Python 檔案所在的資料夾
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config.read(script_dir+'/config.ini')

        # print(config['Discord'].section())
        self.mToken = config['Discord']['Toekn']
        self.mChannelId = int(config['Discord']['Rent_House_Channel'])
        # 啟用 Bot
        intents = discord.Intents.default()
        self.mClient = discord.Client(intents=intents)
        self.mMessage_queue = aMessage_queue
        self.mReady_event = Event()  # 用於追蹤 ready 狀態

        self.setup_events()
    
    def setup_events(self):
        @self.mClient.event
        async def on_ready():
            print(f'Bot logged in as {self.mClient.user}')
            self.mChannel = self.mClient.get_channel(self.mChannelId)
            self.mReady_event.set()  # 設置 ready 狀態
            self.mClient.loop.create_task(self.check_queue())

    async def check_queue(self):
        while True:
            try:
                if not self.mMessage_queue.empty():
                    message = self.mMessage_queue.get_nowait()
                    if self.mChannel:
                        await self.mChannel.send(message)
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Error in check_queue: {e}")
                await asyncio.sleep(1)

    def run_bot(self):
        print('run_bot')
        self.mClient.run(self.mToken)
    
    def start_in_thread(self):
        self.mBot_thread = Thread(target=self.run_bot, daemon=True)
        self.mBot_thread.start()
        
    def wait_until_ready(self, timeout=None):
        """等待直到機器人準備就緒"""
        return self.mReady_event.wait(timeout=timeout)
    
    def is_ready(self):
        """檢查機器人是否準備就緒"""
        return self.mReady_event.is_set()
    
    def push_message(self, mes):
        self.mMessage_queue.put(mes)

    def parse_rent591_message(self, data):
        msg = '# 總共發現 {} 間新房間\n\n'.format(data['left_nums'])
        for room in data['rooms']:
            msg += '## {}\n- 連結: {}\n- 房型: {}\n'.format(room['title'], room['link'], room['type'])
        return msg
