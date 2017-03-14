"""
The flask application package.
"""
from functools import wraps
from flask import Flask
from flask_sslify import SSLify

app = Flask(__name__)
#sslify = SSLify(app)
app.secret_key = 'ThisIsMySecretKeyForMyProject'


import ClickNWin.views
import ClickNWin.api

