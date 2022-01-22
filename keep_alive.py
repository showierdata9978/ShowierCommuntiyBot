
from flask import Flask,render_template,request
from threading import Thread
import random


app = Flask('__name__',template_folder='site')

@app.route('/bot/status')
def status():
	return 'Im in'
@app.route('/bot/status/api/logs')
def BotLogs():
	with open('logs/all.log','r') as l:
		return list(l.readlines()) 
		
	
def run():
  app.run(
		host='0.0.0.0',
		port=5050
	)

def keep_alive():
	'''
	Creates and starts new thread that runs the function run.
	'''
	t = Thread(target=run)
	t.start()
