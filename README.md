# Iainbot - A discord bot inspired by one of my lecturers.

## Getting started
1. Make sure you've downloaded Python 3.9
2. Create a virtual environment on this folder with `venv`
3. Enter the virtual environment using the `activate` script in \Scripts
4. Use `pip` to install the bot's requirements: `pip install -r requirements.txt`
5. Run the bot - it'll create a file called `iain.cfg`, you'll need to put your token there.

## Connecting to a server
You'll need to use the [Discord Developer Portal](https://discord.com/developers/applications/) to create the bot. 

You can follow [this tutorial](https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-the-developer-portal) to learn how to do that (you'll only need the linked section).

Once you've done that, you can get your bot token, add it to the config file, and then use the portal to invite the bot to a server that you own. The bot has code in it to pre-fill the config file with the necessary variables for the bot to work.

**You'll need to go into the config file (iain.cfg) and add your admin roles to the file.** Example:
`admin_roles = admin,mod`
You'll also need to ensure that whoever is configuring the bot has admin permissions.

## Bot commands
Once you're in a server, type `!help` to see a command list. You can also type `!help <commandname>` to get more detailed help on that command.

In order for a bot to assign/unassign roles, you must make sure the bot is of a higher rank in the server than those roles.