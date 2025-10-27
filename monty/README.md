# MONTY THE BOT
#### Video Demo:  https://www.youtube.com/watch?v=ZYMHKLyXhq0
#### Description: 

Monty is a discord bot that allows users to play the famous monty hall game. The program consists of two files, bot.py and bot.db. The database contains two tables, keeping track of users who have played the bot and a history of all plays, keeping track of who the user is, whether they stayed or switched, and whether they won that round. While not in the folder, a seperate .env file is required, containing the personalised discord token mentioned in the python file.


### Introduction to Game:

The monty hall game is a famous problem in statistics where a player is offered three doors, behind one of which is a reward. After the player has chosen a door, another door that does not have a reward is revealed to the player. The player is then offered a choice to switch or stay. While there is a solution that offers a better statistical chance of winning, it is unintuitive to many, hence my motivation to make a bot that allows users to experiment for themselves. A framework of the game is included in monty.py, though this file is not required for the bot to work. 


### Functions of bot.py

## Imports

The import of os and load_dotenv is commonly used to link a .env file to the code containing a discord token, ensuring secure storage. Sqlite3 is chosen as I have more experience using this than MySQL and PostgreSQL, and its features are sufficient for my program. 

## Functions 

# on_ready()

The on_ready function is used to ensure the bot is online and synced up correctly.


# hello()

Just a hello world.


# stats()

The stats function is used to display the statistics of a certain user playing the game (win rate, switch rate, etc.). This is done by first connecting to the bot.db database where it makes use of the table containing the history of plays. The function takes in an additional argument in the form of a mention of another user. The user id is extracted and used to extract data from the plays table. From here float arithmetic is used to calculate the rate at which a user switches and their win rate. Try and excepts are used here to avoid the ZeroDivisionError, where if it occurs just sets the value to 0. From here the data is sent as a message to the channel that the command is run, with the switch rate and win rate set to one decimal point for visual purposes. The database commands are then committed and the database is closed. 


# scoreboard()

The scoreboard function is used to display the stats of all plays that have happened, with a record for games where players stayed and games where players switched. The first step is to form a connection to the bot.db database to access the plays table. From here the data is extracted into variables. The try and excepts are used to avoid errors when there are no records in the database. After this float arithmetic is used to calculate the win rate for the stay and switch strategies, using try and excepts to avoid ZeroDivisionError, where if it occurs just sets the value to 0. The data is then displayed with the win rate set to 1 decimal point for visual purposes, and the database commands are committed and closed.

# play()

This is the command to play the game. The structure of this command is based on the monty.py program. The game is generated with the two tables opendoor and reward, with all values set to False. A random index of the reward list is then set to True, indicating a reward for that number. The first() class is then called (details below), returning the gate that the user chose. The corresponding index in the opendoor list is then switched to True, indicating that this door is flipped.

The next step is the reveal of one of the wrong doors. There are two possibilities depending on whether the user chose the right door. If the wrong door is chosen, only one door will be both unopened and wrong, hence that door is revealed. If the right door is chosen, a random door out of the two is chosen. 

The option to switch is given to the user through the second() class (detailed below). The user's id, name, and whether they switched is returned. If the user chooses to stay, the switch value returned is False, and the index of the original gate is checked with the reward list. If the user chooses to switch, the switch value returned is True. The opendoor list is checked for which gate is still unopened, and that is made into the user's new choice. This new choice is checked with the reward list. 

The user's id, switch choice, and whether they won is then inserted into the plays table, with 0 being False and 1 being True. The username and id is inserted into the users table if not in already. 

The choice of buttons was to limit the variety of input the user could give, ensuring smoothness of the game.


This file was only possible with the help of the following YouTube channels:
James S
Glowstik
