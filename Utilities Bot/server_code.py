#Use link from Webview and sync to hosting software of your choice
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Hello! Utilities Testing is operational."

def run():
  app.run(host='0.0.0.0',port=8080)

def server_code():
  t = Thread(target=run)
  t.start()