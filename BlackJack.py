import random

#defining a class deck which can create a deck object which can be called. Each card object is defined as [value, suit]
class Deck:
    def __init__(self):
        self.cards=[[x,y] for x in [2,3,4,5,6,7,8,9,10,"ACE","KING","QUEEN","JOKER"] for y in ["HEART","SPADE","DIAMOND","CLUB"]]
        random.shuffle(self.cards)
    def deal(self, start=False):
        if start:
            return [self.cards.pop(),self.cards.pop()]
        else:
            return [self.cards.pop()]

#defining a Player object that will be used to initialize each player
class Player:
    def __init__(self, deck):
        self.hand=deck.deal(True)
    def is_busted(self):
        if score(self.hand)>21:
            return True
        return False

#defining a class for the dealer
class Dealer:
    def __init__(self,deck):
        self.hand=deck.deal(True)
        self.card_down=True
        self.upcard=self.hand[0]
        self.last_card=0
    def deal_dealer(self,deck):
        if score(self.hand)<=17:
            self.hand.extend(deck.deal())
            return 1
        self.last_card+=1
        return 0

#global functions
def score(hand):
    score=0
    for card in hand:
        if str(card[0]) in "QUEEN KING JOKER":
            score+=10
        elif str(card[0])== "ACE":
            score+=11
        else:
            score+=card[0]
    for card in hand:
        if str(card[0])=="ACE" and score>21:
            score-=10
    return score
