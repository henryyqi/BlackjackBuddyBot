import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import sqlite3

from dotenv import load_dotenv
import os
load_dotenv() # load the .env file
token = os.getenv("DISCORD_TOKEN") # get the token

from Deck import Deck
from Hand import Hand
from Chips import Chips
from Blackjack import Blackjack
from CheckForWin import CheckForWin
BJ = Blackjack()
CFW = CheckForWin()

class Client(commands.Bot): # discord.Client, commands.Bot
    async def on_guild_join(self,guild):
        global GUILD_ID
        GUILD_ID = guild.id
        print(f"Guild id is: {GUILD_ID}")
    
    async def on_ready(self):
        global channel_id
        channel = discord.utils.get(client.get_all_channels(), name="blackjackbuddy")
        if channel:
            channel_id = channel.id
        
        print(f'Hi! My name is {self.user}!')
        await send_message(channel_id,f"Hi! My name is {self.user}. Type in 'playbj' to play Blackjack with me! ('help' for more commands)")
        
        try:
            # sync with server
            guild = discord.Object(GUILD_ID)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
            
        except Exception as e:
            print(f'Error syncing commands: {e}')
        
    async def on_message(self,message):
        # only respond to messages in channel named "blackjackbuddy"
        if message.channel.id == channel_id:
            # ensure bot does not reply to itself
            if message.author == self.user:
                return
            
            ##############
            # Commands that the bot will respond to #
            if message.content.startswith('hello'):
                await message.channel.send(f"Hi there {message.author}, want to play Blackjack? Type in 'playbj' to play Blackjack with me!")
            
            if message.content.startswith('help'):
                '''
                Lists all the different commands available
                '''
                await message.channel.send(
                                            "'hello' to say hi!"
                                            "\n'playbj' to play Blackplay with me!"
                                            "\n'mystats' to look at your career Blackjack stats!"
                )
            
            if message.content.startswith('playbj'):
                '''
                Starts BJ game when message 'playbj' is sent by a user
                '''
                await playBJ(message.channel,message.author)
        
            if message.content.startswith('mystats'):
                '''
                Shows the user's stats 
                '''
                print(f"channel: {message.channel.name}")
                await show_user_stats(message.channel, message.author.name)
            
            if message.content.startswith('chips'):
                '''
                Testing purposes only. Adds 100 chips to my current_chips
                '''
                select_stmt = "SELECT * FROM player_stats WHERE user_id = ?"
                cursor.execute(select_stmt, (message.author.name,))
                
                try: 
                    results = list(cursor.fetchone()) # fetch a tuple with all the stats, change to a list
                    print(f"Test results: {results}")
                    
                    update_stmt = "UPDATE player_stats SET current_chips = ?, total_chips = ? WHERE user_id = ?"
                    cursor.execute(update_stmt,(results[1]+100,results[2]+100,message.author.name))
                    await message.channel.send(f"Hi there {message.author.name}, 100 chips have been added to your account.")
                    
                except TypeError:
                    await message.channel.send("Unable to add chips.")
                
                
            
            if message.content.startswith('clear'):
                await delete_user_stats(message.author.name)
                
            # Commands that the bot will respond to #
            ##############
        else:
            print(f"Message ignored in {message.channel.name}.")
                   
### SETTING UP SQLITE ###

# connect to an SQLite database (or crease it if it doesn't exist)
connection = sqlite3.connect('blackjack_buddy_stats.db')

# create a cursor object using the cursor() method (used to interact with the database)
cursor = connection.cursor()

# create table
cursor.execute(""" CREATE TABLE IF NOT EXISTS player_stats
(user_id TEXT PRIMARY KEY, current_chips INTEGER, total_chips INTEGER, games_played INTEGER, wins INTEGER, losses INTEGER, pushes INTEGER, blackjacks INTEGER, win_pct REAL, bj_pct REAL)""")
print("TABLE CREATED ON SQLITE")
          
### BOT RUNNING HERE ###       
        
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents) # commands.Bot
channel_id = None
# channel_id = 880211592824913933

# my bot testing server client ID, so slash command only works in my server
# GUILD_ID = discord.Object(id=880211592824913930)


async def send_message(channel_id, message):
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)
    if channel and message is not None:
        await channel.send(message)
    else:
        print(f'Message not sent.')

async def new_player_check(channel,author):
    '''
    Check if the user playing is a new player or not by checking records off player_stats
    '''
    print(f"Author's name is: {author.name}")
    select_stmt = "SELECT * FROM player_stats WHERE user_id = ?"
    cursor.execute(select_stmt, (author.name,))
    
    existing_player = cursor.fetchall()
    
    if existing_player:
        return await get_user_stats(author.name)
    else:
        await add_new_user_stats(author.name)
        return await show_user_stats(channel,author.name)
    
        
async def add_new_user_stats(author_name):
    '''
    Add new user to player_stats
    '''
    insert_stmt = (
        "INSERT INTO player_stats(user_id, current_chips, total_chips, games_played, wins, losses, pushes, blackjacks, win_pct, bj_pct)"
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"    
    )
    data = (author_name, 100, 100, 0, 0, 0, 0, 0, 0.0, 0.0)
    cursor.execute(insert_stmt, data)
    connection.commit()
    print("New user stats added and commited.")

async def get_user_stats(author_name):
    '''
    Gets user's player_stats so they can be updated as the user plays
    user_stats = 0 user_id, 1 current_chips, 2 total_chips, 3 games_played, 4 wins, 5 losses, 6 pushes, 7 blackjacks, 8 win_pct, 9 bj_pct
    '''
    select_stmt = "SELECT * FROM player_stats WHERE user_id = ?"
    cursor.execute(select_stmt, (author_name,))
    results = list(cursor.fetchone()) # fetch a tuple with all the stats, change to a list
    return results

async def show_user_stats(channel,author_name):
    '''
    Shows user's player_stats
    user_stats = 0 user_id, 1 current_chips, 2 total_chips, 3 games_played, 4 wins, 5 losses, 6 pushes, 7 blackjacks, 8 win_pct, 9 bj_pct
    '''
    select_stmt = "SELECT * FROM player_stats WHERE user_id = ?"
    cursor.execute(select_stmt, (author_name,))
    
    try :
        results = list(cursor.fetchone()) # fetch a tuple with all the stats, change to a list
        # print(f"RESULTS: {results}")
        msg = f"**♥ ♦ ♠ ♣** Hello {author_name}, here are your **Blackjack** stats **♥ ♦ ♠ ♣** \n\n\t\t\t\t**Games Played:** {results[3]}\nWins: {results[4]}\tLosses: {results[5]}\tPushes: {results[6]}\t\t\t**Win_pct:** {results[8]}\n\t\t\t\tBlackjacks: {results[7]}\t\t\t\t\t\tBlackjack_pct: {results[9]}\nYou currently have {results[1]} chips.      | Your total winnings all-time is **{results[2]} chips.**\n"
    
    except TypeError:
        print("No data available.")
        msg = f"Hello {author_name}, you have no stats available. Type in 'playbj' to play some Blackjack and get started!"
    
    # UI friendly stat dashboard
    await send_message(channel.id,msg)
    
    if results is None:
        return ['']
    else:
        return results
    
async def update_user_stats(user_stats):
    '''
    Updates the player's stats after a game is finished
    user_stats = 0 user_id, 1 current_chips, 2 total_chips, 3 games_played, 4 wins, 5 losses, 6 pushes, 7 blackjacks, 8 win_pct, 9 bj_pct
    '''
    update_stmt = "UPDATE player_stats SET current_chips = ?, total_chips = ?, games_played = ?, wins = ?, losses = ?, pushes = ?, blackjacks = ?, win_pct = ?, bj_pct = ? WHERE user_id = ?"
    cursor.execute(update_stmt,(user_stats[1],user_stats[2],user_stats[3],user_stats[4],user_stats[5],user_stats[6],user_stats[7],user_stats[8],user_stats[9],user_stats[0]))
    connection.commit()

async def delete_user_stats(author_name):
    '''
    Delete a row from the players_stats table baed on user_id
    '''
    delete_stmt = "DELETE FROM player_stats WHERE user_id = ?"
    cursor.execute(delete_stmt, (author_name,))
    connection.commit()
    print(f"Successfully deleted stats for user_id: {author_name}")
    
    
async def commit_and_close():
    connection.commit()
    # connection.close()
        
async def playBJ(channel,author):
    '''
    Starts BJ game when message 'playbj' is sent by a user
    Stops BJ game when the user is out of chips or wants to stop
    '''
    # intake player stats and save onto variables
    user_stats = list(await new_player_check(channel,author))
    connection.commit()
    current_chips, total_chips, games_played, wins, losses, pushes, blackjacks, win_pct, bj_pct = int(user_stats[1]), int(user_stats[2]), int(user_stats[3]), int(user_stats[4]), int(user_stats[5]), int(user_stats[6]), int(user_stats[7]), float(user_stats[8]), float(user_stats[9])
    
    rounds = 0  
    timeoutCheck = False
    while True:

        rounds += 1
        await send_message(channel.id, "Welcome to Blackjack! Let's begin!")
        
        # create a new, shuffled deck
        deck_of_cards = Deck()
        deck_of_cards.shuffle()
        
        # initializes the player's chips and takes a bet
        if rounds == 1:
            player_chips = Chips(current_chips)
        else:
            player_chips.total = player_chips.total
        
        # prompt user for a bet
        await send_message(channel.id,f'You have {player_chips.total} chips.\nPlease enter your bet: ')
        
        while True:   
            
            try: 
                # wait for user input, then check if message.content is valid
                def check(message):
                    return message.author!=client.user and message.channel == channel
                message = await client.wait_for('message',check=check,timeout=30.0)
                
                try:
                    player_chips.bet = int(message.content)
                    if player_chips.bet <= player_chips.total and player_chips.bet > 0:
                        break
                    else:
                        await send_message(channel.id,f"You have {player_chips.total} chips. Please enter a sufficient bet: ")
             
                except ValueError:
                    await send_message(channel.id,"Enter a valid bet!")
                    continue
                
            except asyncio.TimeoutError:
                await send_message(channel.id,"You have been timed out.")
                timeoutCheck = True
                break
        if timeoutCheck:
            break
        
        await send_message(channel.id,f"You bet {player_chips.bet} chips.\n")
        
        CFW.game_on = True
        CFW.player_bust_check = False
        CFW.player_blackjack = False
        
        # deal two cards to player, two cards to dealer
        player_hand = Hand()
        dealer_hand = Hand()
        
        player_hand.add_card(deck_of_cards.deal_card())
        dealer_hand.add_card(deck_of_cards.deal_card())
        player_hand.add_card(deck_of_cards.deal_card())
        dealer_hand.add_card(deck_of_cards.deal_card())
        
        # if player was dealt a blackjack (value of 21 with just 2 cards), break the loop
        if player_hand.hand_value == 21:
            CFW.player_blackjack = True
            
        # ask user for hit or stand. executes hit if choice is hit.
        while True and CFW.player_blackjack is False:
            
            ### BJ.show_some(player_hand,dealer_hand) ###
            await send_message(channel.id,f"Dealer:\t [{dealer_hand.cards[0]}] [?]\nValue: {dealer_hand.cards[0].value}\n\nPlayer:\t")
            for count, ele in enumerate(player_hand.cards):
                await send_message(channel.id,f"[{ele}]")
            await send_message(channel.id,f"Value: {player_hand.hand_value}\n-------------------")
            ### BJ.show_some(player_hand,dealer_hand) ###
            
            if player_hand.hand_value > 21:
                break
            
            await send_message(channel.id,"Would you like to hit 'h' or stand 's'?")
            
            try: 
                # wait for user input, then check if message.content is valid
                def checkHitOrStand(message):
                    return (message.content.lower() =='h' or message.content.lower() =='s') and message.author!=client.user and message.channel == channel
                message = await client.wait_for('message',check=checkHitOrStand,timeout=30.0)
                
                try:
                    # puts the 'h' or 's' into variable named choice
                    BJ.choice = message.content.lower()
                    if BJ.choice == 'h':
                        BJ.hit(deck_of_cards,player_hand)
                        
                        if player_hand.hand_value > 21:
                            # bust!
                            await send_message(channel.id,f"Bust! The total value is {player_hand.hand_value}.")
                            break
                        elif player_hand.hand_value == 21:
                            await send_message(channel.id,f"You got 21!")
                            break
                        
                    elif BJ.choice == 's':
                        await send_message(channel.id,"You chose to stand.")
                        break
                    else:
                        await send_message(channel.id,f"Sorry I don't understand, please enter 'h' for HIT or 's' for STAND.")
                        continue  
                except:
                    # print("Enter again!")
                    await send_message(channel.id,"Try again!")
                    continue
                
            except asyncio.TimeoutError:
                await send_message(channel.id,"You have been timed out.")
                timeoutCheck = True
                break
        if timeoutCheck:
            break
        
        if player_hand.hand_value > 21:
            CFW.game_on = CFW.player_busts(player_chips)
            losses += 1  
        
        # if the player is standing and has not busted, it is the dealer's turn
        # play until dealer reaches 17
        if CFW.player_bust_check is False and CFW.player_blackjack is False:
            print("The dealer's turn.")
            dealer_hand.adjust_for_aces()
            await send_message(channel.id,"The dealer's turn.")
            while dealer_hand.hand_value < 17:
                BJ.hit(deck_of_cards,dealer_hand)
                
                if dealer_hand.hand_value > 21:
                    
                    # bust!
                    await send_message(channel.id,f"Bust! The total value is {dealer_hand.hand_value}.")
                    CFW.dealer_busts(player_chips)    
                    wins += 1
        
        # playing is over, time to compare diff winning scenarios
        await send_message(channel.id,"Dealer:\t")
        for count, ele in enumerate(dealer_hand.cards):
            await send_message(channel.id,f"[{ele}]")
        await send_message(channel.id,f"Value: {dealer_hand.hand_value}\n\nPlayer:\t")
        for count, ele in enumerate(player_hand.cards):
            await send_message(channel.id,f"[{ele}]")
        await send_message(channel.id,f"Value: {player_hand.hand_value}\nGAME OVER!\n-------------------")
        
        # player wins/dealer wins
        if CFW.player_blackjack is True:
            player_chips.bet = player_chips.bet*1.5
            CFW.player_wins(player_chips)
            wins += 1
            blackjacks += 1
        elif CFW.player_bust_check is False and player_hand.hand_value > dealer_hand.hand_value:
            CFW.player_wins(player_chips)
            wins += 1
        elif CFW.player_bust_check is False and player_hand.hand_value < dealer_hand.hand_value and dealer_hand.hand_value <= 21:
            CFW.dealer_wins(player_chips)
            losses += 1
        elif CFW.player_bust_check is False and player_hand.hand_value == dealer_hand.hand_value:
            CFW.push()
            pushes += 1
        
        ########################
        # update stat variables
        games_played += 1
        if player_chips.total > current_chips:
            # the player won chips, add to total winnings, if not, don't add
            total_chips += (player_chips.total - current_chips)
        current_chips = player_chips.total
        win_pct = float("{:.2f}".format(wins/games_played*100))
        bj_pct = float("{:.2f}".format(blackjacks/games_played*100))
        print(f"Player: {user_stats[0]}\tCurrent Chips: {current_chips}\tTotal Chips: {total_chips}\t Games Played: {games_played}\tWins: {wins}\t Losses: {losses}\tPushes: {pushes}\tBlackjacks: {blackjacks}\tWin_pct: {win_pct}\tBj_pct: {bj_pct}")
        
        ########################
        # chip count
        # print(f"Chips total: {player_chips.total}")
        await send_message(channel.id,f"Chips total: {player_chips.total}")
        
        if player_chips.total == 0:
            # print("You are out of chips! Better luck next time!")
            await send_message(channel.id,"You are out of chips! Better luck next time!")
            break
        
        # # ask to play again
        
        await send_message(channel.id,"Would you like to play again? (y/n)")
        while True:
            try: 
                # wait for user input, then check if message.content is valid
                def checkReplay(message):
                    return (message.content.lower() == 'y' or message.content.lower() == 'n') and message.author!=client.user and message.channel == channel
                message = await client.wait_for('message',check=checkReplay,timeout=30.0)
                
                try:
                    replay = message.content.lower()
                    if replay == 'y':
                        CFW.game_on = True
                        break
                    elif replay =='n':
                        break
                    else:
                        await send_message(channel.id,"Please enter 'y' to play again, or 'n' to cash out.") 
                except :
                    await send_message(channel.id,"Enter again!")
                    continue
                
            except asyncio.TimeoutError:
                await send_message(channel.id,"You have been timed out.")
                timeoutCheck = True
                break
            
        if timeoutCheck:
            break
        
        if replay == 'y':
            continue
        else:
            await send_message(channel.id,"You've cashed out your chips. Thanks for playing!")
            break
    
    # after BJ game is over
    ########################
    # update user_stats
    user_stats[1], user_stats[2], user_stats[3], user_stats[4], user_stats[5], user_stats[6], user_stats[7], user_stats[8], user_stats[9] = str(current_chips), str(total_chips), str(games_played), str(wins), str(losses), str(pushes), str(blackjacks), str(win_pct), str(bj_pct)
    await update_user_stats(tuple(user_stats))

# client = Client(intents=intents) # discord.Client
client.run(token)




# run_discord_bot()

