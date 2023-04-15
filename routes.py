from queqe import Urls
from flask import request
from flask import jsonify
import time
import random
from config import TIME_SLEEP_CHECK_PREDICT, THREAD
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
def run(app, queqe_):
    @app.route("/predict", methods=["POST"])
    def predict():
        queqe = queqe_[random.randint(0,THREAD-1)]
        # print(f"du doan tren queqe {queqe.id}")
        # url = request.json.get("url", None)
        url = "https://www.youtube.com/" + str(random.randint(0,2000))
        # data = Urls.find_one({url: url})
        data = queqe.checkResult(url)
        if data:
            return jsonify(data['label']) 
        queqe.push(url)
        while True:
            time.sleep(TIME_SLEEP_CHECK_PREDICT)
            data = queqe.checkResult(url)
            if data:
                return jsonify(data['label']) 
    @app.route("/fakeRequeset")
    def fakeRequeset():
        start = time.time()
        for i in range(2000):
            predict()
        return jsonify(time.time()-start)
    @app.route("/testtime")
    def testtime():
        t_ = []
        start = time.time()
        for i in range(500):
            predict()
            t_.append(time.time()-start)
            start = time.time()
        x = np.array([i for i in range(len(t_))])
        t_ = np.array(t_)
        cubic_interpolation_model = interp1d(x, t_, kind = "cubic")
        X_=np.linspace(x.min(), x.max())
        Y_=cubic_interpolation_model(X_)

        plt.plot(X_,Y_)
        plt.savefig('test.png')
        plt.close()
        return 'done'