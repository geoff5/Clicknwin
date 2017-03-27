from datetime import datetime
from functools import wraps
from flask import render_template, session, request, redirect, json, jsonify
from ClickNWin import app, database, utils, views, paypalAPI
"""AJAX API calls for the Flask Application"""


@app.route('/getCard', methods=['POST'])
def getCard():
    id = request.form['id']
    card = database.getCard(id)
    prizes = database.getCardPrizes(card[0])
    cardInfo = card + list(prizes[0])
    panels = utils.createPanelArray(cardInfo) 
    return jsonify(card = panels)

@app.route('/checkUser', methods=['POST'])
def checkUser():
    user = request.form['user']
    exists = database.checkUsername(user)
    return jsonify(exists=exists)

@app.route('/getCardPrice', methods=['POST'])
def getCardPrice():
    type = request.form['type']
    price = database.getPrice(type)
    return jsonify(price=price)

@app.route('/cardRedeemed', methods=['POST'])
def cardRedeemed():
    id = request.form['id']
    card = database.getCard(id)
    prize = card[1]
    database.redeemCard(id)
    if prize:
        database.addFunds(session['user'], prize)
    return jsonify(prize = prize)

@app.route('/checkAdmin', methods=['POST'])
def checkAdmin():
    user = request.form['user']
    exists = database.checkAdmin(user)
    print(exists)
    return jsonify(exists=exists)

@app.route('/getCardType', methods=['POST'])
def getCardType():
    id = request.form['id']
    cardType = database.getCard(id)
    return jsonify(cardType = cardType[0])

@app.route('/checkGame', methods=['POST'])
def checkGame():    
    exists = False
    game = request.form['game']
    games = database.getCardTypes()
    print(game)
    print(games)
    for i in games:
        if game.lower() == i[0].lower():
            exists = True
    return jsonify(exists=exists)

@app.route('/getGame', methods=['POST'])
def getGame():
    game = request.form['game']
    data = database.getPrizes(game)
    cardData = data[0]
    return jsonify(data=cardData)