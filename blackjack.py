"""blackjack.py

"""

import random

class TextInterface:
    def __init__(self):
        print("Welcome to blackjack.")
        
    def setMoney(self, amt):
        pass
    

class CardDeck:
    """"""
    def __init__(self):
        """"""
        self.cards = range(1,14) + range(1,14) + range(1,14) + range(1,14)
        
    def draw(self):
        """"""
        if len(self.cards) == 0:
            self.refill()
        i = random.randrange(0, len(self.cards))
        c = self.cards.pop(i)
        return c
        
    def refill(self):
        """"""
        self.cards = range(1,14) + range(1,14) + range(1,14) + range(1,14)
        
    def cardsLeft(self):
        """"""
        return len(self.cards)
        
# dealer always treats ace as 1 point unless the hand is blackjack  
class Dealer:
    def __init__(self, d):
        self.hand = []
        self.deck = d
        
    def drawCard(self):
        aCard = self.deck.draw()
        self.hand.append(aCard)
        return aCard
            
    def turn(self):
        print("dealer's turn. dealer's hand is %d and %d" \
               % (self.hand[0], self.hand[1]))
        while self.getPoint() < 17:
            raw_input()
            a = self.drawCard()
            print("dealer drew: %d" % a)
        raw_input()
    
    def getPoint(self):
        if self.isBJack():
            return "blackjack"
        point = 0
        for i in self.hand:
            if i >= 10:
                point += 10
            else:
                point += i
        return point
        
    def isBJack(self):
        if len(self.hand) == 2:
            first, second = self.hand
            if first == 1 and second >= 10:
                return True
            elif second == 1 and first >= 10: 
                return True
            else:
                return False
        else:
            return False

# Player class        
class Player:
    # d is an input CardDeck object
    def __init__(self, d):
        self.hand = []
        self.deck = d
        
    def drawCard(self):
        aCard = self.deck.draw()
        self.hand.append(aCard)
        return aCard
    
    def turn(self):
        action = raw_input("player's turn. Hit or stand? Enter h or s: ")
        if action[0] in "hH":
            a = self.drawCard()
            print("player drew: %d" % a)
            if self.getPoint() > 21:
                print("The player busts")
            else:
                self.turn()
        elif action[0] in "sS":
            pass
        else:
            print("Invalid response")
            self.turn()
    
    def getPoint(self):
        if self.isBJack():
            return "blackjack"
        point = 0
        for i in self.hand:
            if i >= 10:
                point += 10
            else:
                point += i
        # treat one of the aces in hand as 11 if the resultant point < 22
        if min(self.hand) == 1 and point < 12:
            point += 10
        return point
        
    def isBJack(self):
        if len(self.hand) == 2:
            first, second = self.hand
            if first == 1 and second >= 10 and second <= 13:
                return True
            elif second == 1 and first >= 10 and first <= 13: 
                return True
            else:
                return False
        else:
            return False
        
class BJackApp:
    def __init__(self, interface):
        self.deck = CardDeck()
        self.dealer = Dealer(self.deck)
        self.player = Player(self.deck)
        self.interface = interface
        self.money = 10
        
    def run(self):
        while self.money >= 1 and self.interface.wantToPlay():
            self.playRound()
        self.interface.close()
    
    def playRound(self):
        self.money = self.money - self.interface.bet();
        self.interface.setMoney(self.money)
        self.deal()
        

        
    def deal(self):
        print("Deal***********")
        a = self.player.drawCard()
        print("player drew: %d" % a)
        a = self.player.drawCard()
        print("player drew: %d" % a)
        a = self.dealer.drawCard()
        print("\ndealer drew: %d" % a)
        a = self.dealer.drawCard()
        print("dealer drew: **\n")
        if self.dealer.isBJack() or self.player.isBJack():
            pass
        else:
            self.player.turn()
            if self.player.getPoint() > 21:
                pass
            else:
                self.dealer.turn()
        
        
    
    def getPoints(self):
        return self.dealer.getPoint(), self.player.getPoint() 

class HandleBets:
    def __init__(self):
        self.money = 10
        
    def update(self, aGame):
        dl, pl = aGame.getPoints()
        print("player's point: %s" % pl)
        print("dealer's point: %s" % dl)
        if dl > 21 and dl != "blackjack":
            dl = 0
        if pl > 21 and pl != "blackjack":
            pl = 0
        
        if dl == "blackjack" and pl == "blackjack":
            print("push")
        elif dl == "blackjack" and pl != "blackjack":
            print("lost")
            self.money -= 1
        elif dl != "blackjack" and pl == "blackjack":
            print("won")
            self.money += 1 
        elif dl >= pl:
            print("lost")
            self.money -= 1
        else:
            print("won")
            self.money += 1
            
    def printMoney(self):
        print("money: %d" % self.money)

def main():
    bets = HandleBets()
    theGame = BJackGame()
    while True:
        theGame.play()
        bets.update(theGame)
        bets.printMoney()
    
if __name__ == "__main__":
    main()
    raw_input("\Press <Enter> to quit")
