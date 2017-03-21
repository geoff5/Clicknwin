from ClickNWin import database
import random
import operator
"""Utility methods for creating scratch cards and helping their design"""
def newCards(cards):#Creates new cards, runs a cumulatitive probability algorithm to determine if they are winners and adds them to the database 
    prizes = database.getPrizes(cards['type'])
    chances  = {}
    chances[prizes[0][3]] = float(prizes[0][4])
    chances[prizes[0][5]] = float(prizes[0][6])
    chances[prizes[0][7]] = float(prizes[0][8])    
    chances[prizes[0][9]] = float(prizes[0][10])

    for i in range(0, int(cards['quantity'])):
        card = {}
        chance = random.uniform(0, 1)
        cumulative = 0.0
        prize = ""
        for k,v in sorted(chances.items(), key=operator.itemgetter(1)):
            cumulative += v
            print(k)
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
        


            
            
        

    
        