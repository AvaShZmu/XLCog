from Bot_Data.Data_Variables import bot_avatar
from Classes.WannaPlay_Class import WannaPlay
from Classes.Gambling_Class import Gambling
from discord.ext import commands
import discord
import asyncio
import random


class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def embed_send(self, ctx, embed, content, view=None):
        embed.description = content
        await ctx.send(embed=embed, view=view)

    async def gamble_get_bound(self, ctx, gamble_embed, *args):

        try:
            type = "high"
            lower_bound = int(args[0])
        except IndexError:
            type = "low"

        gamble_embed.description = f"Pick a {type}er bound, {ctx.author.mention}! (Integer)"
        gamble_embed.set_author(name="Select bound", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=gamble_embed)

        while True:
            try:
                bound_message = await ctx.bot.wait_for("message", check=lambda
                    i: i.author == ctx.author and i.channel == ctx.channel, timeout=10)
                bound = int(bound_message.content)
                if type == "low":
                    return bound
                else:
                    if bound > lower_bound:
                        return bound
                    else:
                        gamble_embed.description = "The upper bound has to be greater than the lower bound"
                        await ctx.send(embed=gamble_embed)
            except ValueError:

                gamble_embed.description = "Input a cogging integer"
                await ctx.send(embed=gamble_embed)

            except asyncio.TimeoutError:
                bound = 0
                if type == "high":
                    bound = lower_bound + 100
                gamble_embed.description = f"{type}er bound value will be set to 0 by default"
                await ctx.send(embed=gamble_embed)
                return bound

    async def number_roll(self, ctx, gamble_embed, low, high, *args):
        try:
            target = args[0]
        except IndexError:
            target = ctx.author

        roll = Gambling(target)

        await self.embed_send(ctx, gamble_embed, f"{target.mention}, roll! roll! roll!!!", view=roll)

        await roll.wait()
        if roll.interacted:

            lucky_number = random.randint(low, high)
            await self.embed_send(ctx, gamble_embed, f"Lucky number: {lucky_number}")
            return lucky_number
        else:

            await self.embed_send(ctx, gamble_embed, f"Bitch since you don't wanna play your number is cogging {low-1}")
            lucky_number = low - 1
            return lucky_number

    async def calculate_result(self, ctx, user, luck_num_ctx, luck_num_user, gamble_embed):
        if luck_num_ctx > luck_num_user:

            gamble_embed.description = f"Yo {ctx.author.mention} you win, gambling king"
            gamble_embed.set_author(name="You Win!", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=gamble_embed)

        elif luck_num_ctx < luck_num_user:

            gamble_embed.description = f"Yo {user.mention} you win, gambling king"
            gamble_embed.set_author(name="You win!", icon_url=user.avatar.url)
            await ctx.send(embed=gamble_embed)

        else:

            gamble_embed.description = "Tie"
            gamble_embed.set_author(name="Tie", icon_url=bot_avatar)
            await ctx.send(embed=gamble_embed)
    @commands.command(name='gamble', brief="(Ping one user) Gamble your life away~")
    async def lucky_number(self, ctx, user: discord.User):
        if user == self.bot.user:
            await ctx.send("You cannot simply challenge the master.")
            return
        gamble_embed = discord.Embed(
            description=f"Do you wanna play, {user.mention}?",
            colour=discord.Colour.lighter_gray()
        )
        accept = WannaPlay(user)

        gamble_embed.set_author(name="Gambling", icon_url=bot_avatar)
        await ctx.send(embed=gamble_embed, view=accept)
        await accept.wait()
        if accept.play:

            await self.embed_send(ctx, gamble_embed, f"{user.mention} will be joining! YEAHH GAMBLING")

            await asyncio.sleep(2)

            await self.embed_send(ctx, gamble_embed, "Welcome to GAMBLING!!1!")

            await asyncio.sleep(2)

            low = await self.gamble_get_bound(ctx, gamble_embed)

            await self.embed_send(ctx, gamble_embed, f"Lower bound: {low}")

            await asyncio.sleep(1)

            high = await self.gamble_get_bound(ctx, gamble_embed, low)

            await self.embed_send(ctx, gamble_embed, f"Upper bound: {high}")

            await asyncio.sleep(1)

            gamble_embed.set_author(name="Roll!", icon_url=ctx.author.avatar.url)

            await self.embed_send(ctx, gamble_embed, "GAMBLING! GAMBLING! GAMBLING")

            luck_num_ctx = await self.number_roll(ctx, gamble_embed, low, high)

            luck_num_user = await self.number_roll(ctx, gamble_embed, low, high, user)

            await self.calculate_result(ctx, user, luck_num_ctx, luck_num_user, gamble_embed)


        else:
            gamble_embed.description = f"{user.mention} won't be joining. What are you, scared of gambling?"
            await ctx.send(embed=gamble_embed)


async def setup(bot):
    await bot.add_cog(Gamble(bot))
