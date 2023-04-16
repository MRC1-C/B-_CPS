import time
import random
from pymongo import MongoClient
from multiprocessing import Process, Queue as Q
from config import URL_DB, BATCH_SIZE, LEN_CACHE, TIME_SLEEP, TIME_MODEL, NUM_PROCESS
from preprocess import process_urls, get_predict

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
        self.result = cache[int(len_cache/2):]
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
    def models(self):
        if len(self.queqe_) > BATCH_SIZE*5:
            start = time.time()
            data = self.queqe_
            self.queqe_ = []
            score1 = Q()
            score2 = Q()
            p1 = Process(target=self.modelsEmergency, args=(data[:int(len(data)/2)],score1))
            p2 = Process(target=self.modelsEmergency, args=(data[int(len(data)/2):],score2))
            p1.start()
            p2.start()
            p1.join()
            p2.join()
            score = list(score1.get()) + list(score2.get())
            for i in range(len(data)):
                self.result.append({"url": data[i], "label": score[i][0]})
            print("sau 2 tien trinh ===========",time.time()-start)
            # for i in range(NUM_PROCESS):
            #     Process(target=self.modelsEmergency, args=(data[i:i],)).start()
        else:  
            data = self.get()
            res = process_urls(data)
            score = get_predict(res)
            # print(score)
            for i in range(len(data)):
                self.result.append({"url": data[i], "label": score[i][0]})
    def modelsEmergency(self, data, score):
        start = time.time()
        res = process_urls(data)
        score_ = get_predict(res)
        score.put(score_)
        print("Tien trinh con",time.time() - start)
        # for i in range(len(data)):
        #     self.result.append({"url": data[i], "label": score[i][0]})
        #     print(len(self.result))
        # print(score)
        # for i in range(len(data)):
        #     self.result.append({"url": data[i], "label": score[i][0]})
        #     print(len(self.result))
    def predict(self):
        i_ = 0
        while True:
            # print(len(self.queqe_))
            i_= i_+1
            if len(self.queqe_) > BATCH_SIZE:
                # print("BATCH_SIZE")
                i_ = 0
                self.models()
                # for i in range(NUM_PROCESS):
                #     Process(target=self.models, args=(TIME_MODEL,)).start()
                # if len(self.queqe_) < 5*BATCH_SIZE:
                #     self.models()
                # else:
                #     for i in range(NUM_PROCESS):
                #         Process(target=self.models).start()

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
                        self.models()
                        if len(self.result) >= self.len_cache: 
                            self.save()
                            print('======================================')
                            print('luu thanh cong')
                else:
                    time.sleep(TIME_SLEEP)
        #qua model 
        #luu vao database 
        #  
    def run(self):
        print(f'khoi chay queqe {self.id}')
        self.predict()
# queqe = Queqe()