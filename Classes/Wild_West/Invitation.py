import discord
import asyncio


class WWInvite(discord.ui.View):
    def __init__(self, embed, bounty, ctx, timeout=20):
        super().__init__(timeout=timeout)
        self.accept = False
        self.embed = embed
        self.person = ''
        self.bounty = bounty
        self.ctx = ctx
    @discord.ui.button(label="Join", style=discord.ButtonStyle.blurple)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.ctx.author.id == interaction.user.id:
            await interaction.response.send_message("You can't play yourself.", ephemeral=True)
        else:
            self.accept = True
            self.person = interaction.user
            await interaction.response.defer()
            if not self.bounty.get(self.person.id, False):
                self.bounty[self.person.id] = 10000
            self.embed.add_field(name=f"{self.person.name}'s bounty: ", value=f"{self.bounty[self.person.id]}$", inline=False)
            self.stop()
