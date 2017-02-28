from ClickNWin import database
import random
import operator

def newCards(cards):
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
        print(chance)
        print(card)
        database.addScratchCard(card)
            
            
        

    
        