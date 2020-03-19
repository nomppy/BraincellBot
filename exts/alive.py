import random
from discord.ext import commands
from mods import info


@commands.command()
async def alive(ctx):
    if ctx.author.bot:
        return
    resp = ['Living the dream!', 'Alive and kicking!', 'Yes, but dead inside :(',
            'We\'re all gonna die anyway',
            'What\'s the point?']
    await ctx.send(resp[random.randint(0, len(resp) - 1)])


def setup(bot):
    info.Help(
        name='alive',
        description='see if the bot is alive',
        usage='`alive`'
    ).export()
    bot.add_command(alive)
