import discord


class textvoice(discord.ui.View):
    def __init(self, timeout=10):
        super().__init__(timeout=timeout)
        self.state = None

    @discord.ui.button(label="Text", style=discord.ButtonStyle.green)
    async def text(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.state = 'text'
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label="Voice", style=discord.ButtonStyle.blurple)
    async def voice(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.state = 'voice'
        await interaction.response.defer()
        self.stop()