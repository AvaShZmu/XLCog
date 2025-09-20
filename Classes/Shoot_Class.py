import discord


class Shoot(discord.ui.View):
    def __init__(self, person, chance, timeout=8):
        super().__init__(timeout=timeout)
        self.person = person
        self.chance = chance
        if self.chance:
            self.dodge = 'bad'
        else:
            self.dodge = 'good'

    @discord.ui.button(label="DODGE!!!", style=discord.ButtonStyle.blurple)
    async def dodge(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.person:
            await interaction.response.defer()
            if self.chance:
                self.dodge = 'good'
            else:
                self.dodge = 'bad'
            self.stop()
        else:
            await interaction.response.send_message("You dodged thin air, sweety!", ephemeral=True)
            self.stop()
