import discord
from discord.ext import commands


class TextFileConverter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="convert", help = "!convert [file name] [file content]")
    async def convert(self, ctx, name, *, input: str):
        await ctx.message.delete()
        with open("text_convert.txt", 'w') as f:
            f.write(input)
        await ctx.send(file=discord.File('text_convert.txt', filename=name))


async def setup(bot):
    await bot.add_cog(TextFileConverter(bot))
