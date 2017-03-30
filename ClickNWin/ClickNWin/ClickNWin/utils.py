from ClickNWin import database, paypalAPI
import random
import operator
"""Utility methods for creating scratch cards and creating panels for their design"""
def newCards(cards):#Creates new cards, runs a cumulatitive probability algorithm to determine if they are winners and adds them to the database 
    prizes = database.getPrizes(cards['type'])
    chances  = {}
    chances[prizes[0][2]] = float(prizes[0][3])
    chances[prizes[0][4]] = float(prizes[0][5])
    chances[prizes[0][6]] = float(prizes[0][7])    
    chances[prizes[0][8]] = float(prizes[0][9])

    for i in range(0, int(cards['quantity'])):
        card = {}
        chance = random.uniform(0, 1)
        cumulative = 0.0
        prize = ""
        for k,v in sorted(chances.items(), key=operator.itemgetter(1)):
            cumulative += v
            if chance < cumulative:
                prize = k
                break
        card['prize'] = prize
        card['user'] = cards['user']
        card['boughtBy'] = cards['boughtBy']
        card['type'] = cards['type']
        card['boughtOn'] = cards['boughtOn']
        database.addScratchCard(card)


def createPanelArray(card):#creates a list of prizes to be displayed on the card based on whether the card is a winner or not
    panels = []
    prizes = card[2:]
    while len(panels) < 6:
        if card[1] and card[1] not in panels:
            for i in range(0, 3):
                panels.append(card[1])
        pick = random.randint(2,5)
        if panels.count(card[pick]) < 2:
            panels.append(card[pick])
    return panels
        
def formatCurrency(amount):#formats the given number to look like a currency value
    point = False
    count = -1
    if amount[0] == '.':
        amount = '0' + amount
        for c in amount:
            if c == '.':
                point = True
            if point:
                count = count + 1
        if count == 1:
            amount = amount + '0'
    return amount

def processCardPayment(user, cardID, amount, cvv):#processes paypal payments using stored credit cards
    card = database.getPaymentCard(int(cardID))
    card  = card[0]
    amount = formatCurrency(amount)
    paymentSuccess = paypalAPI.topUp(card, amount, cvv)
    if paymentSuccess:
        database.addFunds(user, amount)
        data = {}
        data['user'] = user
        data['amount'] = amount
        data['cardNo'] = card[1][12:]
        return data
    else:
        return False
            
def processPaypalPayment(user, amount):#processes paypal payments made through the paypal store
    amount = formatCurrency(amount)
    data = paypalAPI.pay(amount)
    if data:
        return data
    else:
        return False