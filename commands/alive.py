import random
from discord.ext import commands


@commands.command()
async def alive(ctx):
    # resp = ['Living the dream!', 'Alive and kicking!', 'Yes, but dead inside :(', 'We\'re all gonna die anyway',
    #         'What\'s the point?']
    resp = 'test'
    await ctx.send(resp[random.randint(0, len(resp) - 1)])
