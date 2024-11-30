# import bot
import robot
from Blackjack import Blackjack
from CheckForWin import CheckForWin

BJ = Blackjack()
CFW = CheckForWin()

# from IPython.display import clear_output

suits = ('♥', '♦', '♠', '♣')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10,
         'Q':10, 'K':10, 'A':11}

# game_on = True

if __name__ == '__main__':
    # bot.run_discord_bot()
    robot.run_discord_bot()

rounds = 0

    # while CFW.game_on is True:

    # rounds += 1
    # # clear_output()
    # print("Welcome to Blackjack! Let's begin!")

    # # create a new, shuffled deck
    # deck_of_cards = Deck()
    # deck_of_cards.shuffle()

    # # initializes the player's chips and takes a bet
    # if rounds == 1:
    #     player_chips = Chips(100)
    # else:
    #     player_chips = player_chips.total

    # BJ.take_bet(player_chips)
    # CFW.game_on = True
    # CFW.player_bust_check = False

    # # deal two cards to player, two cards to dealer
    # player_hand = Hand()
    # dealer_hand = Hand()

    # player_hand.add_card(deck_of_cards.deal_card())
    # dealer_hand.add_card(deck_of_cards.deal_card())
    # player_hand.add_card(deck_of_cards.deal_card())
    # dealer_hand.add_card(deck_of_cards.deal_card())

    # BJ.show_some(player_hand,dealer_hand)

    # # player is playing their hand
    # while CFW.game_on:
        
    #     # ask user for hit or stand. executes hit if choice is hit.
    #     BJ.hit_or_stand(deck_of_cards,player_hand)
        
    #     if player_hand.hand_value > 21:
    #         CFW.game_on = CFW.player_busts(player_chips)
        
    #     # show cards (including new card added)
    #     BJ.show_some(player_hand,dealer_hand)
        
        
    # # if the player is standing and has not busted, it is the dealer's turn
    # # play until dealer reaches 17
    # if CFW.player_bust_check is False:
    #     print("The dealer's turn.")
    #     while dealer_hand.hand_value < 17:
    #         BJ.hit(deck_of_cards,dealer_hand)

    # # playing is over, time to compare diff winning scenarios
    # print("GAME OVER! The cards are now revealed: ")
    # BJ.show_all(player_hand,dealer_hand)

    # # dealer busts
    # if dealer_hand.hand_value > 21:
    #     CFW.dealer_busts(player_chips)

    # # player wins/dealer wins
    # if CFW.player_bust_check is False and player_hand.hand_value > dealer_hand.hand_value:
    #     CFW.player_wins(player_chips)
    # elif CFW.player_bust_check is False and player_hand.hand_value < dealer_hand.hand_value and dealer_hand.hand_value <= 21:
    #     CFW.dealer_wins(player_chips)
    # elif CFW.player_bust_check is False and player_hand.hand_value == dealer_hand.hand_value:
    #     CFW.push()

    # # chip count
    # print("Chips total: {}".format(player_chips.total))

    # if player_chips.total == 0:
    #     print("You are out of chips! Better luck next time!")
    #     break

    # # ask to play again
    # replay = input("Play again? (y/n)")
    # if replay[0].lower() == 'y':
    #     CFW.game_on = True
    #     continue
    # else:
    #     print("Thanks for playing!")
    #     break











    






