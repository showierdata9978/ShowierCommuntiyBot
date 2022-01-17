import os

from keep_alive import keep_alive
from nextcord.ext import commands 

bot = commands.Bot(
	command_prefix="Two!",  # Change to desired prefix
	case_insensitive=True  # Commands aren't case-sensitive
)

bot.author_id = 893981911003836487  # Change to your discord id!!!

@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


extensions = [
	 # Same name as it would be if you were importing it
    'cogs.Commands'
]

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = "    "  # Starts the bot

bot.run(token)  # Starts the bot
