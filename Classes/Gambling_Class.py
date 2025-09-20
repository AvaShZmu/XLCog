import discord


class Gambling(discord.ui.View):
    def __init__(self, person, timeout=20):
        super().__init__(timeout=timeout)
        self.interacted = False
        self.person = person

    @discord.ui.button(label="Roll", style=discord.ButtonStyle.green)
    async def roll(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.person:
            await interaction.response.send_message("Rolling...")
            self.interacted = True
            self.stop()
        else:
            await interaction.response.send_message("stfu", ephemeral=True)
