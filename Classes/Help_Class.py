from discord.ext import commands
import discord


class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(colour=discord.Color.lighter_gray(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)
