from flask import Flask
# from mongo import setupDB
from threading import Thread
from routes import run
from queqe import Queqe
from flask_cors import CORS
from config import THREAD
app = Flask(__name__)
CORS(app)
queqe = []
t = []
for i in range(THREAD):
	q = Queqe()
	q.id = i
	queqe.append(q)
# setupDB()
try:
	t1 = Thread(target=run, args=(app, queqe))
	for i in range(THREAD):
		try:
			Thread(target=queqe[i].run).start()
		except:
			print('err')
	t1.start()
	# for i in range(THREAD):
	# 	t[i].start()
except:
	print ("error")


# check
# predict 
# predict 
# get  