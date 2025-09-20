from discord.ext import commands
import discord
import wavelink
from typing import cast
import time
import validators
from Classes.Music_Player_Class import Queue_Button
from Classes.Music_Player_Class import Selector
import logging
from youtubesearchpython import VideosSearch

# Original reference: https://github.com/PythonistaGuild/Wavelink/blob/main/examples/simple.py

stream_start_time = {}
queue_page_limit = 6
queue_limit = 150
title_length_max = 40
nc = {}
run_time = {}


async def timeformat(inp: int):  # (hour:)minute:second
    seconds = inp // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    if hours <= 0:
        return f"{minutes}:{remaining_seconds:02d}"
    else:
        return f"{hours}:{minutes:02d}:{remaining_seconds:02d}"


async def timeconversion(inp: str):
    if inp.count(':') == 1:
        minutes, seconds = map(int, inp.split(':'))
        if minutes >= 60 or minutes < 0 or seconds >= 60 or seconds < 0:
            raise ValueError
        total_seconds = minutes * 60 + seconds
    elif inp.count(':') == 2:
        hours, minutes, seconds = map(int, inp.split(':'))
        if hours >= 24 or hours < 0 or minutes >= 60 or minutes < 0 or seconds >= 60 or seconds < 0:
            raise ValueError
        total_seconds = hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError
    return total_seconds


async def search(ctx, url):
    index = 0
    embed = discord.Embed(title='-= Search Results =-', description='', colour=discord.Colour.lighter_grey())
    embed.set_author(name=f"Suggested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
    videosearch = VideosSearch(url, limit=5)
    options = []
    for i in videosearch.result()['result']:
        index += 1
        title = f"{i['title']}"
        if len(title) > title_length_max:
            title = title[:title_length_max] + '...'
        title = title.replace('[', '［').replace(']', '］')
        if i['duration'] is None:
            embed.description += f"**{index}.** [{title}]({i['link']}) 🔴 - {i['channel']['name']}"
        else:
            embed.description += f"**{index}.** [{title}]({i['link']}) [{i['duration']}] - {i['channel']['name']}"
        embed.description += "\n"
        options.append(f"{index}. {title} ({i['channel']['name']})")
    view = Selector(options, ctx.author)
    original_mess = await ctx.send(embed=embed, view=view)
    await view.wait()
    await original_mess.delete()
    response = videosearch.result()['result'][view.selected]['link']
    return response


class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            # Handle edge cases...
            return
        track: wavelink.Playable = payload.track
        # format time

        # Stream case (different)
        if track.is_stream:
            length = "🔴Stream"
            global stream_start_time
            stream_start_time[player.guild.id] = time.time()
        else:
            length = await timeformat(track.length)

        embed: discord.Embed = discord.Embed(title="-= Now Playing =-", colour=discord.Colour.lighter_gray())
        embed.description = f"[__{track.title}__]({track.uri})\n\n0:00 -----------------▶----------------- {length}"

        if track.artwork:
            embed.set_image(url=track.artwork)

        embed.set_author(name=f"XLCog's music service.", icon_url=self.bot.user.avatar.url)
        embed.set_footer(text=f"Video/Track by: {track.author} || {track.source.capitalize()}")

        global nc
        nc[player.guild.id] = False
        await player.set_filters(None)
        await player.home.send(embed=embed)

    @commands.Cog.listener()
    async def on_wavelink_inactive_player(self, player: wavelink.Player) -> None:
        await player.home.send("`Disconnecting...`")
        await player.disconnect()

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload):
        player = payload.player
        try:
            if len(payload.player.channel.members) == 1:
                await payload.player.disconnect()
                return
        except AttributeError:
            pass
        try:
            next_track = player.queue.get()
            logging.info((next_track.title, next_track.uri))
            await player.play(next_track)
        except wavelink.exceptions.QueueEmpty:
            embed = discord.Embed(title="-= The Queue has reached its end! =-",
                                  description="Use `!play` to add more songs to the queue.",
                                  colour=discord.Colour.lighter_grey())
            embed.set_author(name="XLCog's music service", icon_url=self.bot.user.avatar.url)
            embed.set_footer(text="I will automatically disconnect after 2 minutes of inactivity.")
            await player.home.send(embed=embed)
        except Exception as e:
            logging.info(e)

    @commands.command(help="Plays a song with the provided query. Query can either be keywords or a valid url.")
    async def play(self, ctx: commands.Context, *, query: str) -> None:
        """Play a song with the given query."""
        if not ctx.guild:
            return
        # Delete user prompt
        if ctx.author.voice is None:
            await ctx.send("brother get in the vc")
            return
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player: wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)  # type: ignore

        # If the player is not currently playing:
        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)  # type: ignore
                global run_time
                run_time[player.guild.id] = time.time()
            except AttributeError:
                await ctx.send("Please join a voice channel first before using this command.")
                return
            except discord.ClientException:
                await ctx.send("I was unable to join this voice channel. Please try again.")
                return

        # cog AutoPlayMode
        player.autoplay = wavelink.AutoPlayMode.disabled

        # Lock the player to this channel...
        if not hasattr(player, "home"):
            player.home = ctx.channel
        elif player.home != ctx.channel:
            await ctx.send(
                f"You can only play songs in {player.home.mention}, as the player has already started there.")
            return

        # Defaults to YouTube for non URL based queries...
        validation = validators.url(query)
        if not validation:
            # If the query has only words -> Default: YouTube.
            data = await search(ctx, query)
        else:
            # If given a link, fetched like normal.
            data = query
            logging.info(query)
        print("before search")
        try:
            tracks: wavelink.Search = await wavelink.Playable.search(data)
        except Exception as e:
            print(e)
        print("after search")
        if not tracks:
            await ctx.send(f"{ctx.author.mention} - Could not find any tracks with that query. Please try again.")
            return

        if isinstance(tracks, wavelink.Playlist):  # if tracks is a playlist...
            if len(player.queue) + 1 > queue_limit:
                await ctx.send(f"The queue limit is {queue_limit} tracks.")
                return

            if len(player.queue) + len(tracks) > queue_limit:
                await ctx.send(
                    f"Due to the queue limit, only {queue_limit - len(player.queue)} track(s) will be added to the "
                    f"queue.")
                added: int = await player.queue.put_wait(tracks[0:queue_limit - len(player.queue)])
            else:
                added: int = await player.queue.put_wait(tracks)

            async def added_embed_playlist():
                embed = discord.Embed(title="-= Suggestion Added =-", colour=discord.Colour.lighter_gray())
                embed.description = f"Added the playlist [__{tracks.name}__]({tracks.url}) [{tracks.author}] ({added} songs) to the queue."
                embed.set_thumbnail(url=tracks.artwork)
                embed.set_author(name=f"Added by {ctx.author.name}", icon_url=ctx.author.avatar.url)
                embed.set_footer(text=f"Source: {tracks[0].source.capitalize()}")
                return embed

            await ctx.send(embed=await added_embed_playlist())

        else:  # if a single track is added...
            if len(player.queue) + 1 > queue_limit:
                await ctx.send(f"The queue limit is {queue_limit} tracks.")
                return

            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)

            # Embed queue added
            async def added_embed_single():
                embed = discord.Embed(title="-= Suggestion Added =-", colour=discord.Colour.lighter_gray())
                embed.description = f"Added [__{track.title}__]({track.uri}) [{track.author}] to the queue."
                embed.set_thumbnail(url=track.artwork)
                embed.set_author(name=f"Added by {ctx.author.name}", icon_url=ctx.author.avatar.url)
                embed.set_footer(text=f"Source: {track.source.capitalize()}")
                return embed

            await ctx.send(embed=await added_embed_single())

        if not player.playing:
            # Play now since we aren't playing anything...
            await player.play(player.queue.get())

    @commands.command(help="Skips the current song.")
    async def skip(self, ctx: commands.Context) -> None:
        """Skip the current song."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)

        if not player:
            return

        if player.home != ctx.channel:
            await ctx.send(
                f"You can only use voice commands in {player.home.mention}, as the player has already started there.")
            return

        if ctx.author.voice is None:
            await ctx.send("brother get in the vc")
            return

        await player.skip(force=True)
        await ctx.message.add_reaction("\u2705")

    @commands.command(help="NIGHTCORE MODE.", aliases=["nc"])
    async def nightcore(self, ctx: commands.Context) -> None:
        """Set the filter to a nightcore style."""
        global nc
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)

        if not player:
            return

        if player.home != ctx.channel:
            await ctx.send(
                f"You can only use voice commands in {player.home.mention}, as the player has already started there.")
            return

        if ctx.author.voice is None:
            await ctx.send("brother get in the vc")
            return

        if player.current.is_stream:
            await ctx.send("Cannot use nightcore for streams.")
            return

        if not nc[player.guild.id]:
            filters: wavelink.Filters = player.filters
            filters.timescale.set(pitch=1.2, speed=1.2, rate=1)
            await player.set_filters(filters, seek=True)
            await ctx.message.add_reaction("\u2705")
            nc[player.guild.id] = True
        else:
            await player.set_filters(None, seek=True)
            await ctx.message.add_reaction("\u274C")
            nc[player.guild.id] = False

    @commands.command(name="toggle", aliases=["pause", "resume"], help="Pause or Resume the Player.")
    async def pause_resume(self, ctx: commands.Context) -> None:
        """Pause or Resume the Player depending on its current state."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)

        if not player:
            return

        if player.home != ctx.channel:
            await ctx.send(
                f"You can only use voice commands in {player.home.mention}, as the player has already started there.")
            return

        if ctx.author.voice is None:
            await ctx.send("brother get in the vc")
            return

        if player.current.is_stream:
            embed = discord.Embed(title="-= LIVE STREAM =-", colour=discord.Colour.lighter_gray(),
                                  description="Streams cannot be paused.")
            embed.set_author(name="XLCog's music service", icon_url=self.bot.user.avatar.url)
            await ctx.send(embed=embed)
            return
        await player.pause(not player.paused)
        await ctx.message.add_reaction("\u2705")

    @commands.command(help="0 <= VOLUME <= 200.")
    async def volume(self, ctx: commands.Context, value: int) -> None:
        """Change the volume of the player."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)

        if not player:
            return

        if player.home != ctx.channel:
            await ctx.send(
                f"You can only use voice commands in {player.home.mention}, as the player has already started there.")
            return

        if ctx.author.voice is None:
            await ctx.send("brother get in the vc")
            return

        if value > 200 or value < 0:
            await ctx.reply("0 <= VOLUME <= 200")
            await ctx.message.add_reaction("\u274C")
            return
        await player.set_volume(value)
        await ctx.message.add_reaction("\u2705")

    @commands.command(aliases=["dc"])
    async def disconnect(self, ctx: commands.Context) -> None:
        """Disconnect the Player."""
        if ctx.author.name != "avalancheshockz":
            await ctx.send("You're not allowed to use this command.")
            return
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.disconnect()
        await ctx.message.add_reaction("\u2705")

    @commands.command(help="Check the current queue.")
    async def queue(self, ctx: commands.Context) -> None:
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player or not player.playing:
            await ctx.send("Nothing is being played at the moment.")
            return

        if player.home != ctx.channel:
            await ctx.send(
                f"You can only use voice commands in {player.home.mention}, as the player has already started there.")
            return

        item_number = len(player.queue)
        current_page = 1
        pages = (item_number // queue_page_limit) + (1 if item_number % queue_page_limit else 0)
        if len(player.queue) == 0:
            pages = 1

        total_length = 0
        for i in player.queue:
            if i.is_stream:
                total_length = "♾️"
                break
            total_length += i.length
        queue_embed = discord.Embed(title="-= XLCog's Music Service =-", colour=discord.Colour.lighter_gray())
        queue_embed.set_thumbnail(url=player.current.artwork)
        queue_embed.set_author(
            name=f"Queue length: {await timeformat(total_length) if total_length != "♾️" else total_length}",
            icon_url=self.bot.user.avatar.url)
        queue_embed.set_footer(
            text=f"{len(player.queue) + 1} track(s) | Page {current_page}/{pages}")

        # Get current track info
        current_track = f"[{player.current.title}]({player.current.uri}) [{await timeformat(player.current.length)}] - {player.current.author}"
        if player.current.is_stream:
            current_track = f"[{player.current.title}]({player.current.uri}) 🔴 - {player.current.author}"

        # Check if the queue has tracks
        if player.queue:
            queue_list = []
            for i in range(min(queue_page_limit, len(player.queue))):
                original_title = player.queue[i].title
                title = original_title  # Default to original title

                if len(original_title) > title_length_max:
                    # Truncate and add ellipsis
                    title = original_title[:title_length_max] + "..."  # Simple truncation
                if player.queue[i].is_stream:
                    queue_list.append(f"**{i + 1}.** [{title}]({player.queue[i].uri}) 🔴 - {player.queue[i].author}")
                else:
                    queue_list.append(
                        f"**{i + 1}.** [{title}]({player.queue[i].uri}) [{await timeformat(player.queue[i].length)}] - {player.queue[i].author}")

            queue_string = "\n".join(queue_list)
        else:
            queue_string = "No tracks in the queue."

        # Add fields to the embed
        queue_embed.add_field(name="Currently playing:", value=current_track, inline=False)
        queue_embed.add_field(name="Current queue:", value=queue_string, inline=False)

        if len(player.queue) <= queue_page_limit:
            await ctx.send(embed=queue_embed)
        else:
            # Fetching info:
            message = await ctx.send(embed=queue_embed)
            view = Queue_Button(queue_page_limit, item_number, current_page, queue_embed, player, title_length_max,
                                message)
            await message.edit(embed=queue_embed, view=view)

    @commands.command(help="Clear the current queue.")
    async def clear(self, ctx: commands.Context) -> None:
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)

        if ctx.author.voice is None:
            await ctx.send("brother get in the vc")
            return

        if player.home != ctx.channel:
            await ctx.send(
                f"You can only use voice commands in {player.home.mention}, as the player has already started there.")
            return

        player.queue.clear()
        await ctx.message.add_reaction("\u2705")

    @commands.command(help="The currently playing song.")
    async def np(self, ctx: commands.Context) -> None:
        player: wavelink.player = cast(wavelink.Player, ctx.voice_client)

        if not player or not player.playing:
            await ctx.send("Nothing is being played at the moment.")
            return

        if player.home != ctx.channel:
            await ctx.send(
                f"You can only use voice commands in {player.home.mention}, as the player has already started there.")
            return

        track: wavelink.Playable = player.current

        logging.info((player.current.title, player.current.uri))

        player_position = await timeformat(player.position)

        # Separate time handling for streams
        if track.is_stream:
            track_length = "🔴Stream"
            global stream_start_time
            elapsed_time = time.time() - stream_start_time[player.guild.id]
            player_position = await timeformat(int(elapsed_time * 1000))

        # Handling time like normal (using player.track.position)
        else:
            track_length = await timeformat(track.length)

        embed: discord.Embed = discord.Embed(title="-= Now Playing =-", colour=discord.Colour.lighter_gray())
        embed.description = f"[__{track.title}__]({track.uri})\n\n{player_position} -----------------▶----------------- {track_length}"

        if track.artwork:
            embed.set_image(url=track.artwork)

        embed.set_author(name=f"XLCog's music service.", icon_url=self.bot.user.avatar.url)
        embed.set_footer(text=f"Video/Track by: {track.author} || {track.source.capitalize()}")

        await ctx.send(embed=embed)

    @commands.command(help="Seek to the provided position. Format: `[minutes]:[seconds]` or `[hours]:[minutes]:[seconds]`")
    async def seek(self, ctx: commands.Context, position: str) -> None:
        player: wavelink.player = cast(wavelink.Player, ctx.voice_client)

        if not player or not player.playing:
            await ctx.send("Nothing is being played at the moment.")
            return

        if player.home != ctx.channel:
            await ctx.send(
                f"You can only use voice commands in {player.home.mention}, as the player has already started there.")
            return

        if player.current.is_stream:
            await ctx.send("This feature is not supported for streams at the moment.")
            await ctx.message.add_reaction("\u274C")
            return

        try:
            inp_time = await timeconversion(position)
        except ValueError:
            await ctx.send("Please enter the correct format: `[minutes]:[seconds]` or `[hours]:[minutes]:[seconds]`")
            await ctx.message.add_reaction("\u274C")
            return
        except Exception as e:
            logging.info(e)
            await ctx.message.add_reaction("\u274C")
            return

        if inp_time*1000 > player.current.length:
            await ctx.send("The seek time should be within the current track's length.")
            await ctx.message.add_reaction("\u274C")
            return
        await player.seek(inp_time*1000)
        await ctx.message.add_reaction("\u2705")


    @commands.command(help="Shuffles the current queue.")
    async def shuffle(self, ctx: commands.Context) -> None:
        player: wavelink.player = cast(wavelink.Player, ctx.voice_client)
        if player.home != ctx.channel:
            await ctx.send(
                f"You can only use voice commands in {player.home.mention}, as the player has already started there.")
            return

        if not player or not player.playing:
            await ctx.send("Nothing is being played at the moment.")
            return

        player.queue.shuffle()
        await ctx.message.add_reaction("\u2705")
        await self.queue(ctx)

    @commands.command(help="How long the voice function has been running")
    async def runtime(self, ctx: commands.Context) -> None:
        player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            await ctx.send("The music playing function is currently inactive.")
            return
        global run_time
        elapsed = (time.time() - run_time[player.guild.id]) * 1000
        await ctx.send(f"Runtime: {await timeformat(int(elapsed))}")

    @commands.command(help="Searches for a youtube video")
    async def search(self, ctx: commands.Context, *, query: str) -> None:
        if validators.url(query):
            await ctx.send("This command accepts keywords only, as it's searching for YouTube videos.")
            return
        await ctx.message.delete()
        await ctx.send(await search(ctx, query))
        print("insert fix here")


async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))
