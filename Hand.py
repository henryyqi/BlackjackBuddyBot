
suits = ('♥', '♦', '♠', '♣')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10,
         'Q':10, 'K':10, 'A':11}

class Hand():

        def __init__(self):
                # empty list in your hand to start with
                self.cards = []         # list of cards in that hand
                self.hand_value = 0     # start with 0 value
                self.aces = 0           # attribute to keep track of aces
                
        def add_card(self, card):
                # from Deck.deal() --> single Card(suit,rank)
                self.cards.append(card)          # adds the dealt card into the list
                self.hand_value += card.value    # adds card's value to the hand
                # from solutions: self.value += values[card.rank]
                if card.rank == "A":           # check if dealt card is an Ace
                        self.aces += 1
        
        def adjust_for_aces(self):
                while self.hand_value > 21 and self.aces:
                        self.hand_value -= 10
                        self.aces -= 1
                
        # test_player.add_card(tset_deck.deal())



