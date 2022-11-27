from flask import Flask
import logging

app = Flask(__name__)


app.secret_key = "I Love Burritos"


logging.basicConfig(filename='record.log', level=logging.ERROR)
