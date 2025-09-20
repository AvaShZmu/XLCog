from discord.ext import commands, tasks
from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError
import asyncio
import discord
import time


session_status = {}
models = {}
chats = {}
greetings = {}
last_message = {}


async def setup_client(token):
    client = await get_client(token=token)
    me = await client.account.fetch_me()
    print(f"Authenticated as @{me.username}")
    return client


class Chatbot(commands.Cog):
    def __init__(self, bot, client):
        self.bot = bot
        self.client = client
        self.timeout.start()

    async def setup_session(self, ctx):
        default = False
        try:
            chats[ctx.author.id], greetings[ctx.author.id] = await self.client.chat.create_chat(models[ctx.author.id])
        except Exception as e:
            models[ctx.author.id] = "zZ7o2lt_5rFlWpot5h_fo9sm3UTLtse6CRV0Sd06u3M" #default bc model
            chats[ctx.author.id], greetings[ctx.author.id] = await self.client.chat.create_chat(models[ctx.author.id])
            default = True
        return default

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not session_status.get(message.author.id, False):
            return
        if message.content.startswith(self.bot.command_prefix):
            return
        try:
            last_message[message.author.id] = (time.time(), message)
            async with message.channel.typing():
                answer = await self.client.chat.send_message(models[message.author.id],
                                                             chats[message.author.id].chat_id, message.content)
                ans_text = answer.get_primary_candidate().text
                if "b3017h" in ans_text:
                    ans_text = ans_text.replace("b3017h", "you")
                if ans_text == "":
                    ans_text = "[This content has been censored. Stop being freaky jesus christ.]"
                await message.reply(
                    f"「{greetings[message.author.id].author_name}」: {ans_text}")

        except SessionClosedError:
            await message.channel.send("Session closed. Bye!")
        except Exception as e:
            print(f"Error during message processing: {e}")

    @commands.command(name='startchat')
    async def start_chat(self, ctx):
        if ctx.author.id not in session_status:
            session_status[ctx.author.id] = False

        if session_status[ctx.author.id]:
            await ctx.send(
                f'Chat mode is already on! __MODEL: {greetings[ctx.author.id].author_name}__ [{ctx.author.mention}]')
            return

        await ctx.send("Insert a token:")

        async def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            # Wait for a message that meets the check criteria
            msg = await self.bot.wait_for('message', check=check, timeout=30)
            models[ctx.author.id] = msg.content
        except asyncio.TimeoutError:
            await ctx.send('Session aborted.')
            return
        default = await self.setup_session(ctx)
        if default:
            await ctx.send("Cannot fetch the given token. The model will be the default one.")
        await ctx.reply(
            f'Chat mode has been turned on! __MODEL: {greetings[ctx.author.id].author_name}__\n「{greetings[ctx.author.id].author_name}」: {greetings[ctx.author.id].get_primary_candidate().text}')
        session_status[ctx.author.id] = True
        last_message[ctx.author.id] = (time.time(), ctx.message)

    @commands.command(name='stopchat')
    async def stop_chat(self, ctx):
        if not session_status.get(ctx.author.id, False):
            await ctx.reply(f"Chat mode is already off!")
            return
        session_status[ctx.author.id] = False
        del last_message[ctx.author.id]
        await ctx.reply(f"Chat mode has been turned off!")

    @tasks.loop(seconds=30)
    async def timeout(self):
        current_time = time.time()
        for key in list(last_message.keys()):
            if current_time - last_message[key][0] > 120:
                await last_message[key][1].reply("Session aborted due to inactivity. (2 minutes)")
                session_status[key] = False
                del last_message[key]


    @commands.command()
    async def terminate(self, ctx, user: discord.User):
        if ctx.author.name != "avalancheshockz":
            await ctx.reply("You can't use this command.")
            return
        if not session_status.get(user.id, False):
            await ctx.reply(f"Nothing to terminate.")
            return
        session_status[user.id] = False
        await ctx.reply(f"{user.mention}'s chat session has been forcefully terminated!")


    @commands.command(name="generate")
    async def generate_image(self, ctx, *, prompt):
        async with ctx.typing():
            images = await self.client.utils.generate_image(prompt)
        print(f"generated images by the prompt \"{prompt}\": ")
        await ctx.send(images[0])



async def setup(bot):
    token = "CHATBOT TOKEN"
    await bot.add_cog(Chatbot(bot, await setup_client(token)))
