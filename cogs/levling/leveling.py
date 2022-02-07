import json
from .levelingfunc import setLvl
from nextcord.ext import commands


class Leveling(commands.Cog, name="LEVElS"):
    @commands.command("level")
    async def level(self, ctx):
        member = ctx.author
        if not member:
            id = ctx.message.author.id
            with open("users.json", "r") as f:
                users = json.load(f)
            lvl = users[str(id)]["level"]
            await ctx.send(f"You are at level {lvl}!")
        else:
            id = member.id
            with open("users.json", "r") as f:
                users = json.load(f)
            lvl = users[str(id)]["level"]
            await ctx.send(f"{member} is at level {lvl}!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlvl(ctx, *, user, lvl):
        with open("users.json", "r") as f:
            users = json.load(f)
        await setLvl(users, user, lvl)
        await ctx.send(f"set {user}`s level to {lvl}!")


def setup(bot):
    bot.add_cog(Leveling(bot))
