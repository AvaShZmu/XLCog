import os
import discord
from discord.ext import commands
import Classes.Bot_Class
import logging
import asyncio
import sys

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

TOKEN = "INSERT YOUR DISCORD APP'S TOKEN HERE"

bot = Classes.Bot_Class.Bot()


# BOT EVENTS


@bot.event  # MESSAGES
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.bot:
        return


    if 'skibidi' in message.content.lower():
        await message.channel.send('skibidi dom dom dom yes yes, skibidi dabadu yipp yipp')



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You are not allowed to use this command.')


bot.run(TOKEN, log_handler=handler)
