import discord


class WannaPlay(discord.ui.View):
    def __init__(self, person, timeout=15):
        super().__init__(timeout=timeout)
        self.person = person
        self.play = False

    @discord.ui.button(label="LET'S DANCE", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.person:
            self.play = True
            await interaction.response.defer()
            self.stop()
        else:
            await interaction.response.send_message("You're not him", ephemeral=True)

    @discord.ui.button(label="Nah", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.person:
            self.play = False
            await interaction.response.send_message("You will not be joining", ephemeral=True)
            self.stop()
        else:
            await interaction.response.send_message("You're not him", ephemeral=True)
