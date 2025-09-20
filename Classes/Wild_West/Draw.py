import asyncio
import discord


class Draw(discord.ui.View):
    def __init__(self, embed, mes, playerlist, timeout=20):
        super().__init__(timeout=timeout)
        self.embed = embed
        self.chosen = {}
        self.person = None
        self.shootable = False
        self.broke = False
        self.interacted = False
        self.playerlist = playerlist

    async def start_countdown(self, mes):
        for i in range(1, 6):
            if self.broke:
                self.embed.description = 'cog off'
                await mes.edit(embed=self.embed)
                break
            if i == 5:
                self.shootable = True
                self.embed.description = f'DRAW!'
                await mes.edit(embed=self.embed)
                break
            self.embed.description = f'Countdown: {5 - i}'
            await mes.edit(embed=self.embed)
            await asyncio.sleep(1)


    @discord.ui.button(label="DRAW", style=discord.ButtonStyle.blurple)
    async def draw(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.playerlist:
            if self.interacted:
                await interaction.response.send_message("One step too late.", ephemeral=True)
            else:
                self.interacted = True
                self.person = interaction.user
                if self.shootable:
                    self.chosen[interaction.user] = True
                    await interaction.response.defer()
                    await asyncio.sleep(1)
                    self.stop()
                else:
                    self.broke = True
                    self.chosen[interaction.user] = False
                    await interaction.response.defer()
                    await asyncio.sleep(1)
                    self.stop()
        else:
            await interaction.response.send_message("You're not in the round", ephemeral = True)
