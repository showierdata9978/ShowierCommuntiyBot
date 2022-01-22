from nextcord.ext import commands
from nextcord import Embed
import aiohttp
import sys
import random
import nextcord
import json

class Command(commands.Cog, name="normal commands"):
	def __init__(self, bot):
	    self.bot = bot	
	@commands.command(name="ping")
	async def ping(self, ctx):
	    self.ctx = ctx
	    await self.ctx.send(f"The Bots Ping is {round(ctx.bot.latency,1)}, The server name is {ctx.guild}")
	    return "done"
	@commands.command(name="Announce",AdminsOnly = True)

	async def announce(self, ctx,*,message):	
		self.announsment = []
		for channel in ctx.Guild.channels:
			if channel.isinstance(channel, nextcord.announcementchanel):
				self.announsment.append(channel)
		self.channel = ctx.bot.get_channel(self.announsment[1].id)
		await self.channel.send(f"@everyone {message}")


class DevCommands(commands.Cog, name='Developer Commands'):
    '''These are the developer commands'''

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        return ctx.author.id == self.bot.author_id

    @commands.command(  # Decorator to declare where a command is.
        name='reload',  # Name of the command, defaults to function name.
        aliases=['rl']  # Aliases for the command.
    )
    async def reload(self, ctx, cog):
        '''
        Reloads a cog.
        '''
        extensions = self.bot.extensions  # A list of the bot's cogs/extensions.
        if cog == 'all':  # Lets you reload all cogs at once
            for extension in extensions:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            await ctx.send('Done')
        if cog in extensions:
            self.bot.unload_extension(cog)  # Unloads the cog
            self.bot.load_extension(cog)  # Loads the cog
            await ctx.send('Done')  # Sends a message where content='Done'
        else:
            await ctx.send('Unknown Cog')  # If the cog isn't found/loaded.

    @commands.command(name="unload", aliases=['ul'])
    async def unload(self, ctx, cog):
        '''
        Unload a cog.
        '''
        extensions = self.bot.extensions
        if cog not in extensions:
            await ctx.send("Cog is not loaded!")
            return
        self.bot.unload_extension(cog)
        await ctx.send(f"`{cog}` has successfully been unloaded.")

    @commands.command(name="load")
    async def load(self, ctx, cog):
        '''
        Loads a cog.
        '''
        try:

            self.bot.load_extension(cog)
            await ctx.send(f"`{cog}` has successfully been loaded.")

        except commands.errors.ExtensionNotFound:
            await ctx.send(f"`{cog}` does not exist!")

    @commands.command(name="listcogs", aliases=['lc'])
    async def listcogs(self, ctx):
        '''
        Returns a list of all enabled commands.
        '''
        base_string = "```css\n"  # Gives some styling to the list (on pc side)
        base_string += "\n".join([str(cog) for cog in self.bot.extensions])
        base_string += "\n```"
        await ctx.send(base_string)

    @commands.command(name="Shutoff", aliases=['ShutDown', 'TurnOff', 'poweroff', 'Sd'])
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
class fun(commands.Cog, name='Commands that are fun'):
    def __init__(self, bot):
    	self.bot = bot

   
    @commands.command(name = "Meme",pass_context=True)
    async def meme(self,ctx):
        embed = Embed(title="", description="")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)
    @commands.command(name = "randomNum")
    async def RadomNum(self,ctx):
        await ctx.send(random.randint(1,10000))
    @commands.command(name="Guess",pass_context=True)
    async def command(self,ctx):
        computer = random.randint(1, 10)
        await ctx.send('Guess my number , 1 to 10')

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and int(msg.content) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        msg = await self.bot.wait_for("message", check=check)

        if int(msg.content) == computer:
            await ctx.send("Correct")
        else:
            await ctx.send(f"Nope it was {computer}")
class Econemy(commands.Cog, name='Econemy commands'):
		@commands.command()
		async def balance(self,ctx):
			await self.open_account(ctx.author)

			user = ctx.author

			users = await self.get_bank_data()
		
			wallet_amt= users[str(user.id)]["Wallet"]
			bank_amt= users[str(user.id)]["Bank"]


			em = nextcord.Embed(title=f"{ctx.author.name}'s balance.", color=nextcord.Color.teal()) 
			em.add_field(
				name="Wallet Balance",value=wallet_amt
			)
			em.add_field(
				name="Bank Balance",value=bank_amt
			)
			await ctx.send(embed=em)

		async def open_account(self,user):
			users = await self.get_bank_data()
		
			if str(user.id) in users:
				return False
			else:
				users[str(user.id)] = {}
				users[str(user.id)]["Wallet"] = 0
				users[str(user.id)]["Bank"] = 0
		
			with open("bank.json",'w') as f:
				users = json.dump(users,f)
			return True

		async def get_bank_data(self):
				with open("bank.json",'r') as f:
					users = json.load(f)
				return users

		@commands.command()
		async def beg(self,ctx):
			await self.open_account(ctx.author)

			user = ctx.author


			users = await self.get_bank_data()

			earnings = random.randrange(101)
			await ctx.send(f"Someone gave your {earnings} coins")

			users[str(user.id)]["Wallet"] += earnings

			with open("bank.json",'w') as f:
				users = json.dump(users,f)



def setup(bot):
    
	bot.add_cog(Command(bot))
	bot.add_cog(DevCommands(bot))
	bot.add_cog(fun(bot))
	bot.add_cog(Econemy(bot))
