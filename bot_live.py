from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Hello, AlchemyBot is Live Now! Have fun on Discord Server."

def run():
  app.run(host = '0.0.0.0', port = 1024)

def alive():
  b = Thread(target = run)
  b.start()