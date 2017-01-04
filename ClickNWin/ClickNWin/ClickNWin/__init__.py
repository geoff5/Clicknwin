"""
The flask application package.
"""
from functools import wraps
from flask import Flask
app = Flask(__name__)
app.secret_key = 'fhdgsd;ohfnvervneroigerrenverbner32hrjegb/kjbvr/o'

def isLoggedIn(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'loggedIn' in session:
            return func(*args, **kwargs)
        return render_template('index.html', title='ClickNWin', year=datetime.now().year)
    return wrapped_function

import ClickNWin.views

