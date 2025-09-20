from discord.ext import commands


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def checkping(self, ctx):
        await ctx.send(f"My ping is: **{round(self.bot.latency * 1000)}ms**")

    @commands.command()
    async def version(self, ctx):
        await ctx.send(f"Last updated: <t:1730998020:R>\nCHATBOT FUNCTION OFFICIALLY OUT!\n- Use !startchat to do freaky stuff with XLCog.\n- Use !generate <prompt> to generate an image based on the given prompt.\n(This is still in development, expect bugs.)")


async def setup(bot):
    await bot.add_cog(Debug(bot))
