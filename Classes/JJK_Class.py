import discord


class JJK(discord.ui.View):
    def __init__(self, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Gojo", style=discord.ButtonStyle.green)
    async def gojo(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Yo {interaction.user.mention} ur based", ephemeral=True)

    @discord.ui.button(label="Sukuna", style=discord.ButtonStyle.red)
    async def sukuna(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"{interaction.user.mention}. You swine. You vulgar little maggot. You worthless bag of filth. I wager "
            f"you couldn't empty a boot of excrement were the instructions on the heel. You are a canker. A sore that "
            f"won't go away. I would rather kiss a lawyer than be seen with you. Try to edit your responses of "
            f"unnecessary material before attempting to impress us with your insight. The evidence that you are a "
            f"nincompoop will still be available to readers, but they will be able to access it more rapidly.",
            ephemeral=True)
