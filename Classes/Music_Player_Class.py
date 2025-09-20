import discord
import asyncio

def timeformat(inp: int):
    seconds = inp // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    if hours <= 0:
        return f"{minutes}:{remaining_seconds:02d}"
    else:
        return f"{hours}:{minutes:02d}:{remaining_seconds:02d}"


class Queue_Button(discord.ui.View):
    def __init__(self, page_limit, item_number, current_page, embed, player, title_length_max, mess, timeout=60):
        super().__init__(timeout=timeout)
        self.page_limit = page_limit
        self.current_page = current_page
        self.item_number = item_number
        self.embed = embed
        self.pages = (item_number // page_limit) + (1 if item_number % page_limit else 0)
        self.player = player
        self.mess = mess
        self.title_length_max = title_length_max
        self.check_status()  # Initial check for button states

    @discord.ui.button(label="|<", style=discord.ButtonStyle.gray)
    async def prev_most(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 1:
            self.current_page = 1
            self.update_embed_content()
            self.check_status()  # Update button states
            await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label="<", style=discord.ButtonStyle.gray)
    async def prev(self, interaction: discord.Interaction, button: discord.ui.Button):
        # if interaction.user != self.author:
        #     await interaction.response.send_message("Only the command invoker can view the queue.", ephemeral=True)
        #     return
        if self.current_page > 1:
            self.current_page -= 1
            self.update_embed_content()
            self.check_status()  # Update button states
            await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label=">", style=discord.ButtonStyle.gray)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.pages:
            self.current_page += 1
            self.update_embed_content()
            self.check_status()  # Update button states
            await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label=">|", style=discord.ButtonStyle.gray)
    async def next_most(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.pages:
            self.current_page = self.pages
            self.update_embed_content()
            self.check_status()  # Update button states
            await interaction.response.edit_message(embed=self.embed, view=self)

    def update_embed_content(self):
        start_index = (self.current_page - 1) * self.page_limit
        end_index = min(start_index + self.page_limit, self.item_number)

        queue_list = []
        for i in range(start_index, end_index):
            original_title = self.player.queue[i].title
            title = original_title  # Default to original title

            if len(original_title) > self.title_length_max:
                # Truncate and add ellipsis
                title = original_title[:self.title_length_max] + "..."  # Simple truncation

            if self.player.queue[i].is_stream:
                queue_list.append(
                    f"**{i + 1}.** [{title}]({self.player.queue[i].uri}) 🔴 - {self.player.queue[i].author}")
            else:
                queue_list.append(f"**{i + 1}.** [{title}]({self.player.queue[i].uri}) [{timeformat(self.player.queue[i].length)}] - {self.player.queue[i].author}")

        queue_string = "\n".join(queue_list)
        self.embed.set_field_at(index=1, name="Current queue:", value=queue_string, inline=False)
        self.embed.set_footer(
            text=f"{len(self.player.queue) + 1} track(s) | Page {self.current_page}/{self.pages}")

    def check_status(self):
        self.children[0].disabled = (self.current_page == 1)  # Disable "First" if on the first page
        self.children[1].disabled = (self.current_page == 1)  # Disable "Previous" if on the first page
        self.children[2].disabled = (self.current_page == self.pages)  # Disable "Next" if on the last page
        self.children[3].disabled = (self.current_page == self.pages)  # Disable "Last" if on the last page

    async def on_timeout(self) -> None:
        self.children[0].disabled = True
        self.children[1].disabled = True
        self.children[2].disabled = True
        self.children[3].disabled = True
        await self.mess.edit(content="The interaction has timed out.", embed=self.embed, view=self)


# YT SEARCH
class DropDown(discord.ui.Select):
    def __init__(self, lOption, author):
        self.lOption = lOption
        self.author = author
        # Set the options that will be presented inside the dropdown
        options = []
        for i in lOption:
            options.append(discord.SelectOption(label=i))
        options.append(discord.SelectOption(label="Nevermind."))

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select a suggestion', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour of choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        if interaction.user != self.author:
            await interaction.response.send_message("Only the command invoker can choose.", ephemeral=True)

        if self.values[0] == "Nevermind.":
            self.view.stop()
            return
        await interaction.message.edit(view=None)
        self.view.selected = int(self.values[0][0]) - 1
        self.view.stop()


class Selector(discord.ui.View):
    def __init__(self, lOptions, author, timeout=30):
        super().__init__(timeout=timeout)
        self.selected = None
        self.add_item(DropDown(lOptions, author))
