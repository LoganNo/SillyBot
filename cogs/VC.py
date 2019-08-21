import discord
from discord.ext import commands, tasks
from itertools import cycle

class VC(commands.Cog):
    def __init__(self, client):
        self.client = client

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
        author = ctx.message.author
        channel = author.voice.channel
        await channel.connect()

    @commands.command(pass_context=True)
    async def kick(self, ctx):
        server = ctx.message.guild.voice_client
        await server.disconnect()

    @commands.command()
    async def test(self, ctx, channel: discord.VoiceChannel):
        vc_members = channel.members
        for x in range(len(vc_members)):
            await ctx.send(vc_members[x])
        return

    @commands.command(pass_context = True)
    async def vcmembers(self, ctx):
        voice_channel = ctx.message.guild.voice_channels
        for x in range(len(voice_channel)):
            for y in range(len(voice_channel[x].members)):
                await ctx.send(voice_channel[x].members[y].id)

        return

def setup(client):
    client.add_cog(VC(client))
