# bot.py
# https://realpython.com/how-to-make-a-discord-bot-python/
import os
import configparser
import discord
import random

# https://docs.python.org/3/library/configparser.html
config = configparser.ConfigParser()
config.read("iain.cfg")
TOKEN = config["INFO"]["token"]
GUILD = config["INFO"]["server"]

class Iain(discord.Client):
    async def on_ready(self):
        guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})')
    
    async def on_message(self, message):
        if message.author == client.user:
            return
        
        iain_puns = [
            "Don't interrupt someone working intently on a puzzle. Chances are, you'll hear some crosswords!",
            "I'm a big fan of whiteboards. I find them quite re-markable!",
            "I was going to make myself a belt made out of watches, but then I realized it would be a waist of time!",
            "The machine at the coin factory just suddenly stopped working, with no explanation. It doesn't make any cents!",
            "Yesterday, a clown held the door open for me. It was such a nice jester!",
            "I'm only friends with 25 letters of the alphabet. I don't know Y."
        ]

        if message.content == ("!pun"):
            response = random.choice(iain_puns)
            await message.channel.send(response)
            print(
                f'Replied to {message.author} with a random pun.'
            )

client = Iain()
client.run(TOKEN)
