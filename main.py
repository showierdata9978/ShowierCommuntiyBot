import os
import random
import json

import asyncio
import time

from dotenv import load_dotenv
from nextcord.ext import commands
import nextcord
import logging


from cogs.levling.levelingfunc import add_experience, level_up, update_data




def Logs():
    global log_name
    global logger
    global lgrall

    log_name = f"{time.time()}"
    f = open(f"logs/all/{log_name}.log", "x")
    logger = logging.getLogger("nextcord")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(
        filename=f"logs/all/{log_name}.log", encoding="utf-8", mode="w"
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)
    lgrall = logging.getLogger("nextcord")
    lgrall.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename=f"logs/all.log", encoding="utf-8", mode="w")
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    lgrall.addHandler(handler)


Logs()
bot = commands.Bot(
    command_prefix="Data!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
)
loop = asyncio.get_event_loop()
bot.author_id = 893981911003836487  # Change to your discord id!!!


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    await asyncio.sleep(5)  # waits 5 second to fully load in


extensions = [
    # Same name as it would be if you were importing it
    "cogs.Commands",
    "cogs.ecom",
]


@bot.event
async def on_member_join(member):
    await member.send(
        "hi , to verify put you age range in thw twosided yt server (ie 13 t0 18 ) and xbox username :D -Owner of bot"
    )



def Banned(thing,type):
    if type == "member":
        with open("banned.txt", "r") as f:
            lines = f.readlines()
        for line in lines:
            if thing.id == line.strip("\n"):
                return True
        return False
    elif type == "guild":
        with open('guilds.json','r') as f:
            j = json.load(f)
        if j['guilds'][thing.id]['banned']:
            return True
        return False

@bot.event
async def on_message(message):
    if message.author.bot is False:
        if not Banned(message.author,'member'):
            with open("users.json", "r") as f:
                users = json.load(f)
            await update_data(users, message.author)
            await add_experience(users, message.author, random.randint(1, 5))
            await level_up(users, message.author, message)
            with open("users.json", "w") as f:
                json.dump(users, f)
            await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)
    print(ctx,"\n\n", error)
    raise error


@bot.event
async def guild_available():
    channels = []
    for channel in bot.get_all_channels():
        channels.append(channel)
    channel = bot.get_channel(channels[2])
    await channel.send("@everyone Showier Is working on the bot :D do Two!help")
    print("ssss")

@bot.listen
async def on_guild_join(self, guild):
    guild_owner = bot.get_user(int(guild.owner.id))
    if not Banned(guild,'guild'):
        
        await guild.text_channels[0].send(f"""
                                hi <@{guild_owner.id}> \n \n

                                          
                                Hi Im ShowierCommunity Bot\n
                                I am Made By ShowierData9978#3454\n
                                I am Also Open Src , My code is here : \n
                                https://github.com/showierdata9978/ShowierCommuntiyBot\n


                                This Bot has these right`s at any point in time to : \n
                                    - Ban Any of your members from the bot (or you)\n
                                    - Ban Your Server From the bot\n
                                    - Reset AnyThing the bot has done in your server (includeing Invites)\n 
                                    - Stop You from inviteing the bot again (WILL PING EVERYONE ON BC YOU ARE BANNED IF SO)\n\n

                                Also Please Run Data!Setup (NOT IMPLEMENTED YET)\n\n\n


                                for help run Data!help\n
                                """)
        print(f"Joined {guild.name}")
        with open('guilds.json','r') as f:
            j = json.load(f)

        j['guilds'][guild.id] = {
            "general":None,
            "Announsmets":None,
            "banned":False
        }

    else:
        await guild.text_channels[0].send(f"""
                                @here \n
                                Someone , One Of your moderators / server makers, invited me.\n\n

                                This Guild Is banned From this Bot. Look at what it can do to your server \n\n

                                This Bot has these right`s at any point in time to : \n
                                    - Ban Any of your members from the bot (or you)\n
                                    - Ban Your Server From the bot\n
                                    - Reset AnyThing the bot has done in your server (includeing Invites)\n 
                                    - Stop You from inviteing the bot again (WILL PING EVERYONE ON BC YOU ARE BANNED IF SO)\n


                                Also <@{bot.author_id}> Is me :D , If this actualy pings The Owner of the bot , 
                                           
                                           
                                """)
        with open('banned.txt','a') as f:
            f.write(guild_owner.id)
        guild.leave()    
        
    
if __name__ == "__main__":  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loades every extension.

# Starts a webserver to be pinged.


# Starts the bot

def runbot():
    load_dotenv()
    token = os.environ.get("token")
    bot.run(token)  # Starts the bot


runbot()
