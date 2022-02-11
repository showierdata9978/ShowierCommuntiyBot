from nextcord.ext import commands
from nextcord import Embed
import aiohttp
import sys
import random
import nextcord
import json
import datetime
import time


class Command(commands.Cog, name="normal commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        self.ctx = ctx
        await self.ctx.send(
            f"The Bots Ping is {round(ctx.bot.latency,1)}, The server name is {ctx.guild}"
        )
        return "done"

    @commands.command(name="Announce", AdminsOnly=True)
    async def announce(self, ctx, *, message):
        self.announsment = []
        for channel in ctx.Guild.channels:
            if channel.isinstance(channel, nextcord.announcementchanel):
                self.announsment.append(channel)
        self.channel = ctx.bot.get_channel(self.announsment[1].id)
        await self.channel.send(f"@everyone {message}")


class DevCommands(commands.Cog, name="Developer Commands"):
    """These are the developer commands"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        """
        return ctx.author.id == self.bot.author_id

    @commands.command(  # Decorator to declare where a command is.
        name="reload",  # Name of the command, defaults to function name.
        aliases=["rl"],  # Aliases for the command.
    )
    async def reload(self, ctx, cog):
        """
        Reloads a cog.
        """
        extensions = self.bot.extensions  # A list of the bot's cogs/extensions.
        if cog == "all":  # Lets you reload all cogs at once
            for extension in extensions:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            await ctx.send("Done")
        if cog in extensions:
            self.bot.unload_extension(cog)  # Unloads the cog
            self.bot.load_extension(cog)  # Loads the cog
            await ctx.send("Done")  # Sends a message where content='Done'
        else:
            await ctx.send("Unknown Cog")  # If the cog isn't found/loaded.

    @commands.command(name="unload", aliases=["ul"])
    async def unload(self, ctx, cog):
        """
        Unload a cog.
        """
        extensions = self.bot.extensions
        if cog not in extensions:
            await ctx.send("Cog is not loaded!")
            return
        self.bot.unload_extension(cog)
        await ctx.send(f"`{cog}` has successfully been unloaded.")

    @commands.command(name="load")
    async def load(self, ctx, cog):
        """
        Loads a cog.
        """
        try:

            self.bot.load_extension(cog)
            await ctx.send(f"`{cog}` has successfully been loaded.")

        except commands.errors.ExtensionNotFound:
            await ctx.send(f"`{cog}` does not exist!")

    @commands.command(name="listcogs", aliases=["lc"])
    async def listcogs(self, ctx):
        """
        Returns a list of all enabled commands.
        """
        base_string = "```css\n"  # Gives some styling to the list (on pc side)
        base_string += "\n".join([str(cog) for cog in self.bot.extensions])
        base_string += "\n```"
        await ctx.send(base_string)

    @commands.command(name="Shutoff", aliases=["ShutDown", "TurnOff", "poweroff", "Sd"])
    async def shutdown(self, ctx):
        await ctx.send("Shutting down")
        await ctx.bot.close()
        print("bot shutdown complete")

        sys.exit(0)

    @commands.command(name="say")
    async def say(self, ctx, *, message):

        self.ctx = ctx
        self.message = message
        await ctx.message.delete()
        await self.ctx.send(message)

    @commands.command(name="ban")
    async def ban(self, ctx, *, Memeber: nextcord.member):
        with open("banned.txt", "a") as f:
            f.write(Memeber.id)

    @commands.command("unban")
    async def unban(self, ctx, *, member):
        with open("banned.txt", "r") as file:
            lines = file.readlines()

        # delete matching content
        content = member.id
        with open("banned.txt", "a") as file:
            for line in lines:
                # readlines() includes a newline character
                if line.strip("\n") != content:
                    file.write(line)

    @commands.command()
    async def servers(self, ctx):
        activeservers = client.guilds
        for guild in activeservers:
            await ctx.send(guild.name)
            print(guild.name)

    async def leaveguild(self, ctx, guild_name):
        targetGuild = get(self.bot.guilds, name=guild_name)
        if targetGuild is None:
            await ctx.send(f"Cannot find guild with name: {guild_name}")
            return
        await targetGuild.text_channels[0].send(
            "@here the owner has removed me from this server forcefully"
        )
        await targetGuild.text_channels[0].send(
            "If You Want to appeal this removel dm ShowierData9978#3454"
        )
        await targetGuild.leave()
        await ctx.send(f":+1: Left guild: {targetGuild.name} with id {targetGuild.id}")


class fun(commands.Cog, name="Commands that are fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Meme", pass_context=True)
    async def meme(self, ctx):
        embed = Embed(title="", description="")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                "https://www.reddit.com/r/dankmemes/new.json?sort=hot"
            ) as r:
                res = await r.json()
                embed.set_image(
                    url=res["data"]["children"][random.randint(0, 25)]["data"]["url"]
                )
                await ctx.send(embed=embed)

    @commands.command(name="randomNum")
    async def RadomNum(self, ctx):
        await ctx.send(random.randint(1, 10000))

    @commands.command(name="Guess", pass_context=True)
    async def command(self, ctx):
        computer = random.randint(1, 10)
        await ctx.send("Guess my number , 1 to 10")

        def check(msg):
            return (
                msg.author == ctx.author
                and msg.channel == ctx.channel
                and int(msg.content) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            )

        msg = await self.bot.wait_for("message", check=check)

        if int(msg.content) == computer:
            await ctx.send("Correct")
        else:
            await ctx.send(f"Nope it was {computer}")

    @commands.command("rank")
    async def rank(self, ctx, member: nextcord.member = None):
        with open("users.json", "r") as users:
            users = json.load(users)
            if member is None:
                userlvl = users[f"{ctx.author.id}"]["level"]
                await ctx.send(f"{ctx.author.mention} You are at level {userlvl}!")
            else:
                userlvl2 = users[f"{ctx.author.id}"]["level"]
                await ctx.send(f"{ctx.author.mention} is at level {userlvl2}!")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self} has been loaded")
        global startTime
        startTime = time.time()

    # create a command in the cog
    @commands.command(name="Uptime")
    async def _uptime(self, ctx):

        # what this is doing is creating a variable called 'uptime' and assigning it
        # a string value based off calling a time.time() snapshot now, and subtracting
        # the global from earlier
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - startTime))))
        await ctx.send(uptime)

    @commands.command("30day")
    async def q30day(self, ctx):
        await ctx.send("You GOT IT")


def setup(bot):

    bot.add_cog(Command(bot))
    bot.add_cog(DevCommands(bot))
    bot.add_cog(fun(bot))
