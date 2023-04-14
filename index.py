from flask import Flask
# from mongo import setupDB
from threading import Thread
import threading
from routes import run
from queqe import queqe
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# setupDB()
try:
	t1 = threading.Thread(target=run, args=(app, queqe))
	t2 = threading.Thread(target=queqe.run)
	t2.start() 
	t1.start()
except:
	print ("error")


# check
# predict 
# predict 
# get  