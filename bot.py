# bot.py
# https://realpython.com/how-to-make-a-discord-bot-python/
import os
import configparser
from discord.ext import commands
from discord import utils
import random

# https://docs.python.org/3/library/configparser.html
config = configparser.ConfigParser()
config.read("iain.cfg")

TOKEN = config["INFO"]["token"]
GUILD = config["INFO"]["server"]
IAIN_PUNS = [
        "Don't interrupt someone working intently on a puzzle. Chances are, you'll hear some crosswords!",
        "I'm a big fan of whiteboards. I find them quite re-markable!",
        "I was going to make myself a belt made out of watches, but then I realized it would be a waist of time!",
        "The machine at the coin factory just suddenly stopped working, with no explanation. It doesn't make any cents!",
        "Yesterday, a clown held the door open for me. It was such a nice jester!",
        "I'm only friends with 25 letters of the alphabet. I don't know Y."
    ]

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    # guild = utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(
        # f'{bot.user.name} is connected to the following guild:\n'
        # f'{guild.name}(id: {guild.id})'
        f'{bot.user.name} is connected to discord!'
        )

@bot.command(name="pun")
async def pun(ctx):
    response = random.choice(IAIN_PUNS)
    await ctx.send(response)

@bot.command(name="thanks")
async def pun(ctx):
    response = "No worries!\nhttps://media.discordapp.net/attachments/497770127975120907/783443362429927465/FaceApp_1603736244196.jpg"
    await ctx.send(response)

bot.run(TOKEN)
