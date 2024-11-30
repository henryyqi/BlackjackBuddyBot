
class CheckForWin():

    def __init__(self):
        self.game_on = False
        self.player_bust_check = False
        self.player_blackjack = False
    
    def player_busts(self,chips):
        print("You have busted! You lost to the dealer!\n")
        chips.lose_bet()
        self.game_on = False
        self.player_bust_check = True
        return self.game_on

    def player_wins(self,chips):
        print("You won!\n")
        chips.win_bet()

    def dealer_busts(self,chips):
        print("The dealer busted! You won against the dealer!\n")
        chips.win_bet()

    def dealer_wins(self,chips):
        print("The dealer has won!\n")
        chips.lose_bet()

    def push(self):
        print("PUSH! The dealer and player tie!")

    
    
    