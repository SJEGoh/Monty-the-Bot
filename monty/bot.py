import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from random import randint
import sqlite3

gate: int
switch: bool = None

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix = "./", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is up")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.\n")
    except Exception as e:
        print(e)

@bot.tree.command(name = "hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello world!")

@bot.tree.command(name = "stats")
async def stats(interaction: discord.Interaction, member: discord.Member):
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()
    userid = member.id
    times_played = (cur.execute("SELECT COUNT(*) FROM plays WHERE userid = ( ? )", (userid,))).fetchone()[0]
    wins = (cur.execute("SELECT COUNT(*) FROM plays WHERE userid = ( ? ) AND win = 1", (userid,))).fetchone()[0]
    losses = (cur.execute("SELECT COUNT(*) FROM plays WHERE userid = ( ? ) AND win = 0", (userid,))).fetchone()[0]
    switches = (cur.execute("SELECT COUNT(*) FROM plays WHERE userid = ( ? ) AND stay = 0", (userid,))).fetchone()[0]
    try:
        switchrate = 100 * (float(switches)/times_played)
    except:
        switchrate = 0
    try:
        winrate = 100 * (float(wins)/times_played)
    except:
        winrate = 0
    await interaction.response.send_message(f"-----Showing stats for {member.name}-----\n\n\
     Plays: {times_played}\n     Wins: {wins}\n     Losses: {losses}\n     Switch Rate: {round(switchrate, 1)}%\n     Win rate: {round(winrate, 1)}%")
    conn.commit()
    conn.close()


@bot.tree.command(name = "scoreboard")
async def scoreboard(interaction: discord.Interaction):
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()

    try:
        stwins = (cur.execute("SELECT COUNT(win) FROM plays WHERE stay = 1 AND win = 1")).fetchone()[0]
    except:
        stwins = 0
    try: 
        stlose = (cur.execute("SELECT COUNT(win) FROM plays WHERE stay = 1 AND win = 0")).fetchone()[0]
    except:
        stlose = 0
    try: 
        swwins = (cur.execute("SELECT COUNT(win) FROM plays WHERE stay = 0 AND win = 1")).fetchone()[0]
    except:
        swwins = 0
    try:
        swlose = (cur.execute("SELECT COUNT(win) FROM plays WHERE stay = 0 AND win = 0")).fetchone()[0]
    except: 
        swlose = 0

    try:
        stwinrate = 100 * (float(stwins)/(cur.execute("SELECT COUNT(win) FROM plays WHERE stay = 1")).fetchone()[0])
    except:
        stwinrate = 0
    try:
        swwinrate = 100 * (float(swwins)/(cur.execute("SELECT COUNT(win) FROM plays WHERE stay = 0")).fetchone()[0])
    except: 
        swwinrate = 0
    await interaction.response.send_message(f"Record where players stayed: {stwins} W : {stlose} L\n\
Record where players switched: {swwins} W : {swlose} L\n\
Win rate (Stay : Switch): {round(stwinrate, 1)}% : {round(swwinrate,1)}%")
    
    conn.commit()
    conn.close()
    
class first(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label = "First Door", style = discord.ButtonStyle.green)
    async def door1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You have selected the first door")
        self.gate = 0
        self.stop()
    
    @discord.ui.button(label = "Second Door", style = discord.ButtonStyle.blurple)
    async def door2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You have selected the second door")
        self.gate = 1
        self.stop()

    @discord.ui.button(label = "Third Door", style = discord.ButtonStyle.red)
    async def door3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You have selected the third door")
        self.gate = 2
        self.stop()

class second(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label = "Stay", style = discord.ButtonStyle.green)
    async def stay(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You have chosen to stay")
        self.client = interaction.user.name
        self.clientid = interaction.user.id
        self.switch = False
        self.stop()

    @discord.ui.button(label = "Switch", style = discord.ButtonStyle.blurple)
    async def switch(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You have chosen to switch")
        self.client = interaction.user.name
        self.clientid = interaction.user.id
        self.switch = True
        self.stop()

@bot.command()
async def play(ctx):
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()

    opendoor = [False, False, False]
    reward = [False, False, False]

    reward[randint(0, 2)] = True
    await ctx.channel.send("Please choose a door")
    one = first()
    await ctx.send(view = one)
    await one.wait()
    opendoor[one.gate] = True

    wrong = []
    for i in range(0, 3):
        if opendoor[i] == False and reward[i] == False:
            wrong.append(i + 1)

    if len(wrong) == 2:
        reveal = wrong[randint(0, 1)]
        await ctx.channel.send(f"Gate {reveal} has no reward\n")
        opendoor[reveal - 1] = True
    else:
        await ctx.channel.send(f"Gate {wrong[0]} has no reward\n")
        opendoor[wrong[0] - 1] = True
    
    two = second()
    await ctx.send(view = two)
    await two.wait()
    cur.execute("INSERT OR IGNORE INTO users (id, user) VALUES ( ? , ? )", (two.clientid, two.client))

    if two.switch == False:
        if reward[one.gate] == True:
            await ctx.channel.send("You won!")
            cur.execute("INSERT INTO plays (userid, stay, win) VALUES ( ? , ? , ?)", (two.clientid, 1, 1))
        else:
            await ctx.channel.send("You lose")
            cur.execute("INSERT INTO plays (userid, stay, win) VALUES ( ? , ? , ?)", (two.clientid, 1, 0))
    elif two.switch == True:
        for i in range(0, 3):
            if opendoor[i] == False:
                newchoice = i
            else:
                continue
        
        if reward[newchoice] == True:
            await ctx.channel.send("You won!")
            cur.execute("INSERT INTO plays (userid, stay, win) VALUES ( ? , ? , ?)", (two.clientid, 0, 1))
        else:
            await ctx.channel.send("You lose")
            cur.execute("INSERT INTO plays (userid, stay, win) VALUES ( ? , ? , ?)", (two.clientid, 0, 0))

    conn.commit()
    conn.close()

bot.run(TOKEN)
