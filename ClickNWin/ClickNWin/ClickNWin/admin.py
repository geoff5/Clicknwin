"""Routes and views for admin functions"""

from datetime import datetime
from functools import wraps
from flask import render_template, session, request, redirect, flash
from ClickNWin import app, database

def isAdmin(func):#decorator to ensure only logged in admins can access admin pages
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'isAdmin' in session:
            return func(*args, **kwargs)
        return redirect('/adminLogin')
    return wrapped_function


@app.route('/adminLogin')
def adminLogin():
    return render_template('adminLogin.html', title="ClickNWin")

@app.route('/adminLoggedIn', methods=['POST'])
def adminLoggedIn():
    admin = {}
    admin['user'] = request.form['username']
    admin['password'] = request.form['password']
    success = database.adminLogin(admin)
    if success:
        session['isAdmin'] = True
        session['admin'] = admin['user']
        return redirect('adminHome')
    flash("Username or password is incorrect.  Please try again")
    return redirect('/adminLogin')  

@app.route('/adminLogout', methods=['GET'])
def logout():
    session.pop('isAdmin')
    session.pop('admin')
    return redirect('/adminLogin')

@app.route('/adminHome')
@isAdmin
def adminHome():
    return render_template('adminHome.html', title='ClickNWin')  

@app.route('/addAdmin', methods=['GET'])
@isAdmin
def addAdmin():
    return render_template('addAdmin.html', title='ClickNWin')

@app.route('/adminAdded', methods=['POST'])
@isAdmin
def adminAdded():
    admin = {}
    admin['username'] = request.form['username']
    admin['password'] = request.form['password']
    database.addAdmin(admin)
    return redirect('/adminHome')

@app.route('/addNewGame', methods=['GET'])
@isAdmin
def addNewGame():
    return render_template('addNewGame.html', title='ClickNWin')

@app.route('/newGameAdded', methods=['POST'])
@isAdmin
def newGameAdded():
    gameName = request.form['gameName']
    newGame = {'gameName':'', 'gamePrice':'', 'prize1':'', 'prize1Chance':'', 'prize2':'', 'prize2Chance':'', 'prize3':'', 'prize3Chance':'', 'prize4':'', 'prize4Chance':'', 'noWin':''}
    for k,v in request.form.items():
        newGame[k] = request.form[k]
    database.addCardType(newGame)
    flash("New Game " + gameName + " successfuly added")
    return redirect('/adminHome')

@app.route('/changeGame', methods=['GET'])
@isAdmin
def changeGame():
    games = database.getCardTypes()
    return render_template('changeGame.html', title='ClickNWin', games=games)

@app.route('/gameChanged', methods=['POST'])
@isAdmin
def gameChanged():
    gameName = request.form['gameName']
    changeGame = {'gameName':'', 'gamePrice':'', 'prize1':'', 'prize1Chance':'', 'prize2':'', 'prize2Chance':'', 'prize3':'', 'prize3Chance':'', 'prize4':'', 'prize4Chance':'', 'noWin':''}
    for k,v in request.form.items():
       changeGame[k] = request.form[k]
    database.modifyGame(changeGame)
    flash("Game " + gameName + " has been successfuly modified")
    return redirect('/adminHome')    