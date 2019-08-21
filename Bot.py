import discord
import random
import os
from discord.ext import commands, tasks

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
	print('Bot is ready.')
	await client.change_presence(status=discord.Status.online, activity=discord.Game('with your heart.'))

@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')
	await ctx.send(f'{extension} loaded')

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	await ctx.send(f'{extension} unloaded')

@client.command()
async def reload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	client.load_extension(f'cogs.{extension}')
	await ctx.send(f'{extension} reloaded')

client.run('NjEzMzg1OTQ3ODg2OTExNTEy.XVwNFg.2KOcgET6lfsZ2lRliBWoAdDJLBc')
