from datetime import datetime
from functools import wraps
from flask import render_template, session, request, redirect, json, jsonify
from ClickNWin import app, database, cards,views

def isLoggedIn(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'isLoggedIn' in session:
            return func(*args, **kwargs)
        return redirect('/home')
    return wrapped_function


@app.route('/getCard', methods=['POST'])
@isLoggedIn
def getCard():
    id = request.form['id']
    card = database.getCard(id)
    prizes = database.getCardPrizes(card[0][0])
    cardInfo = card[0] + prizes[0]
    panels = cards.createPanelArray(cardInfo) 
    return jsonify(card = panels)

@app.route('/checkUser', methods=['POST', 'GET'])
@isLoggedIn
def checkUser():
    user = request.form['user']
    exists = database.checkUsername(user)
    return jsonify(exists=exists)

@app.route('/getCardPrice', methods=['POST'])
@isLoggedIn
def getCardPrice():
    type = request.form['type']
    price = database.getPrice(type)
    return jsonify(price=price)

@app.route('/cardRedeemed', methods=['POST'])
@isLoggedIn
def cardRedeemed():
    id = request.form['id']
    card = database.getCard(id)
    prize = card[0][1]
    database.redeemCard(id)
    database.addFunds(session['user'], prize)
    return jsonify(prize = prize)
