import discord
from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
import youtube_dl
import os
import time
from mutagen.mp3 import MP3
players = {}

class VC(commands.Cog):
    def __init__(self, client):
        self.client = client

    players = {}
    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print('VC is ready.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if 'VC' in message.content:
            channel = message.channel
            await channel.send('Ofcourse you want to VC')

    #commands
    @commands.command(pass_context=True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await voice.disconnect()
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f"The bot has connected to {channel}\n")

        await ctx.send(f"Joined {channel}")

    @commands.command(pass_context=True)
    async def kick(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"The bot has left {channel}")
            await ctx.send(f"Left {channel}")
        else:
            print("Bot was told to leave voice channel, but was not in one")
            await ctx.send("Don't think I am in a voice channel")

    @commands.command()
    async def test(self, ctx, channel: discord.VoiceChannel):
        vc_members = channel.members
        for x in range(len(vc_members)):
            await ctx.send(vc_members[x])
        return


    @commands.command(pass_context = True)
    async def annoy(self, ctx):
        url = "https://www.youtube.com/watch?v=Y9QHak8h1AQ"
        #make sure we dont download it if we already have it
        song_there = os.path.isfile("annoy.mp3")
        voice = get(self.client.voice_clients, guild=ctx.guild)

        #download the file.
        if(not song_there):

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now\n")
                ydl.download([url])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    name = file
                    print(f"Renamed File: {file}\n")
                    os.rename(file, "annoy.mp3")

        voice_channel = ctx.message.guild.voice_channels

        for x in range(len(voice_channel)):
            #join a lonely VC user
            if(len(voice_channel[x].members) == 1
            and not voice_channel[x].members[0].bot):
                await ctx.send("lonely user found")
                voice = get(self.client.voice_clients, guild=ctx.guild)
                if voice and voice.is_connected():
                    await voice.move_to(voice_channel[x])
                else:
                    voice = await voice_channel[x].connect()

            if(len(voice_channel[x].members) == 2
            and (not voice_channel[x].members[0].bot or not voice_channel[x].members[1].bot)):
                await ctx.send("lonely user found w bot")
                voice = get(self.client.voice_clients, guild=ctx.guild)
                if voice and voice.is_connected():
                    await voice.move_to(voice_channel[x])
                else:
                    voice = await voice_channel[x].connect()

        voice.play(discord.FFmpegPCMAudio("annoy.mp3"), after=lambda e: print("Song done!"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        audio = MP3("annoy.mp3")
        t_end = time.time() + audio.info.length
        while time.time() < t_end:
            #await ctx.send("Testig")
            for x in range(len(voice_channel)):
                await ctx.send("Testimg")
                if(len(voice_channel[x].members) == 1
                and not voice_channel[x].members[0].bot):
                    await ctx.send("You cant escape")
                    voice = get(self.client.voice_clients, guild=ctx.guild)
                    await voice.move_to(voice_channel[x])
                    if voice and voice.is_connected():
                        await voice.move_to(voice_channel[x])
                    else:
                        voice = await voice_channel[x].connect()


def setup(client):
    client.add_cog(VC(client))
