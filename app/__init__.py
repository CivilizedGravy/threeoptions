from flask import Flask
import json
app = Flask(__name__)
with open('/etc/config.json') as config_file:
  config = json.load(config_file)
app.config['SECRET_KEY'] = config.get('SECRET_KEY')
from flask_app import route
