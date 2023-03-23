from flask import Flask
import os
import random,string
app = Flask(__name__)
app.secret_key = b'\xbd\rzl\x86dK#19\xa8_\xa4\xf9\xb2\xa2\xa1X\xd3\x01\xdc\x0f\tP'
from . import route
