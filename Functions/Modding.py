from discord.ext import commands
from Classes.TextVoice_Class import textvoice
import discord


class Modding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create-channel', help = "Creates a text/voice channel (mods only)")  # creating channels
    @commands.has_role("Ruler of XLCog")
    async def create_channel(self, ctx):
        guild = ctx.guild
        view = textvoice()
        await ctx.send("Do you want to create a text channel or a voice channel?", view=view)
        await view.wait()
        if view.state is not None:
            await ctx.send("What shall be the name of the channel?")
            channel_name = await ctx.bot.wait_for('message', check=lambda
                message: message.author == ctx.author and message.channel == ctx.channel)
            existing_channel = discord.utils.get(guild.channels, name=channel_name.content)
            if not existing_channel:
                await ctx.send(f'Creating {view.state} channel: {channel_name.content}')
                if view.state == 'text':
                    await guild.create_text_channel(channel_name.content)
                else:
                    await guild.create_voice_channel(channel_name.content)
                await ctx.send(f'Created {view.state} channel: {channel_name.content}')
            else:
                await ctx.send(f'Channel {channel_name.content} already exists')
        else:
            await ctx.send('Interaction Timeout.')

    @commands.command()
    async def purge(self, ctx, number: int):
        if ctx.author.name != "avalancheshockz":
            return
        if number > 400:
            number = 400
        async with ctx.typing():
           deleted = await ctx.channel.purge(limit=number)
        await ctx.send(f"Deleted {len(deleted) - 1} messages.")
async def setup(bot):
    await bot.add_cog(Modding(bot))
