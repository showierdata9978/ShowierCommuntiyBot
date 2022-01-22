import os
from keep_alive import keep_alive
from nextcord.ext import commands
import nextcord
import logging
import asyncio
import time
import json
from cogs.levling.levelingfunc import update_data,add_experience,level_up

def Logs():
	global log_name
	global logger
	global lgrall

	log_name = f"{time.time()}"
	f = open(f"logs/all/{log_name}.log", "x")
	logger = logging.getLogger('nextcord')
	logger.setLevel(logging.INFO)
	handler = logging.FileHandler(filename=f"logs/all/{log_name}.log",encoding='utf-8',mode='w')
	handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
	logger.addHandler(handler)
	lgrall = logging.getLogger('nextcord')
	lgrall.setLevel(logging.DEBUG)
	handler = logging.FileHandler(filename=f"logs/all.log",encoding='utf-8',mode='w')
	handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
	lgrall.addHandler(handler)

Logs()
bot = commands.Bot(
    command_prefix="Two!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    )
loop = asyncio.get_event_loop()
bot.author_id = 893981911003836487  # Change to your discord id!!!



@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    await asyncio.sleep(5)  #waits 5 second to fully load in





extensions = [
    # Same name as it would be if you were importing it
    'cogs.Commands',
    'cogs.levling.leveling'
]

@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)

async def logmsg(msg):
	print(msg)
	ctx = commands.Context(message=msg,bot=bot,view ='')
	msgt = nextcord.TextChannel.last_message.__Str__
	try:
		with open(f'logs/msglogs/{log_name}','x') as f:
			f.write(f'Time:{time.time()} owner: {msg.author} MSG:{msgt}\n')
	except FileExistsError:
		with open(f'logs/msglogs/{log_name}','a') as f:
			f.write(f'Time:{time.time()} owner: {msg.author} MSG:{msgt}\n')

	
@bot.event
async def on_message(message):
	#await logmsg(message)
	if message.author.bot == False:
		with open('users.json', 'r') as f:
			users = json.load(f)

		await update_data(users, message.author)
		await add_experience(users, message.author, 5)
		await level_up(users, message.author, message)
		with open('users.json', 'w') as f:
		    json.dump(users, f)
		await bot.process_commands(message)

    



@bot.event
async def guild_available():
	channels = []
	for channel in bot.get_all_channels():
	    channels.append(channel)
	channel = bot.get_channel(channels[2])
	await channel.send("@everyone Showier Is working on the bot :D do Two!help")
	print('ssss')

if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ['token']


# Starts the bot
def runbot(token):
    bot.run(token)  # Starts the bot


runbot(token)
