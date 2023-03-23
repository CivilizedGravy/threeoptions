from flask import Flask
import os
import random,string
app = Flask(__name__)
app.config.from_envvar('THREEOPTIONS_SETTINGS')
if app.secret_key == None:
    print('secret not set will use a random generated one')
    app.secret_key = os.urandom(24)
from . import route
