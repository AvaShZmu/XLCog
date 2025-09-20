import logging
import os
import discord
from discord.ext import commands
from Classes.Help_Class import MyHelpCommand
import wavelink



class Bot(commands.Bot):
    def __init__(self) -> None:
        intents: discord.Intents = discord.Intents.default()
        intents.message_content = True

        discord.utils.setup_logging(level=logging.INFO)
        super().__init__(command_prefix="b!", intents=intents)

    async def load_extensions(self):
        # Load all Functions from the Functions folder
        cogs_dir = os.path.join(os.path.dirname(__file__), '..', 'Functions')
        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py"):
                try:
                    # Await the load_extension coroutine
                    await self.load_extension(f"Functions.{filename[:-3]}")
                    logging.info(f"Loaded {filename[:-3]}")
                except Exception as e:
                    logging.info(f"Failed to load {filename[:-3]}: {e}")
    async def setup_hook(self) -> None:
        nodes = [wavelink.Node(uri="LAVALINK SERVER URI:PORT", password="PASSWORD", inactive_player_timeout=120)]
        # http://localhost:2333

        # cache_capacity is EXPERIMENTAL. Turn it off by passing None
        await wavelink.Pool.connect(nodes=nodes, client=self, cache_capacity=100)

    async def on_ready(self) -> None:
        logging.info("Logged in: %s | %s", self.user, self.user.id)
        await self.load_extensions()
        self.help_command = MyHelpCommand()
        logging.info("XLCog has connected to Discord!")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name="Kenshi Yonezu")) #goated

    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        logging.info("Wavelink Node connected: %r | Resumed: %s", payload.node, payload.resumed)