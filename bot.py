# bot.py
# https://realpython.com/how-to-make-a-discord-bot-python/
import os
import configparser
from discord.ext import commands
from discord import utils
from discord import File
from discord import Intents
import random

# https://docs.python.org/3/library/configparser.html
config = configparser.ConfigParser()
if not os.path.exists("iain.cfg"):
    config["INFO"] = {"token": ""}
    config.write(open("iain.cfg, w"))

config.read("iain.cfg")

# gets the bot token
TOKEN = config["INFO"]["token"]
IAIN_PUNS = [
        "Don't interrupt someone working intently on a puzzle. Chances are, you'll hear some crosswords!",
        "I'm a big fan of whiteboards. I find them quite re-markable!",
        "I was going to make myself a belt made out of watches, but then I realized it would be a waist of time!",
        "The machine at the coin factory just suddenly stopped working, with no explanation. It doesn't make any cents!",
        "Yesterday, a clown held the door open for me. It was such a nice jester!",
        "I'm only friends with 25 letters of the alphabet. I don't know Y."
    ] # yes, this is indeed a list of puns.
DEFAULT_ROLE = "SetYourRolePlease" # Role to be autoroled when user joins

# bot intents
intents = Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents) #setting the command prefix to !

# bot initialisation readouts
@bot.event
async def on_ready():
    print(
        f'{bot.user.name} is live.\n'
        f'{bot.user.name} is connected to:'
        )
    for guild in bot.guilds:
        print(
            f'-{guild.name}'
            )
    print("")

# creates server info in cfg file when bot joins server
@bot.event
async def on_guild_join(guild):
    config[f"{guild.name}"] = {"name": f"'{guild.name}''", "autorole": "false", "default_role": "", "adminroles": "", "self_assignable_roles": ""}
    config.write(open("iain.cfg", "w"))
    print(f"{bot.user.name} has joined {guild.name}")

    general = utils.find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello {}!'.format(guild.name))

# auto-assigns member role if enabled
@bot.event
async def on_member_join(member):
    if config[member.guild.name]["autorole"] == "true":
        rank = utils.get(member.guild.roles, name=DEFAULT_ROLE) #Bot get guild(server) roles
        await member.add_roles(rank)
        print(f"{member} was given the {rank} role.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I don't understand what you mean!")

# prints a random pun from the pun list
@bot.command(name="pun", brief="Sends a random pun", help="Sends a random pun from a predefined list. Ask Nick about adding more!")
async def pun(ctx):
    response = random.choice(IAIN_PUNS)
    await ctx.send(response)

# prints "No worries!" with an image of ronald murray smiling. How lovely
@bot.command(name="thanks", brief="You're welcome (and a free iain picture)", help="Responds to a user saying `You're welcome` and a picture of Iain smiling. How cute")
async def pun(ctx):
    response = "No worries!"
    smiley_iain = File("images/smiley_iain.png")
    await ctx.send(response)
    await ctx.send(file=smiley_iain)

@bot.command(name="anecdote", brief="[beta]Responds with the beginning of an annecdote", help="Responds with an annecdote akin to something Iain might say. Needs more work, feel free to contribute.")
async def pun(ctx):
    response = "I remember once back in 1987 when I was learning to work with computers..."
    await ctx.send(response)

@bot.command(name="join", brief="Join a VC that the user is in", help="Joins whichever voice channel the message author is in. Returns an error message if you're not in one.")
async def join(ctx):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
    except AttributeError:
        await ctx.send("You need to join a voice channel first before I can join you!")

@bot.command(name="leave", brief="Leaves whatever VC he's in.", help="Leaves whichever voice channel he's currently in. Responds with an error message if he's not in a voice channel.")
async def leave(ctx):
    try:
        await ctx.voice_client.disconnect()
    except AttributeError:
        await ctx.send("I can't leave the voice channel because I'm not in one!")

# @bot.command(name="autorole")
# async def autorole(ctx, arg):
#     # mod = any(x in ctx.message.author.roles for x in config[ctx.guild.name]["adminroles"].split(","))
#     if arg == "true":
#         # config[ctx.guild.name]["autorole"] = {"true"}
#         # config.write(open("iain.cfg", "w"))
#         await ctx.send("Autorole set to true")

if TOKEN == "" or TOKEN == " ":
    print("You haven't set your bot's token.")
    print("Please go into iain.cfg and paste in your bot's token, which can be found here: https://discord.com/developers/applications/")
else:
    bot.run(TOKEN)
