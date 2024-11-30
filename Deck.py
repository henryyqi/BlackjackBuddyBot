import random
from Card import Card
    
suits = ('♥', '♦', '♠', '♣')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10,
         'Q':10, 'K':10, 'A':11}

class Deck():
    '''
    output: creates a deck of 52 cards. shuffles the deck afterwards. can deal one card by popping out from deck.
    '''
    def __init__(self):
        # empty list to place the created cards
        self.deck = []
        
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                    
                # append the created card into the list (create the card obj)
                self.deck.append(created_card)

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal_card(self):
        return self.deck.pop()

    def __str__(self):
        for card in self.deck:
            return print(card)