from queqe import Urls
from flask import request
from flask import jsonify
import time
import random
from config import TIME_SLEEP_CHECK_PREDICT

def run(app, queqe):
    @app.route("/predict", methods=["POST"])
    def predict():
        # url = request.json.get("url", None)
        url = "https://www.youtube.com/" + str(random.randint(0,100))
        # data = Urls.find_one({url: url})
        data = queqe.checkResult(url)
        if data:
            return jsonify(data['label']) 
        else:
            queqe.push(url)
            while True:
                time.sleep(TIME_SLEEP_CHECK_PREDICT)
                data = queqe.checkResult(url)
                if bool(data):
                    return jsonify(data['label']) 
                data_ = Urls.find_one({url: url})
                if data_:
                    return jsonify(data_['label']) 
    @app.route("/fakeRequeset")
    def fakeRequeset():
        start = time.time()
        for i in range(2000):
            predict()
        return jsonify(time.time()-start)