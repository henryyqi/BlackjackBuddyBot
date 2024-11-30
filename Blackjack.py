
from CheckForWin import CheckForWin

CFW = CheckForWin()

class Blackjack():
    '''
    basic functions of blackjack game
    '''

    def __init__(self):
        self.choice = ''
    
    def play_blackjack(self):
        print("Welcome to Blackjack! Let's begin!")
        

    def take_bet(self,player_chips):
        
        print(f'You have {player_chips.total} chips.')
        
        while True:   
            try:
                player_chips.bet = int(input("Please enter your bet: "))
            except:
                print("Enter again!")
                continue
            if player_chips.bet <= player_chips.total:
                break
            else:
                print(f"Insufficient chips! You have: {player_chips.total}")
        
        print(f"You bet {player_chips.bet} chips.\n")
        
    def hit(self,deck,player_hand):
        # the hit (adding card to the hand)
        player_hand.add_card(deck.deal_card())
        
        if player_hand.hand_value > 21:
            player_hand.adjust_for_aces()
        
        # if player_hand.hand_value > 21:
        #     # bust!
        #     print("Bust! The total value is {}".format(player_hand.hand_value))
            
    def hit_or_stand(self,deck,player_hand,dealer_hand):
        
        while True:
            self.show_some(player_hand,dealer_hand)
            if player_hand.hand_value >= 21:
                break
            self.choice = input("Would you like to hit or stand? (h/s)")
            if self.choice[0].lower() == "h":
                self.hit(deck,player_hand)
                
            elif self.choice[0].lower() == 's':
                break
            else:
                print("Sorry I did not understand. Try again.")
                continue
            
    def show_some(self,player_hand,dealer_hand):
        print(f"Dealer:\t {dealer_hand.cards[0]} and [?]")
        
        print("\nPlayer:\t")
        for num in range(0,len(player_hand.cards)):
            print(player_hand.cards[num])
        print("Value: {}".format(player_hand.hand_value))
        
        print("---------------------------------")
        
    def show_all(self,player_hand,dealer_hand):
        print("\nDealer:\t")
        for num in range(0,len(dealer_hand.cards)):
            print(dealer_hand.cards[num])
        print("Value: {}".format(dealer_hand.hand_value))
        
        print("\nPlayer:\t")
        for num in range(0,len(player_hand.cards)):
            print(player_hand.cards[num])
        print("Value: {}".format(player_hand.hand_value))
        
        print("---------------------------------")
        
        # Another way to display items: 
        # items = [1,2,3]
        # print("Items are: ",*items,sep='\n')

    

