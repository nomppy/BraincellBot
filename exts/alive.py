import random
from discord.ext import commands


@commands.command()
async def alive(ctx):
    await ctx.send('hi')
    resp = ['Living the dream!', 'Alive and kicking!', 'Yes, but dead inside :(',
            'We\'re all gonna die anyway',
            'What\'s the point?']
    await ctx.send(resp[random.randint(0, len(resp) - 1)])


def setup(bot):
    bot.add_command(alive)
