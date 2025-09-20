from discord.ext import commands
import discord
import random
from discord import ui
import asyncio
import math

class RussianRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rrduel", help="Contributed by moonlight_gazer\nUse 'summon_wetpuss' to summon wetpuss. (wtf)")
    async def russianroulette(self, ctx, member: discord.Member = None, optionaltext=None):
        image_startrevolver = "https://media.istockphoto.com/id/1180397787/video/cinematic-dolly-shot-of-a-human-hand-holding-black-colored-revolver-gun-lit-with-golden-lights.jpg?s=640x640&k=20&c=qPnW6cw_QyzCkbuAMaxpmFnf1-t2Cdbvla5A5WjnSUk="
        image_spin = "https://images.pond5.com/hand-spinning-cylinder-357-magnum-086884139_prevstill.jpeg"
        image_shootself = "https://img.freepik.com/premium-photo/young-man-with-gun-is-preparing-commit-suicide-depression-with-fatal-outcome-guy-black-shirt-m_72464-1747.jpg?semt=ais_hybrid"
        image_shootopponent = "https://images.pond5.com/close-male-hand-firing-357-footage-065826653_iconl.jpeg"
        image_revolver = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/cb198cba-ed29-496a-b196-0911cab8a526/d5zb7w9-a43463fb-c11e-4711-b941-f5d1c2bd9fab.jpg/v1/fill/w_800,h_533,q_75,strp/revolver_porn_by_zorindenu_d5zb7w9-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NTMzIiwicGF0aCI6IlwvZlwvY2IxOThjYmEtZWQyOS00OTZhLWIxOTYtMDkxMWNhYjhhNTI2XC9kNXpiN3c5LWE0MzQ2M2ZiLWMxMWUtNDcxMS1iOTQxLWY1ZDFjMmJkOWZhYi5qcGciLCJ3aWR0aCI6Ijw9ODAwIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.BeXiwG9VvV5i02JmSgm6H27MFtutISg_l68omFreLUY"
        image_dead = "https://media.istockphoto.com/id/1157205911/photo/revolver-and-blood-on-black.jpg?s=612x612&w=0&k=20&c=nwRUuikPjfVNfnJmcYG8HkaTRZzKlrJEvGmdo0cUoYo="
        image_jammed = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJ5NTBsemoxdXVrbmZ4cHE2ZWN6OGl5bWpmYmd2cjBrdHRvczdsbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Jlv6kiW4hvIEyaVbPS/giphy.gif"
        image_fainted = "https://media.istockphoto.com/id/171351171/photo/nerd-athlete-lies-exhausted-in-green-grass.jpg?s=612x612&w=0&k=20&c=NAjJlKI7yzE74wiowbsAnQKtitZsZKuXY8mm39hDHXA="

        player = ctx.author
        opponent = member
        winner = None
        turn = 1
        turns_taken_all = 1
        triggerpulls = 0
        current_chamber = random.randrange(1, 7)
        death_chamber = random.randrange(1, 7)

        if member == None:
            opponent = player
            member = player

        # Set difficulty if bot
        bot_diff = None
        bot_peek = 0
        if optionaltext == "summon_wetpuss":
            await ctx.send(f"*Summoning WetPuss to possess the unfortunate soul of* {opponent.mention}")
            await asyncio.sleep(2)
            bot_diff = "hard"
            taunt_list = [
                "The gun knows who it belongs to—and it’s **not you**.",
                "Challenging me? You’re not playing to win; you’re playing to **die**.",
                "I don’t play Russian Roulette; I **own** it.",
                "Every spin bends to my will — don’t believe me? **Watch.**",
                "Go ahead, spin it. Fate already knows how this **ends.**",
                "I decide where the bullet lands, and it’s **never in my chamber.**",
                "This isn’t a game; it’s your **last mistake.**",
                "The revolver has one rule: **I never lose.**",
                "Step up, if you’re ready to meet a **god** and your end."
            ]
            await ctx.send("*Oh?*")
            await asyncio.sleep(2)
            await ctx.send(f"{taunt_list[random.randrange(0, len(taunt_list))]}")
            await asyncio.sleep(2)
        if member.bot == True and bot_diff == None:
            bot_diff = "easy"
            if member.name == "XLCog":
                bot_diff = "medium"
                big_cock_list = [
                    "cum",
                    "shut the cog up",
                    "im gooning dude",
                    f"guys {ctx.author.mention} likes femboy twinks",
                    "hey solve this before the match begins: 23 x 3 = ?",
                    "自害しろ",
                    "the king of curses drained all his efforts and energy because of his opponent who was very strong",
                    "479762",
                    "498130",
                    "308519",
                    "your foreskin is leaking",
                    "nah",
                    "help is not available, you are alone."
                    ]
                result = big_cock_list[random.randrange(0, len(big_cock_list))]
                if result == "nah":
                    await ctx.send(result)
                    await asyncio.sleep(2)
                    await ctx.send("```The game refused to begin. XLCog is busy bigging his cock.```")
                    return
                await ctx.send(result)
                await asyncio.sleep(2)

            elif member.name == "WetPuss":
                bot_diff = "hard"
                taunt_list = [
                    "The gun knows who it belongs to—and it’s **not you**.",
                    "Challenging me? You’re not playing to win; you’re playing to **die**.",
                    "I don’t play Russian Roulette; I **own** it.",
                    "Every spin bends to my will — don’t believe me? **Watch.**",
                    "Go ahead, spin it. Fate already knows how this **ends.**",
                    "I decide where the bullet lands, and it’s **never in my chamber.**",
                    "This isn’t a game; it’s your **last mistake.**",
                    "The revolver has one rule: **I never lose.**",
                    "Step up, if you’re ready to meet a **god** and your end."
                ]
                await ctx.send("*Oh?*")
                await asyncio.sleep(2)
                await ctx.send(f"{taunt_list[random.randrange(0, len(taunt_list))]}")
                await asyncio.sleep(2)
            else:
                taunt_list = [
                    "Let's spin some bad decisions into action!",
                    "Time to test if luck is on my side or just laughing at me.",
                    "One bullet, six chambers—let's see if math is my friend today.",
                    "I’ve always been a fan of high-stakes drama.",
                    "A loaded game for an empty soul.",
                    "Let’s hope my guardian angel isn’t on break.",
                    "Well, if I’m wrong, I won’t live to regret it.",
                    "You know, I've never lost a Russian Roulette duel before."
                ]
                await ctx.send(f"**{opponent.name}**: {taunt_list[random.randrange(0, len(taunt_list))]}")
                await asyncio.sleep(2)

        player_used_peek = False
        opponent_used_peek = False

        playershootcd = False
        opponentshootcd = False

        player_spin_finale = False
        opponent_spin_finale = False

        recently_jammed = False

        print(death_chamber)
        spin_decision = None
        shootwho = None
        roundlog = []

        print(ctx.author)
        print(member)

        if player == opponent:
            await ctx.send("help is available. you are not alone.")
        else:
            await ctx.send(f" {ctx.author.mention} challenged {member.mention} to a duel!")

        class SpinCylinder(ui.View):
            def __init__(self, user):
                super().__init__(timeout=10)  # Set timeout for the button view
                self.has_spun = False
                self.target = user
                self.triggerpulls = triggerpulls
                self.spin_decision = None

            @ui.button(label="Spin", style=discord.ButtonStyle.blurple)
            async def spin_button_clicked(self, interaction: discord.Interaction, button: ui.Button):
                if (interaction.user != self.target):
                    await interaction.response.send_message(
                        "The Dealer slapped your hand as you reached for their revolver.", ephemeral=True)
                    return
                # Reset trigger clicks
                self.triggerpulls = 0
                # Choose player's decision
                self.spin_decision = "spin"
                # Disable the button after it's clicked
                button.disabled = True
                await interaction.response.defer()

            @ui.button(label="No Spin", style=discord.ButtonStyle.red)
            async def nospin_button_clicked(self, interaction: discord.Interaction, button: ui.Button):
                if (interaction.user != self.target):
                    await interaction.response.send_message(
                        "The Dealer slapped your hand as you reached for their revolver.", ephemeral=True)
                    return
                # Choose player's decision
                self.spin_decision = "no spin"
                # Disable the button after it's clicked
                button.disabled = True
                await interaction.response.defer()

            @ui.button(label="Peek", style=discord.ButtonStyle.green)
            async def peek_button_clicked(self, interaction: discord.Interaction, button: ui.Button):
                if (interaction.user != self.target):
                    await interaction.response.send_message(
                        "The Dealer slapped you as you tried to peek at the chamber.", ephemeral=True)
                    return
                if (turn == 1 and not player_used_peek) or (turn == 2 and not opponent_used_peek):
                    # Choose player's decision
                    self.spin_decision = "no spin peek"
                    # Sneaky hint for the player
                    if current_chamber <= death_chamber:
                        await interaction.response.send_message(
                            f"As you peek into the chamber of the gun, you can see it is *{death_chamber - current_chamber + 1} pull(s) away* from going off.",
                            ephemeral=True)
                    else:
                        await interaction.response.send_message(
                            f"As you peek into the chamber of the gun, you can see it is *{death_chamber + 6 - current_chamber + 1} pull(s) away* from going off.",
                            ephemeral=True)
                    # Disable the button after it's clicked
                    button.disabled = True
                else:
                    await interaction.response.send_message("You can only peek once. Don't get too suspicious now.",
                                                            ephemeral=True)
                    return

            async def on_timeout(self):
                self.spin_decision = "no spin"

        class ShootWhoWithOpponent(ui.View):
            def __init__(self, holder, notholder):
                super().__init__(timeout=10)  # Set timeout for the button view
                self.holder = holder
                self.notholder = notholder
                self.shootwho = None

            @ui.button(label="Shoot Self", style=discord.ButtonStyle.blurple)
            async def spin_button_clicked(self, interaction: discord.Interaction, button: ui.Button):
                if (interaction.user != self.holder):
                    await interaction.response.send_message(
                        "The Dealer slapped your hand as you reached for their revolver.", ephemeral=True)
                    return
                # Choose player's decision
                self.shootwho = "self"
                # Disable the button after it's clicked
                button.disabled = True
                await interaction.response.defer()

            async def on_timeout(self):
                self.shootwho = "chicken"

            @ui.button(label="Shoot Opponent", style=discord.ButtonStyle.red)
            async def nospin_button_clicked(self, interaction: discord.Interaction, button: ui.Button):
                if (interaction.user != self.holder):
                    await interaction.response.send_message(
                        "The Dealer slapped your hand as you reached for their revolver.", ephemeral=True)
                    return
                # Choose player's decision
                self.shootwho = "opponent"
                # Disable the button after it's clicked
                button.disabled = True
                await interaction.response.defer()

        class ShootWhoWithoutOpponent(ui.View):
            def __init__(self, holder, notholder):
                super().__init__(timeout=10)  # Set timeout for the button view
                self.holder = holder
                self.notholder = notholder
                self.shootwho = None

            @ui.button(label="Shoot Self", style=discord.ButtonStyle.blurple)
            async def spin_button_clicked(self, interaction: discord.Interaction, button: ui.Button):
                if (interaction.user != self.holder):
                    await interaction.response.send_message(
                        "The Dealer slapped your hand as you reached for their revolver.", ephemeral=True)
                    return
                # Choose player's decision
                self.shootwho = "self"
                # Disable the button after it's clicked
                button.disabled = True
                await interaction.response.defer()

            async def on_timeout(self):
                self.shootwho = "chicken"

        ### MAIN PART ###
        if bot_diff == None or bot_diff == "easy":
            if player.name == opponent.name:
                gamescreen = discord.Embed(
                    title="Russian Roulette",
                    description=f"{player.mention} is feeling a bit suicidal today...",
                    color=0xFF5733
                )
            else:
                gamescreen = discord.Embed(
                    title="Russian Roulette Duel",
                    description=f"{player.mention} is challenging {opponent.mention} to a match of Russian Roulette!",
                    color=0xFF5733
                )
        else:
            if bot_diff == "medium":
                gamescreen = discord.Embed(
                    title="Russian Roulette Duel",
                    description=f"{player.mention} is challenging the **all-mighty** {opponent.mention} to a match of Russian Roulette!",
                    color=0xFF5733
                )
            elif bot_diff == "hard":
                gamescreen = discord.Embed(
                    title=f"{player.name}'s Demise",
                    description=f"*This will not end well for you,* {player.mention}.",
                    color=0xFF5733
                )

        async def update_screen():
            await ctx.send(embed=gamescreen)

        def clear_fields():
            for i in range(1, 10):
                gamescreen.remove_field(0)

        gamescreen.set_image(url=image_startrevolver)  # SET IMAGE

        msg = await ctx.send(embed=gamescreen)  # CREATES EMBED
        clear_fields()  # CLEARS FIELDS

        await msg.edit(embed=gamescreen, view=None)  # EDITS THE EMBED
        while not winner:
            print(current_chamber)
            clear_fields()

            if turns_taken_all == 10:
                gamescreen.add_field(name=f"Too long.", value=f"This is getting a bit boring, isn't it?", inline=False)
                await msg.edit(embed=gamescreen, view=None)  # EDITS THE EMBED
                await asyncio.sleep(2)
                gamescreen.add_field(name=f"You only have one spin from now on.", value=f"Use it well.", inline=False)
                await msg.edit(embed=gamescreen, view=None)  # EDITS THE EMBED
                triggerpulls = 0
                current_chamber = random.randrange(1, 7)
                roundlog.append(f"- *FINALE - EACH DUELER ONLY HAS ONE SPIN FORWARD* ")
                recently_jammed = False
                await asyncio.sleep(2)

            if turn == 1:
                # Player's Turn
                if recently_jammed:
                    if current_chamber == death_chamber:
                        gamescreen.add_field(name=f"{player}'s turn.", value=f"The gun **will** go off this round",
                                             inline=False)
                    else:
                        gamescreen.add_field(name=f"{player}'s turn.", value=f"The gun will **not** go off this round",
                                             inline=False)
                else:
                    gamescreen.add_field(name=f"{player}'s turn.",
                                         value=f"The gun has a {math.ceil(1 / (6 - triggerpulls) * 10000 * (5 / 6)) / 100}% chance of going off",
                                         inline=False)
                if player_spin_finale == False:
                    # Spin the cylinder?
                    spinview = SpinCylinder(player)

                    spin_decision = None
                    spinview.spin_decision = None
                    await msg.edit(embed=gamescreen, view=spinview)

                    while spin_decision == None:
                        await asyncio.sleep(0.25)
                        spin_decision = spinview.spin_decision

                    if spin_decision == "spin":
                        gamescreen.add_field(name=f"{player}'s turn.", value=f"{player} spins the cylinder...",
                                             inline=False)
                        triggerpulls = 0
                        recently_jammed = False
                        current_chamber = random.randrange(1, 7)
                        if turns_taken_all >= 10:
                            player_spin_finale = True
                        gamescreen.set_image(url=image_spin)  # EDIT IMAGE
                    else:
                        gamescreen.add_field(name=f"{player}'s turn.", value=f"{player} did not spin the cylinder.",
                                             inline=False)
                        gamescreen.set_image(url=image_revolver)  # EDIT IMAGE
                        if spin_decision == "no spin peek":
                            player_used_peek = True
                    await msg.edit(embed=gamescreen, view=None)  # EDITS THE EMBED
                    await asyncio.sleep(2)
                clear_fields()
                if recently_jammed:
                    if current_chamber == death_chamber:
                        gamescreen.add_field(name=f"{player}'s turn.", value=f"The gun **will** go off this round",
                                             inline=False)
                    else:
                        gamescreen.add_field(name=f"{player}'s turn.", value=f"The gun will **not** go off this round",
                                             inline=False)
                else:
                    gamescreen.add_field(name=f"{player}'s turn.",
                                         value=f"The gun has a {math.ceil(1 / (6 - triggerpulls) * 10000 * (5 / 6)) / 100}% chance of going off",
                                         inline=False)
                await msg.edit(embed=gamescreen, view=None)  # EDITS THE EMBED
                # Shoot who?
                if playershootcd:
                    shootview = ShootWhoWithoutOpponent(player, opponent)
                else:
                    shootview = ShootWhoWithOpponent(player, opponent)
                shootwho = None
                await msg.edit(embed=gamescreen, view=shootview)

                while shootwho == None:
                    await asyncio.sleep(0.25)
                    shootwho = shootview.shootwho
                if shootwho == "self":
                    gamescreen.add_field(name=f"{player}'s turn.",
                                         value=f"*{player} puts the revolver against their head...*", inline=False)
                    gamescreen.set_image(url=image_shootself)  # EDIT IMAGE
                    playershootcd = False
                elif shootwho == "opponent":
                    gamescreen.add_field(name=f"{player}'s turn.",
                                         value=f"*{player} points the revolver to {opponent}.*", inline=False)
                    gamescreen.set_image(url=image_shootopponent)  # EDIT IMAGE
                    playershootcd = True
                else:
                    gamescreen.add_field(name=f"{player}'s turn.", value=f"{player} fainted from stress.", inline=False)
                    gamescreen.set_image(url=image_fainted)  # EDIT IMAGE
                    winner = opponent
                await msg.edit(embed=gamescreen, view=None)  # EDITS THE EMBED
                await asyncio.sleep(2)

                if shootwho != "chicken":
                    if current_chamber != death_chamber:
                        gamescreen.add_field(name=f"{player}'s turn.", value="*The gun didn't go off*", inline=False)
                    else:
                        # Bang
                        # Hard diff bias
                        if bot_diff == "hard":
                            if random.randrange(1, 7) == 1:
                                # Shot
                                gamescreen.add_field(name=f"{player}'s turn.", value="***BANG***", inline=False)
                                if shootwho == "self":
                                    winner = opponent
                                else:
                                    winner = player
                            else:
                                # Jammed
                                gamescreen.add_field(name=f"{player}'s turn.", value="*The gun **jammed.***",
                                                     inline=False)
                                gamescreen.set_image(url=image_jammed)  # EDIT IMAGE
                                recently_jammed = True
                        else:
                            if random.randrange(1, 7) == 1:
                                # Jammed
                                gamescreen.add_field(name=f"{player}'s turn.", value="*The gun **jammed.***",
                                                     inline=False)
                                gamescreen.set_image(url=image_jammed)  # EDIT IMAGE
                                recently_jammed = True
                            else:
                                # Shot
                                gamescreen.add_field(name=f"{player}'s turn.", value="***BANG***", inline=False)
                                if shootwho == "self":
                                    winner = opponent
                                else:
                                    winner = player

                # Log the round
                if shootwho != "chicken":
                    if spin_decision == "spin" and shootwho == "self":
                        roundlog.append(f"{turns_taken_all}. {player} spun the cylinder, shot self.")
                    elif spin_decision == "spin" and shootwho == "opponent":
                        roundlog.append(f"{turns_taken_all}. {player} spun the cylinder, shot {opponent}.")
                    elif shootwho == "self":
                        roundlog.append(f"{turns_taken_all}. {player} shot self.")
                    elif shootwho == "opponent":
                        roundlog.append(f"{turns_taken_all}. {player} shot {opponent}.")
                    if current_chamber == death_chamber and winner:
                        roundlog.append(f"  The gun went off.")
                    elif current_chamber == death_chamber and not winner:
                        roundlog.append(f"  The gun jammed.")
                else:
                    roundlog.append(f"{turns_taken_all}. {player} fainted from stress.")
            else:
                # OPPONENT'S TURN
                if current_chamber <= death_chamber:
                    bot_peek = death_chamber - current_chamber + 1
                else:
                    bot_peek = death_chamber + 6 - current_chamber + 1
                if recently_jammed:
                    if current_chamber == death_chamber:
                        gamescreen.add_field(name=f"{opponent}'s turn.", value=f"The gun **will** go off this round",
                                             inline=False)
                    else:
                        gamescreen.add_field(name=f"{opponent}'s turn.",
                                             value=f"The gun will **not** go off this round", inline=False)
                else:
                    gamescreen.add_field(name=f"{opponent}'s turn.",
                                         value=f"The gun has a {math.ceil(1 / (6 - triggerpulls) * 10000 * (5 / 6)) / 100}% chance of going off",
                                         inline=False)
                spin_decision = None
                if opponent_spin_finale == False:
                    # Spin the cylinder?
                    spinview = SpinCylinder(opponent)
                    await msg.edit(embed=gamescreen, view=spinview)

                    if bot_diff != None:  # BOT GAMEPLAY
                        await asyncio.sleep(random.randrange(10, 50) / 10)  # Simulate human behaviour

                        if bot_diff == "easy":
                            ## EASY DIFFICULTY - RANDOM
                            if random.randrange(1, 3) == 1:
                                spin_decision = "spin"
                            else:
                                spin_decision = "no spin"
                        elif bot_diff == "medium":
                            ## MEDIUM DIFFICULTY - NO SPINS FOR PEEK 1 AND 3, SPINS FOR PEEK 2
                            if bot_peek > 3:
                                if random.randrange(1, 3) == 1:
                                    spin_decision = "spin"
                                else:
                                    spin_decision = "no spin"
                            elif bot_peek == 2:
                                spin_decision = "spin"
                            else:
                                spin_decision = "no spin"
                        else:
                            ## HARD DIFFICULTY - NO SPINS FOR ALL EXCEPT PEEK 2
                            if bot_peek == 2:
                                spin_decision = "spin"
                            else:
                                spin_decision = "no spin"
                    else:
                        while spin_decision == None:  ## AWAITING A SPIN DECISION
                            await asyncio.sleep(0.25)
                            spin_decision = spinview.spin_decision

                    if spin_decision == "spin":
                        gamescreen.add_field(name=f"{opponent}'s turn.", value=f"{opponent} spins the cylinder...",
                                             inline=False)
                        triggerpulls = 0
                        recently_jammed = False
                        current_chamber = random.randrange(1, 7)
                        if turns_taken_all >= 10:
                            opponent_spin_finale = True
                        gamescreen.set_image(url=image_spin)  # EDIT IMAGE
                    else:
                        gamescreen.add_field(name=f"{opponent}'s turn.", value=f"{opponent} did not spin the cylinder.",
                                             inline=False)
                        gamescreen.set_image(url=image_revolver)  # EDIT IMAGE
                        if spin_decision == "no spin peek":
                            opponent_used_peek = True
                    await msg.edit(embed=gamescreen, view=None)  # EDITS THE EMBED
                    await asyncio.sleep(2)
                clear_fields()
                if recently_jammed:
                    if current_chamber == death_chamber:
                        gamescreen.add_field(name=f"{opponent}'s turn.", value=f"The gun **will** go off this round",
                                             inline=False)
                    else:
                        gamescreen.add_field(name=f"{opponent}'s turn.",
                                             value=f"The gun will **not** go off this round", inline=False)
                else:
                    gamescreen.add_field(name=f"{opponent}'s turn.",
                                         value=f"The gun has a {math.ceil(1 / (6 - triggerpulls) * 10000 * (5 / 6)) / 100}% chance of going off",
                                         inline=False)
                await msg.edit(embed=gamescreen, view=None)  # EDITS THE EMBED
                # Shoot who?
                if opponentshootcd:
                    shootview = ShootWhoWithoutOpponent(opponent, player)
                else:
                    shootview = ShootWhoWithOpponent(opponent, player)
                shootwho = None
                await msg.edit(embed=gamescreen, view=shootview)

                if bot_diff != None:
                    await asyncio.sleep(random.randrange(10, 50) / 10)  # Simulate human behaviour
                    if bot_diff == "easy":
                        # EASY DIFF - RANDOM
                        if opponentshootcd:
                            shootwho = "self"
                        elif triggerpulls > 3:
                            shootwho = "opponent"
                        else:
                            if random.randrange(1, 3) == 1:
                                shootwho = "self"
                            else:
                                shootwho = "opponent"
                    elif bot_diff == "medium":
                        # EASY AND MEDIUM DIFF - ATTEMPTS TO SHOOT PLAYER IF PEEK 1, GUARANTEED TO SHOOT SELF IF PEEK 3
                        if bot_peek == 1 and not opponentshootcd:
                            shootwho = "opponent"
                        elif bot_peek == 3:
                            shootwho = "self"
                        else:  # ANY
                            if opponentshootcd:
                                shootwho = "self"
                            else:
                                if random.randrange(1, 3) == 1:
                                    shootwho = "self"
                                else:
                                    shootwho = "opponent"
                    elif bot_diff == "hard":
                        # HARD DIFF - GUARANTEED TO SHOOT SELF IS PEEK 3+, ATTEMPTS TO SHOOT PLAYER IF PEEK 1

                        if current_chamber <= death_chamber:
                            bot_peek = death_chamber - current_chamber + 1
                        else:
                            bot_peek = death_chamber + 6 - current_chamber + 1

                        if bot_peek == 1 and not opponentshootcd:
                            shootwho = "opponent"
                        elif bot_peek >= 3:
                            shootwho = "self"
                        else:  # ANY (or peek 2)
                            if opponentshootcd:
                                shootwho = "self"
                            else:
                                if random.randrange(1, 3) == 1:
                                    shootwho = "self"
                                else:
                                    shootwho = "opponent"


                else:
                    while shootwho == None:  ## AWAITING PLAYER INPUT
                        await asyncio.sleep(0.25)
                        shootwho = shootview.shootwho
                if shootwho == "self":
                    gamescreen.add_field(name=f"{opponent}'s turn.",
                                         value=f"*{opponent} puts the revolver against their head...*", inline=False)
                    gamescreen.set_image(url=image_shootself)  # EDIT IMAGE
                    opponentshootcd = False
                elif shootwho == "opponent":
                    gamescreen.add_field(name=f"{opponent}'s turn.",
                                         value=f"*{opponent} points the revolver to {player}.*", inline=False)
                    gamescreen.set_image(url=image_shootopponent)  # EDIT IMAGE
                    opponentshootcd = True
                else:
                    gamescreen.add_field(name=f"{opponent}'s turn.", value=f"{opponent} fainted from stress.",
                                         inline=False)
                    gamescreen.set_image(url=image_fainted)  # EDIT IMAGE
                    winner = player
                await msg.edit(embed=gamescreen, view=None)  # EDITS THE EMBED
                await asyncio.sleep(2)

                if shootwho != "chicken":
                    if current_chamber != death_chamber:
                        gamescreen.add_field(name=f"{player}'s turn.", value="*The gun didn't go off*", inline=False)
                    else:
                        # Bang
                        if random.randrange(1, 7) == 1:
                            # Jammed
                            gamescreen.add_field(name=f"{player}'s turn.", value="*The gun **jammed.***", inline=False)
                            gamescreen.set_image(url=image_jammed)  # EDIT IMAGE
                            recently_jammed = True
                        else:
                            # Shot
                            gamescreen.add_field(name=f"{player}'s turn.", value="***BANG***", inline=False)
                            if shootwho == "self":
                                winner = player
                            else:
                                winner = opponent

                # Log the round
                if shootwho != "chicken":
                    if spin_decision == "spin" and shootwho == "self":
                        roundlog.append(f"{turns_taken_all}. {opponent} spun the cylinder, shot self.")
                    elif spin_decision == "spin" and shootwho == "opponent":
                        roundlog.append(f"{turns_taken_all}. {opponent} spun the cylinder, shot {player}.")
                    elif shootwho == "self":
                        roundlog.append(f"{turns_taken_all}. {opponent} shot self.")
                    elif shootwho == "opponent":
                        roundlog.append(f"{turns_taken_all}. {opponent} shot {player}.")
                    if current_chamber == death_chamber and winner:
                        roundlog.append(f"  The gun went off.")
                    elif current_chamber == death_chamber and not winner:
                        roundlog.append(f"  The gun jammed.")
                else:
                    roundlog.append(f"{turns_taken_all}. {opponent} fainted from stress.")

            await msg.edit(embed=gamescreen, view=None)  # EDITS THE EMBED
            await asyncio.sleep(2)
            if current_chamber == death_chamber and not winner:
                await asyncio.sleep(2)

            turns_taken_all += 1
            triggerpulls += 1
            if current_chamber == death_chamber:
                triggerpulls = -1
            current_chamber += 1
            if current_chamber > 6:
                current_chamber = 1
            turn += 1
            if turn > 2:
                turn = 1
            clear_fields()
            await msg.edit(embed=gamescreen, view=None)  # EDITS THE EMBED
        # END GAME
        clear_fields()
        if player.name == opponent.name:
            gamescreen.add_field(name=f"GAME OVER", value=f"*{winner} died.*", inline=True)
        else:
            gamescreen.add_field(name=f"GAME OVER", value=f"*{winner} is the winner of the duel.*", inline=True)
        gamescreen.add_field(name=f"Turns taken:", value=f"{turns_taken_all - 1}", inline=True)

        gamescreen.set_image(url=image_dead)  # EDIT IMAGE
        print(roundlog)
        for i in range(0, len(roundlog)):
            gamescreen.add_field(name="", value=roundlog[i], inline=False)

        await msg.edit(embed=gamescreen, view=None)  # EDITS THE EMBED

        if bot_diff != None and winner == opponent:
            if bot_diff == "easy":
                await ctx.send(
                    f"**{opponent.name}**: You know, it's a wonder that I even won this. The Dealer thinks bots are too stupid for this.")
            elif bot_diff == "medium":
                await ctx.send("back to gooning")
            elif bot_diff == "hard":
                await ctx.send(
                    f"Your fatal mistake to challenge the creator of this game. I'm not just good, I can rig the game to my desire.")
                await asyncio.sleep(2)
                await ctx.send(
                    f"I always know where the bullet is at all times, and if the gun dares to go off in my face before the finale, 5 out of 6 times it will jam.")


async def setup(bot):
    await bot.add_cog(RussianRoulette(bot))
