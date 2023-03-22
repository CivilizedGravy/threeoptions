from flask import Flask
import random,string
app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
from . import route
