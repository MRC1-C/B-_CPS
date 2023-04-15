import time
import random
from pymongo import MongoClient
from multiprocessing import Process
from config import URL_DB, BATCH_SIZE, LEN_CACHE, TIME_SLEEP, TIME_MODEL, NUM_PROCESS

client = MongoClient(URL_DB)
db = client['cps']
Urls = db['urls']
print('connect DB')
class Queqe:
    def __init__(self, batch_size = BATCH_SIZE, len_cache = LEN_CACHE) -> None:
        self.batch_size = batch_size
        self.len_cache = len_cache
        self.queqe_ = []
        # load cache 
        print('load cache')
        cache = list(Urls.find({}))
        self.result = cache
        print('load thanh cong')
        self.id = -1
    def get(self):
        if len(self.queqe_) > self.batch_size:
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
        Urls.drop()
        Urls.insert_many(self.result)
        self.result = self.result[int(len(self.result)/2):]
    def checkResult(self, url):
        # print(self.result)
        if len(self.result) > 0:
            for i in self.result:
                if i['url'] == url:
                    return i
        else:
            return {}
    def models(self, t):
        time.sleep(t)
    def predict(self):
        i_ = 0
        while True:
            i_= i_+1
            if len(self.queqe_) > BATCH_SIZE:
                # print("BATCH_SIZE")
                i_ = 0
                data = self.get()
                self.models(TIME_MODEL)
                # for i in range(NUM_PROCESS):
                #     Process(target=self.models, args=(TIME_MODEL,)).start()
                #  Process(target=self.models, args=(TIME_MODEL,))
                for i in data:
                    self.result.append({"url": i, "label": random.randint(0,1)})
                if len(self.result) >= self.len_cache: 
                    self.save()
                    print('======================================')
                    print('luu thanh cong')
            else:
                if i_ > 10:
                    # print("NGHI")
                    # print(len(self.queqe_))
                    i_ = 0
                    if len(self.queqe_) > 0:
                        data = self.get()
                        # print("SAU NGHI")
                        self.models(TIME_MODEL)
                        for i in data:
                            self.result.append({"url": i, "label": random.randint(0,1)})
                        if len(self.result) >= self.len_cache: 
                            self.save()
                            print('======================================')
                            print('luu thanh cong')
            time.sleep(TIME_SLEEP)
        #qua model 
        #luu vao database 
        #  
    def run(self):
        print(f'khoi chay queqe {self.id}')
        self.predict()
# queqe = Queqe()