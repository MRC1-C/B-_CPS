import time
import random
from pymongo import MongoClient
from config import URL_DB, BATCH_SIZE, LEN_CACHE, TIME_SLEEP, TIME_MODEL

client = MongoClient(URL_DB)
db = client['cps']
Urls = db['urls']
print('connect DB')
class Queqe:
    def __init__(self, batch_size = BATCH_SIZE, len_cache = LEN_CACHE) -> None:
        self.batch_size = batch_size
        self.len_cache = len_cache
        self.queqe_ = []
        self.result = []
    def get(self):
        if(len(self.queqe_) > self.batch_size):
            data = self.queqe_[:self.batch_size]
            self.queqe_ = self.queqe_[self.batch_size:]
            return data
        else: 
            data = self.queqe_
            self.queqe_ = []
            return data
    def push(self, urls):
        self.queqe_.append(urls)
        self.queqe_ = list(set(self.queqe_)) 
    def save(self):
        Urls.insert_many(self.result)
        self.result = []
    def checkResult(self, url):
        # print(self.result)
        if len(self.result) > 0:
            for i in self.result:
                if i['url'] == url:
                    return i
        else:
            return {}
    def predict(self):
        data = self.get()
        if len(data) > 0:
            print('train model')
            time.sleep(TIME_MODEL)
            for i in data:
                self.result.append({"url": i, "label": random.randint(0,1)})
            if len(self.result) >= self.len_cache: 
                self.save()
                print('luu thanh cong')
        else:
            # print('nghi')
            time.sleep(TIME_SLEEP)
        self.run()
        #qua model 
        #luu vao database 
        #  
    def run(self):
        self.predict()
queqe = Queqe()