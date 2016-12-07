"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from ClickNWin import app

@app.route('/')
@app.route('/home', methods=['POST'])
def home():
    return render_template('index.html', title='ClickNWin', year=datetime.now().year)

@app.route('/register')
def register():
    return render_template('register.html', title='ClickNWin', year = datetime.now().year)