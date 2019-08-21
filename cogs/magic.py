import discord
from mtgsdk import Card
from discord.ext import commands, tasks

class magic(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Magic is ready.')

    #commands
    @commands.command()
    async def fetch(self, ctx, * ,cardname):
        await ctx.send('Working on it.')
        cards = Card.where(name=cardname).all()
        all_cards = []
        for x in range(len(cards)):
            if cards[x].name not in all_cards:
                all_cards.append(cards[x].name)

        if(len(all_cards) == 0):
            await ctx.send('No such cards')
            return

        if(len(all_cards) == 1):
            cardname = cards[0]
            await ctx.send(cardname.image_url)
            await ctx.send("General Info of "+ cardname.name)
            await ctx.send('ManaCost: '+cardname.mana_cost+', CMC: ' +str(cardname.cmc))
            await ctx.send(cardname.text)
            return

        await ctx.send('Fetched all card names.')

        for x in range(len(all_cards)):
            await ctx.send(f'*{all_cards[x]}*')

        await ctx.send('Which card name do you want to see?')
        channel = ctx.channel
        #def check(m):
        #    return m.content in all_cards and m.channel == channel
        msg = await self.client.wait_for('message')
        if(msg.content in all_cards):
            cardname = Card.where(name=msg.content).all()
            await ctx.send(cardname[0].image_url)
            await ctx.send("General Info of "+ cardname[0].name)
            await ctx.send('ManaCost: '+cardname[0].mana_cost+', CMC: ' +str(cardname[0].cmc))
            await ctx.send(cardname[0].text)
            return
        else:
            await ctx.send('Bad Data')
            return

def setup(client):
    client.add_cog(magic(client))
