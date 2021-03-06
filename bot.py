# bot.py
# https://realpython.com/how-to-make-a-discord-bot-python/
import os
import configparser
from discord.ext import commands
from discord import utils
from discord import File
from discord import Intents
from discord import Embed
import random
import puns
import anecdotes
import facts

# https://docs.python.org/3/library/configparser.html
config = configparser.ConfigParser()
if not os.path.exists("iain.cfg"):
    config["INFO"] = {"token": ""}
    config.write(open("iain.cfg, w"))

config.read("iain.cfg")

# gets the bot token
TOKEN = config["INFO"]["token"]
IAIN_PUNS = puns.neutral # yes, this is indeed a list of puns. https://pyjok.es/
IAIN_ANECDOTE = anecdotes.neutral # takes list from anecdotes file
IAIN_FACT = facts.neutral # takes list from facts file
RESTRICTED_COMMAND_MSG = "Sorry, that command is for server moderators only!"

print("constants initialised.")

# bot intents
intents = Intents.default()
intents.members = True
print("bot intents set.")

bot = commands.Bot(command_prefix="!", intents=intents) #setting the command prefix to !
print("bot created.")

# mod checker
def check_if_mod(roles, guildname):
    mod = False
    for role in roles:
        if role.name in config[guildname]["admin_roles"].split(","):
            mod = True
    return mod


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
    config[f"{guild.name}"] = {"name": f"'{guild.name}'", "autorole": "false", "remove_default_role": "true", "default_role": "", "admin_roles": "", "self_assignable_roles": ""}
    config.write(open("iain.cfg", "w"))
    print(f"{bot.user.name} has joined {guild.name}")

    general = utils.find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello {}!'.format(guild.name))

# auto-assigns member role if enabled
@bot.event
async def on_member_join(member):
    if config[member.guild.name]["autorole"] == "true":
        rank = utils.get(member.guild.roles, name=config[member.guild.name]["default_role"]) #Bot get guild(server) roles
        await member.add_roles(rank)
        print(f"{member} was given the {rank} role.")

# error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I don't understand what you mean!")
    raise error

print("events defined.")

# prints a random pun from the pun list
@bot.command(name="pun", brief="Sends a random pun", help="Sends a random pun from a predefined list. Ask Nick about adding more!")
async def pun(ctx):
    response = random.choice(IAIN_PUNS)
    await ctx.send(response)

# prints "No worries!" with an image of ronald murray smiling. How lovely
@bot.command(name="thanks", brief="You're welcome (and a free iain picture)", help="Responds to a user saying `You're welcome` and a picture of Iain smiling. How cute")
async def thanks(ctx):
    response = "No worries!"
    smiley_iain = File("images/smiley_iain.png")
    await ctx.send(response)
    await ctx.send(file=smiley_iain)

# gives an anecdote
@bot.command(name="anecdote", brief="Responds with the beginning of an annecdote", help="Responds with an annecdote akin to something Iain might say. Needs more work, feel free to contribute.")
async def anecdote(ctx):
    response = random.choice(IAIN_ANECDOTE) # added anecdotes into file, choses one at random
    await ctx.send(response)

# joins VC of user
@bot.command(name="join", brief="Join a VC that the user is in", help="Joins whichever voice channel the message author is in. Returns an error message if you're not in one.")
async def join(ctx):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
    except AttributeError:
        await ctx.send("You need to join a voice channel first before I can join you!")

# leaves VC
@bot.command(name="leave", brief="Leaves whatever VC he's in.", help="Leaves whichever voice channel he's currently in. Responds with an error message if he's not in a voice channel.")
async def leave(ctx):
    try:
        await ctx.voice_client.disconnect()
    except AttributeError:
        await ctx.send("I can't leave the voice channel because I'm not in one!")

# toggles auto-role for a server
@bot.command(name="autorole", brief="[Admin]Toggle automatic role assignment", help="Turns automatic role assignment on or off (using arg 'true' or 'false' respectively). It'll give the status of autorole if you don't provide args", usage="<true/false>")
async def autorole(ctx, *arg):
    mod = check_if_mod(ctx.message.author.roles, ctx.guild.name)
    if mod:
        if config[ctx.guild.name]["default_role"] == "" or config[ctx.guild.name]["default_role"] == " ":
            await ctx.send("Please set a default role using `defaultRole <rolename>` before activating autorole.")
        else:
            if arg:
                if arg[0] == "true":
                    config[ctx.guild.name]["autorole"] = 'true'
                    config.write(open("iain.cfg", "w"))
                    await ctx.send("Autorole is now true")
                elif arg[0] == "false":
                    config[ctx.guild.name]["autorole"] = 'false'
                    config.write(open("iain.cfg", "w"))
                    await ctx.send("Autorole is now false")
                else:
                    await ctx.send("Invalid argument. Please try again.")
            else:
                autorole_status = config[ctx.guild.name]["autorole"]
                await ctx.send(f"Autorole status: {autorole_status}")
    else:
        await ctx.send(RESTRICTED_COMMAND_MSG)

@bot.command(name="removeDefaultRole", brief="[Admin]Toggle default role removal", help="Turns default role removal on or off (using arg 'true' or 'false' respectively). It'll give the status of removeDefaultRole if you don't provide args", usage="<true/false>")
async def removeDefaultRole(ctx, *arg):
    mod = check_if_mod(ctx.message.author.roles, ctx.guild.name)
    if mod:
        if arg:
            if arg[0] == "true":
                config[ctx.guild.name]["remove_default_role"] = 'true'
                config.write(open("iain.cfg", "w"))
                await ctx.send("RemoveDefualtRole is now true")
            elif arg[0] == "false":
                config[ctx.guild.name]["remove_default_role"] = 'false'
                config.write(open("iain.cfg", "w"))
                await ctx.send("RemoveDefualtRole is now false")
            else:
                await ctx.send("Invalid argument. Please try again.")
        else:
            remove_default_role_status = config[ctx.guild.name]["remove_default_role"]
            await ctx.send(f"RemoveDefualtRole status: {remove_default_role_status}")
    else:
        await ctx.send(RESTRICTED_COMMAND_MSG)

# sets the default role
@bot.command(name="defaultRole", brief="[Admin]Sets the default role for new users", help="Sets the default role that autorole uses for new users. You need to turn autorole on for this to work!", usage="<rolename>")
async def set_default_role(ctx, *arg):
    mod = check_if_mod(ctx.message.author.roles, ctx.guild.name)
    if mod:
        if arg:
            roles = ctx.guild.roles
            valid_role = False
            for role in roles:
                if arg[0] == role.name:
                    valid_role = True
                    break
            if valid_role:
                config[ctx.guild.name]["default_role"] = arg[0]
                config.write(open("iain.cfg", "w"))
                await ctx.send(f"Default role for new members is now `{arg[0]}`")

                if config[ctx.guild.name]["autorole"] == 'false':
                    await ctx.send("Remember to activate autorole to use this feature!")

            else:
                await ctx.send(f"`{arg[0]}` is not in the list of roles for this server.")
        else:
            current_default_role = config[ctx.guild.name]["default_role"]
            await ctx.send(f"Current default role: {current_default_role}")
    else:
        await ctx.send(RESTRICTED_COMMAND_MSG)

@bot.command(name="selfAssignableRoles", brief="[Admin]Add/remove/view self-assignable roles", help="Add, remove, or view roles which are self-assignable. Leave empty to view self-assignable roles", usage="<add/remove> <rolename>")
async def self_assignable_roles(ctx, *args):
    mod = check_if_mod(ctx.message.author.roles, ctx.guild.name)
    if mod:
        if args:
            roles = ctx.guild.roles
            valid_role = False
            for role in roles:
                try:
                    if args[1] == role.name:
                        valid_role = True
                        break
                except IndexError:
                    await ctx.send("You need to specify which role you're trying to modify!")
                    break
            if valid_role:
                if args[0] == "add":
                    current_roles = config[ctx.guild.name]["self_assignable_roles"].split(",")
                    if args[1] not in current_roles:
                        current_roles.append(args[1])
                        if current_roles[0] == "":
                            current_roles.pop(0)
                        config[ctx.guild.name]["self_assignable_roles"] = ",".join(current_roles)
                        config.write(open("iain.cfg", "w"))
                        await ctx.send(f"`{args[1]}` is now self-assignable.")
                    else:
                        await ctx.send(f"`{args[1]}` is already self-assignable!")


                elif args[0] == "remove":
                    current_roles = config[ctx.guild.name]["self_assignable_roles"].split(",")
                    if current_roles[0] == "":
                        current_roles.pop(0)

                    if args[1] in current_roles:
                        current_roles.remove(args[1])
                        config[ctx.guild.name]["self_assignable_roles"] = ",".join(current_roles)
                        config.write(open("iain.cfg", "w"))
                        await ctx.send(f"`{args[1]}` is no longer self-assignable.")
                    else:
                        await ctx.send("That role is not self-assignable, no need to remove it.")
                    
                else:
                    await ctx.send("Sorry, that option does not exist!")
            else:
                await ctx.send(f"`{args[1]}` is not in the list of roles for this server.")
        else:
            current_roles = config[ctx.guild.name]["self_assignable_roles"]
            await ctx.send(f"Current self-assignable roles: {current_roles}")
    else:
        await ctx.send(RESTRICTED_COMMAND_MSG)

# assign role to self
@bot.command(name="iam", brief="Assign yourself a role. Leave empty to see self-assignable roles.", help="Assign yourself one of the self-assignable roles. If you don't provide a role name, the list of self-assignable roles wll be shown.", usage="<rolename>")
async def self_assign_role(ctx, *arg):
    if arg:
        roles = ctx.guild.roles
        role_exists = False
        valid_role = False
        role_name = None
        for role in roles:
            try:
                if arg[0].lower() == role.name.lower():
                    role_exists = True
                    role_name = role.name
                    break
            except IndexError:
                await ctx.send("You need to specify which role you're trying to assign!")
                break
        if role_exists:
            current_roles = config[ctx.guild.name]["self_assignable_roles"].split(",")
            if role_name in current_roles:
                valid_role = True
            else:
                await ctx.send("That role is not self-assignable!")
        else:
            await ctx.send("That role does not exist!")
        if valid_role:
            rank = utils.get(ctx.guild.roles, name=role_name)
            if rank not in ctx.message.author.roles:
                await ctx.message.author.add_roles(rank)
                await ctx.send(f"You are now {role_name}")
                if config[ctx.guild.name]["remove_default_role"] == "true":
                    default_role = utils.get(ctx.guild.roles, name=config[ctx.guild.name]["default_role"])
                    await ctx.message.author.remove_roles(default_role)
            else:
                await ctx.send(f"You're already {role_name}!")
    else:
        current_roles = config[ctx.guild.name]["self_assignable_roles"]
        await ctx.send(f"Current self-assignable roles: {current_roles}")

# pet command, sends picture of pet
@bot.command(name="pet", brief="Sends a picture of Vincent's dog, Nick's cat, or another pet.", help="Fetches a picture of Vincent's dog (Ollie), Nick's cat (Scruffy), or one of vincent's freinds' pets and puts it in the chat.")
async def pet(ctx):
    petnumber = random.randint(0, 145)
    imagelink = f"https://cdn.vlee.me.uk/TurnipBot/pets/{petnumber}.png"
    
    await ctx.send(imagelink)

# helpful tips when exams role around
@bot.command(name="examHelp", brief="A handy hint from Uncle Iain")
async def examHelp(ctx):
    await ctx.send("```sql\nSELECT answer\n FROM notes\n WHERE answer=correct\n AND relevance>80\n```")

# Iain Facts
@bot.command(name="fact", brief="Let me show you my vast intelect", help="Prints a random fact from the facts file")
async def fact(ctx):
    response = random.choice(IAIN_FACT)
    await ctx.send(response)

# Iain's opinion on cheating
@bot.command(name="cheat", brief="A reminder of how I feel about cheating", help="Iain gives his opinion about cheating and sends the university guide to academic misconduct")
async def cheat(ctx):
    response = ("I've said it before, I'll say it again... ANY form of cheating is prohibited under university policy. Just because you are in a discord server, does not mean you are safe from being caught... some folk are right snakes\nReminder: https://www.dundee.ac.uk/corporate-information/code-practice-academic-misconduct-students... even though you shouldn't need to be reminded :/")
    await ctx.send(response)

print ("functions loaded.")

if TOKEN == "" or TOKEN == " ":
    print("You haven't set your bot's token.")
    print("Please go into iain.cfg and paste in your bot's token, which can be found here: https://discord.com/developers/applications/")
else:
    print("running bot.")
    bot.run(TOKEN)
