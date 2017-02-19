from ClickNWin import database

def newCards(cardNo, user, type):
    prizes = database.getPrizes(type)
    print(prizes)