import discord
from Classes.Shoot_Class import Shoot
import random
from discord.ext import commands
import asyncio
from Bot_Data.Data_Variables import shotgun_limit
from Classes.Wild_West.Invitation import WWInvite
from Classes.Wild_West.Draw import Draw
from Bot_Data.Data_Variables import bounty
from Bot_Data.Data_Variables import bounty_play
from Bot_Data import Data_Variables


class Shooting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bullet will hit player
    async def shootr(self, ctx, user: discord.User = None, *args):
        number_index = '#0'
        try:
            receiver = args[0]
            instigator = user
            number_index = f"# {args[1]}"
            timeout = args[2]
        except IndexError:
            timeout = 8
            instigator = ctx.author
            if user is None:
                receiver = ctx.author
            else:
                receiver = user
        if receiver == self.bot.user:
            await ctx.send(f"{self.bot.user.mention} gracefully dodged the bullet and twisted your balls.")
            return
        try:
            if ctx.message:
                await ctx.message.delete()
        except discord.NotFound:
            pass
        view = Shoot(receiver, True, timeout=timeout)
        shoot_embed = discord.Embed(title=f"Shots fired! {number_index}",
                                    description=f"{instigator.mention} just whipped out a gun on {receiver.mention}!",
                                    colour=discord.Colour.red())
        shoot_embed.set_author(name=f"Shot by {instigator}", icon_url=instigator.avatar.url)
        shooting = await ctx.send(embed=shoot_embed, view=view)
        await view.wait()
        shoot_embed = discord.Embed(title="Shoot!")
        shoot_embed.set_author(name=f"Shot by {instigator}", icon_url=instigator.avatar.url)
        if view.dodge == 'bad':
            luck = random.randint(1, 6)
            if luck == 1:
                shoot_embed.description = f"{receiver.mention} got shot, yet is still alive miraculously."
                shoot_embed.colour = discord.Colour.yellow()
            else:
                shoot_embed.description = f"{receiver.mention} has been shot."
                shoot_embed.colour = discord.Colour.red()
                if len(args) > 0:
                    Data_Variables.die += 1
        elif view.dodge == 'good':
            shoot_embed.description = f"{receiver.mention} narrowly dodged the bullet!"
            shoot_embed.colour = discord.Colour.green()
        await shooting.edit(embed=shoot_embed, view=None)
        if len(args) > 0:
            await asyncio.sleep(4)
            await shooting.delete()

    # Bullet won't hit player
    async def shootf(self, ctx, user: discord.User = None, *args):
        number_index = '#0'
        try:
            receiver = args[0]
            instigator = user
            number_index = f"# {args[1]}"
            timeout = args[2]
        except IndexError:
            timeout = 8
            instigator = ctx.author
            if user is None:
                receiver = ctx.author
            else:
                receiver = user
        if receiver == self.bot.user:
            await ctx.send(f"{self.bot.user.mention} gracefully dodged the bullet and twisted your balls.")
            return
        try:
            if ctx.message:
                await ctx.message.delete()
        except discord.NotFound:
            pass
        view = Shoot(receiver, False, timeout=timeout)
        shoot_embed = discord.Embed(title=f"Shots fired! {number_index}",
                                    description=f"{instigator.mention} just whipped out a gun on {receiver.mention}!",
                                    colour=discord.Colour.blurple())
        shoot_embed.set_author(name=f"Shot by {instigator}", icon_url=instigator.avatar.url)
        shooting = await ctx.send(embed=shoot_embed, view=view)
        await view.wait()
        shoot_embed = discord.Embed(title="Shoot!")
        shoot_embed.set_author(name=f"Shot by {instigator}", icon_url=instigator.avatar.url)
        if view.dodge == 'good':
            shoot_embed.description = f"The bullet barely missed and {receiver.mention} is somehow still alive."
            shoot_embed.colour = discord.Colour.green()
        elif view.dodge == 'bad':
            luck = random.randint(1, 6)
            if luck == 1:
                shoot_embed.description = f"{receiver.mention} dodged into the bullet, yet is still alive miraculously."
                shoot_embed.colour = discord.Colour.yellow()
            else:
                shoot_embed.description = f"{receiver.mention} dodged right into the cogging bullet and died."
                shoot_embed.colour = discord.Colour.red()
                if len(args) > 0:
                    Data_Variables.die += 1
        await shooting.edit(embed=shoot_embed, view=None)
        if len(args) > 0:
            await asyncio.sleep(4)
            await shooting.delete()

    @commands.command(name="shoot", help="Shoots an user!")  # The above functions will be randomized
    async def shoot(self, ctx, user: discord.User = None, *args):
        try:
            print("reached shoot")
            print(args)
            receiver = args[0]
            instigator = user
            number_index = args[1]
            timeout = args[2]
            Data_Variables.die = 0
            chances = random.choice([True, False])
            print("passed shoot once")
            if chances:
                await self.shootr(ctx, instigator, receiver, number_index, timeout)
                print("passed shoot (real)")
            else:
                await self.shootf(ctx, instigator, receiver, number_index, timeout)
                print("passed shoot (fake)")
        except IndexError:
            if bounty_play.get(ctx.channel.id, False):
                mes = await ctx.reply("Shut up cogger")
                await asyncio.sleep(2)
                await mes.delete()
                await ctx.message.delete()
                return
            chances = random.choice([True, True, False])
            if chances:
                await self.shootr(ctx, user)
            else:
                await self.shootf(ctx, user)

    # Custom function: Shooting multiple bullets at a time.

    async def shoot_multi(self, ctx, user: discord.User = None, *args):
        shots = args[0]
        try:
            receiver = args[1]
            instigator = user

            async def delay(i, instigator, receiver):
                await asyncio.sleep((2 * i) / 3)
                await self.shoot(ctx, instigator, receiver, i + 1, 2.5)

            tasks = [delay(i, instigator, receiver) for i in range(shots)]
            await asyncio.gather(*tasks)
        except IndexError:
            receiver = user
            instigator = ctx.author

            async def delay(i, instigator, receiver):
                await asyncio.sleep((2 * i) / 3)
                await self.shoot(instigator, receiver)

            tasks = [delay(i, instigator, receiver) for i in range(shots)]
            await asyncio.gather(*tasks)
            await asyncio.sleep(20)

    @commands.command(name="shotgun", help = "Shoots an user multiple times!")
    async def shotgun(self, ctx, user: discord.User = None):
        if bounty_play.get(ctx.channel.id, False):
            mes = await ctx.reply("Shut up cogger")
            await asyncio.sleep(2)
            await mes.delete()
            await ctx.message.delete()
            return
        if user == self.bot.user:
            await ctx.send(f"{self.bot.user.mention} gracefully dodged the bullets and twisted your balls.")
            return
        if shotgun_limit.get(ctx.channel.id, False):
            mes = await ctx.reply(f"Cooldown")
            await ctx.message.delete()
            await mes.delete()
            return
        shotgun_limit[ctx.channel.id] = True
        await self.shoot_multi(ctx, user, 6)
        await asyncio.sleep(50)
        shotgun_limit[ctx.channel.id] = False

    @commands.command(name="duel", help = "Starts a duel, wild west style.")
    async def duel(self, ctx):
        if bounty_play.get(ctx.channel.id, False):
            mes = await ctx.reply("A game is already in progress.")
            await asyncio.sleep(2)
            await mes.delete()
            await ctx.message.delete()
            return
        bounty_play[ctx.channel.id] = True
        if not bounty.get(ctx.author.id, False):
            bounty[ctx.author.id] = 10000
        round = 1
        await ctx.message.delete()
        challenge_embed = discord.Embed(title="A duel invitation has been sent out!",
                                        colour=discord.Colour.lighter_gray())
        challenge_embed.set_author(name="--= WANTED =--")
        challenge_embed.add_field(name=f"{ctx.author}'s bounty: ", value=f"{bounty[ctx.author.id]}$",
                                  inline=False)
        challenge_embed.set_thumbnail(url=ctx.author.avatar.url)
        challenge_embed.set_footer(text="You will risk your current bounty if you enter.")
        chall_view = WWInvite(challenge_embed, bounty, ctx)
        invitation = await ctx.send(embed=challenge_embed, view=chall_view)
        await chall_view.wait()
        await invitation.delete()
        if not chall_view.accept:
            challenge_embed.set_author(name="--= NO MATCHES FOUND =--")
            challenge_embed.title = "The game cannot begin."
            await ctx.send(embed=challenge_embed, view=None)
            bounty_play[ctx.channel.id] = False
            return
        challenge_embed.set_author(name="--= MATCH FOUND =--")
        challenge_embed.set_thumbnail(url=chall_view.person.avatar.url)
        challenge_embed.title = "It's high noon."
        challenge_embed.set_footer(text="You're risking your bounties.")
        preparation = await ctx.send(embed=challenge_embed, view=None)
        await asyncio.sleep(5)
        await preparation.delete()
        # ------------------------------------- game start
        player_list = [ctx.author.id, chall_view.person.id]
        hp1 = 3
        hp2 = 3
        draw_embed = discord.Embed(colour=discord.Colour.lighter_grey())
        draw_embed.add_field(name=f"{ctx.author}'s HP:", value="❤️" * hp1 + "🖤" * (3 - hp1), inline=False)
        draw_embed.add_field(name=f"{chall_view.person.name}'s HP:", value="❤️" * hp2 + "🖤" * (3 - hp2), inline=False)
        draw_mes = await ctx.send(embed=draw_embed, view=None)

        while True:
            draw_embed.title = f"-== ROUND {round} ==-"
            draw_view = Draw(draw_embed, draw_mes, player_list)
            await draw_mes.edit(embed=draw_embed, view=draw_view)
            await draw_view.start_countdown(draw_mes)
            await draw_view.wait()
            await draw_mes.edit(embed=draw_embed, view=None)
            draw_view.shootable = False
            draw_view.interacted = False
            notif_embed = discord.Embed(title="--= Damn! =--", colour=discord.Colour.lighter_grey())
            if draw_view.person is None:
                await ctx.send("Game abandoned (placeholder)")
                bounty_play[ctx.channel.id] = False
                return
            elif draw_view.chosen[draw_view.person] is True:
                notif_embed.description = f"{draw_view.person.name} was the first to draw!"
                mes = await ctx.send(embed=notif_embed)
                await asyncio.sleep(2)
                await mes.delete()
                if draw_view.person == ctx.author:
                    await self.shoot_multi(ctx, ctx.author, round + 2, chall_view.person)
                    hp2 -= Data_Variables.die
                    if hp2 < 0:
                        hp2 = 0
                else:
                    await self.shoot_multi(ctx, chall_view.person, round + 2, ctx.author)
                    hp1 -= Data_Variables.die
                    if hp1 < 0:
                        hp1 = 0
            elif draw_view.chosen[draw_view.person] is False:
                notif_embed.description = f"{draw_view.person.name} broke the cogging rules!"
                mes = await ctx.send(embed=notif_embed)
                await asyncio.sleep(2)
                await mes.delete()
                if draw_view.person == ctx.author:
                    await self.shoot_multi(ctx, chall_view.person, round + 2, ctx.author)
                    hp1 -= Data_Variables.die
                    if hp1 < 0:
                        hp1 = 0
                else:
                    await self.shoot_multi(ctx, ctx.author, round + 2, chall_view.person)
                    hp2 -= Data_Variables.die
                    if hp2 < 0:
                        hp2 = 0
            draw_embed.set_field_at(0, name=f"{ctx.author}'s HP:", value="❤️" * hp1 + "🖤" * (3 - hp1), inline=False)
            draw_embed.set_field_at(1, name=f"{chall_view.person.name}'s HP:", value="❤️" * hp2 + "🖤" * (3 - hp2),
                                    inline=False)
            await draw_mes.edit(embed=draw_embed)
            if hp1 <= 0 or hp2 <= 0:
                print(bounty)
                win_embed = discord.Embed(title="--= Fastest gun in the West =--",
                                          colour=discord.Colour.lighter_grey())
                if hp1 <= 0:
                    win = chall_view.person
                    incr = bounty[ctx.author.id] // 5
                    decr = bounty[ctx.author.id] // 10
                    bounty[chall_view.person.id] += incr
                    bounty[ctx.author.id] -= decr
                    win_embed.add_field(name=f"{chall_view.person.name}'s bounty: ",
                                        value=f"{bounty[chall_view.person.id]}$ (+{incr}$)", inline=False)
                    win_embed.add_field(name=f"{ctx.author}'s bounty: ",
                                        value=f"{bounty[ctx.author.id]}$ (-{decr}$)", inline=False)
                elif hp2 <= 0:
                    win = ctx.author
                    incr = bounty[chall_view.person.id] // 5
                    decr = bounty[chall_view.person.id] // 10
                    bounty[ctx.author.id] += incr
                    bounty[chall_view.person.id] -= decr
                    win_embed.add_field(name=f"{ctx.author}'s bounty: ",
                                        value=f"{bounty[ctx.author.id]}$ (+{incr}$)", inline=False)
                    win_embed.add_field(name=f"{chall_view.person.name}'s bounty: ",
                                        value=f"{bounty[chall_view.person.id]}$ (-{decr}$)", inline=False)
                win_embed.description = f"{win.mention} won the exchange."
                win_embed.set_thumbnail(url=win.avatar.url)
                await ctx.send(embed=win_embed)
                bounty_play[ctx.channel.id] = False
                return
            round += 1

    @commands.command(name="bounty", help = "Checks your current bounty.")
    async def bounty(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        if not bounty.get(user.id, False):
            bounty[user.id] = 10000
        bounty_value = bounty[user.id]
        embed = discord.Embed(colour=discord.Colour.lighter_grey(), title=f"-== {user.name}'s bounty ==-")
        embed.set_author(name=user.name, icon_url=user.avatar.url)
        embed.description = f"{user.mention}'s current bounty: {bounty_value}$"
        embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Shooting(bot))
