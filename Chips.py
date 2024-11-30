
class Chips():
        '''
        output: keeps track of the amount of chips the user has. adds or subtracts bet after playing.
        '''
        
        def __init__(self,total):
                self.total = total
                self.bet = 0
                print(f"You start with {total} chips.")

        def win_bet(self):
                self.total += self.bet
                
                
        def lose_bet(self):
                self.total -= self.bet

