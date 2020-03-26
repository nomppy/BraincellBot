import random
from discord.ext import commands
from mods import info, vars_


@commands.command()
async def alive(ctx):
    if ctx.author.bot:
        return
    resp = ['Living the dream!', 'Alive and kicking!', 'Yes, but dead inside :(',
            'We\'re all gonna die anyway',
            'What\'s the point?']
    await ctx.send(resp[random.randint(0, len(resp) - 1)])


def setup(bot):
    info.Info(
        name='alive',
        brief="this is for you to see if I'm alive",
        usage='`alive`',
        category='Info',
    ).export(vars_.info_)

    bot.add_command(alive)
