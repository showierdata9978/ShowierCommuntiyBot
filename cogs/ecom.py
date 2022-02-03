import nextcord as discord
from nextcord.ext import commands, tasks
import asyncio
from itertools import cycle
import os
import json
import random






####################################################################
####################################################################
# Main code starts :)
class Ecom(commands.Cog,name="ecom reborn"):
    def __init__(self,bot:commands.Bot) -> None:
       self.mainshop = [{"name":"Watch","price":100,"description":"Time"},
                {"name":"Laptop","price":1000,"description":"Work"},
                {"name":"PC","price":10000,"description":"Gaming"},
                {"name":"Ferrari","price":99999,"description":"Sports Car"}]
       self.bot = bot

    @commands.command(aliases=['bal'])
    async def balance(self,ctx):
        await self.open_account(ctx.author)
        user = ctx.author

        users = await self.get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        em = discord.Embed(title=f'{ctx.author.name} Balance',color = discord.Color.red())
        em.add_field(name="Wallet Balance", value=wallet_amt)
        em.add_field(name='Bank Balance',value=bank_amt)
        await ctx.reply(embed= em)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self,ctx):
        await self.open_account(ctx.author)
        user = ctx.author

        users = await self.get_bank_data()

        earnings = random.randrange(101)

        await ctx.send(f'{ctx.author.mention} Got {earnings} coins!!')

        users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json",'w') as f:
            json.dump(users,f)


    @commands.command(aliases=['wd'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def withdraw(self,ctx,amount = None):
        await self.open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter the amount")
            return

        bal = await self.update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[1]:
            await ctx.send('You do not have sufficient balance')
            return
        if amount < 0:
            await ctx.send('Amount must be positive!')
            return

        await self.update_bank(ctx.author,amount)
        await self.update_bank(ctx.author,-1*amount,'bank')
        await ctx.send(f'{ctx.author.mention} You withdrew {amount} coins')


    @commands.command(aliases=['dp'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def deposit(self,ctx,amount = None):
        await self.open_account(ctx.author)
        if amount == None:
            await ctx.reply("Please enter the amount")
            return

        bal = await self.update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[0]:
            await ctx.reply('You do not have sufficient balance')
            return
        if amount < 0:
            await ctx.reply('Amount must be positive!')
            return

        await self.update_bank(ctx.author,-1*amount)
        await self.update_bank(ctx.author,amount,'bank')
        await ctx.reply(f'{ctx.author.mention} You deposited {amount} coins')


    @commands.command(aliases=['sm'])
    async def send_message(self,ctx,member : discord.Member,amount = None):
        await self.open_account(ctx.author)
        await self.open_account(member)
        if amount == None:
            await ctx.reply("Please enter the amount")
            return

        bal = await self.update_bank(ctx.author)
        if amount == 'all':
            amount = bal[0]

        amount = int(amount)

        if amount > bal[0]:
            await ctx.reply('You do not have sufficient balance')
            return
        if amount < 0:
            await ctx.send('Amount must be positive!')
            return

        await self.update_bank(ctx.author,-1*amount,'bank')
        await self.update_bank(member,amount,'bank')
        await ctx.send(f'{ctx.author.mention} You gave {member} {amount} coins')

    @commands.cooldown(1, 100000, commands.BucketType.user)
    @commands.command(aliases=['rb'])
    async def rob(self,ctx,member : discord.Member):
        await self.open_account(ctx.author)
        await self.open_account(member)
        bal = await self.update_bank(member)


        if bal[0]<100:
            await ctx.send('It is useless to rob him :(')
            return

        earning = random.randrange(0,bal[0])

        await self.update_bank(ctx.author,earning)
        await self.update_bank(member,-1*earning)
        await ctx.send(f'{ctx.author.mention} You robbed {member} and got {earning} coins')


    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def slots(self,ctx,amount = None):
        await self.open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter the amount")
            return

        bal = await self.update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[0]:
            await ctx.send('You do not have sufficient balance')
            return
        if amount < 0:
            await ctx.send('Amount must be positive!')
            return
        final = []
        for i in range(3):
            a = random.choice(['X','O','Q'])

            final.append(a)

        await ctx.send(str(final))

        if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
            await self.update_bank(ctx.author,2*amount)
            await ctx.send(f'You won :) {ctx.author.mention}')
        else:
            await self.update_bank(ctx.author,-1*amount)
            await ctx.send(f'You lose :( {ctx.author.mention}')


    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def shop(self,ctx):
        em = discord.Embed(title = "Shop")

        for item in self.mainshop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name = name, value = f"${price} | {desc}")

        await ctx.send(embed = em)



    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def buy(self,ctx,item,amount = 1):
        await self.open_account(ctx.author)

        res = await self.buy_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send("That Object isn't there!")
                return
            if res[1]==2:
                await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
                return


        await ctx.send(f"You just bought {amount} {item}")


    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def bag(self,ctx):
        await self.open_account(ctx.author)
        user = ctx.author
        users = await self.get_bank_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []


        em = discord.Embed(title = "Bag")
        for item in bag:
            name = item["item"]
            amount = item["amount"]

            em.add_field(name = name, value = amount)    

        await ctx.send(embed = em)


    async def buy_this(self,user,item_name,amount):
        item_name = item_name.lower()
        name_ = None
        for item in self.mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                price = item["price"]
                break

        if name_ == None:
            return [False,1]

        cost = price*amount

        users = await self.get_bank_data()

        bal = await self.update_bank(user)

        if bal[0]<cost:
            return [False,2]


        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt + amount
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t = 1
                    break
                index+=1 
            if t == None:
                obj = {"item":item_name , "amount" : amount}
                users[str(user.id)]["bag"].append(obj)
        except:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"] = [obj]        

        with open("mainbank.json","w") as f:
            json.dump(users,f)

        await self.update_bank(user,cost*-1,"wallet")

        return [True,"Worked"]


    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def sell(self,ctx,item,amount = 1):
        await self.open_account(ctx.author)

        res = await self.update_bank(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send("That Object isn't there!")
                return
            if res[1]==2:
                await ctx.send(f"You don't have {amount} {item} in your bag.")
                return
            if res[1]==3:
                await ctx.send(f"You don't have {item} in your bag.")
                return

        await ctx.send(f"You just sold {amount} {item}.")

    async def update_bank(self,user,item_name,amount,price = None):
        item_name = item_name.lower()
        name_ = None
        for item in self.mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                if price==None:
                    price = 0.7* item["price"]
                break

        if name_ == None:
            return [False,1]

        cost = price*amount

        users = await self.get_bank_data()

        bal = await self.update_bank(user)


        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt - amount
                    if new_amt < 0:
                        return [False,2]
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t = 1
                    break
                index+=1 
            if t == None:
                return [False,3]
        except:
            return [False,3]    

        with open("mainbank.json","w") as f:
            json.dump(users,f)

        await self.update_bank(user,cost,"wallet")

        return [True,"Worked"]


    @commands.command(aliases = ["lb"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def leaderboard(self,ctx,x = 1):
        users = await self.get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total,reverse=True)    

        em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = ctx.server.get_member(id_)
            name = member.name
            em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
            if index == x:
                break
            else:
                index += 1

        await ctx.send(embed = em)


    async def open_account(self,user):

        users = await self.get_bank_data()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0

        with open('mainbank.json','w') as f:
            json.dump(users,f)

        return True


    async def get_bank_data(self):
        with open('mainbank.json','r') as f:
            users = json.load(f)

        return users


    async def update_bank(self,user,change=0,mode = 'wallet'):
        users = await self.get_bank_data()

        users[str(user.id)][mode] += change

        with open('mainbank.json','w') as f:
            json.dump(users,f)
        bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
        return bal

def setup(bot):
    bot.add_cog(Ecom(bot))
