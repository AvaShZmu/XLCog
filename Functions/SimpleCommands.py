import discord
from discord.ext import commands
import random
import asyncio
from Classes.JJK_Class import JJK
from Bot_Data.Data_Variables import kiss


class SimpleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='roll_dice', help='Stimulates rolling dice')
    async def roll_dice(self, ctx, number_of_sides: int, number_of_roles: int):
        dice = [str(random.choice(range(1, number_of_sides + 1))) for i in range(number_of_roles)]
        await ctx.send(', '.join(dice))

    @commands.command(name="pp", help = "Evaluate one's pp size")
    async def ppsize(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        if user == self.bot.user or user.name == "avalancheshockz":
            mid = "=" * 10
            pps = "8" + mid + "D"
            mes = await ctx.send(f"{user.mention}'s pp:\n{pps}")
            for i in range(1, 12):
                mid += "==="
                pps = "8" + mid + "D"
                await mes.edit(content=f"{user.mention}'s pp:\n{pps}")
                await asyncio.sleep(1)
        elif user.name == "lknaa":
            pps = "8" + "=" * 0 + "D"
            await ctx.send(f"{user.mention}'s pp:\n{pps}")
        else:
            pps = "8" + "=" * random.randint(0, 20) + "D"
            await ctx.send(f"{user.mention}'s pp:\n{pps}")

    @commands.command(name='jjk', brief="Gojo vs Sukuna",
                      description="The strongest sorcerer in history vs the strongest sorcerer of today.")
    async def jjk(self, ctx):
        view = JJK()
        await ctx.reply("Gojo or Sukuna", view=view)

    @commands.command(name="kiss", help = "Kisses someone.")
    async def kissy(self, ctx, user: discord.User):
        kiss_embed = discord.Embed(
            colour=discord.Colour.lighter_gray(),
            description=f"{ctx.author.mention} gave {user.mention} a loving kiss :3"
        )
        kiss_embed.set_image(url=random.choice(kiss))
        await ctx.send(embed=kiss_embed)


    @commands.command(name="pfp", help = "Fetches an user's profile picture.")
    async def profile(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(title=f"{user.name}'s pfp:", colour=discord.Colour.lighter_gray())
        embed.set_author(name=f"Started by {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.set_image(url=user.avatar.url)
        await ctx.send(embed=embed)



    @commands.command(name="ping")
    async def shadow(self, ctx, user: discord.User = None):
        await ctx.message.delete()
        if user is None:
            await ctx.send("@everyone")
            print(f"Culprit: {ctx.author}")
        else:
            await ctx.send(user.mention)
        if ctx.author.name == "avalancheshockz":
            return
        if random.randint(1,4) == 4:
            await ctx.send(f"The culprit is {ctx.author.mention} you little snitch")



async def setup(bot):
    await bot.add_cog(SimpleCommands(bot))
