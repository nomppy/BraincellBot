import random

import discord
from discord.ext import commands
from mods import info, vars_


@commands.command()
async def alive(ctx):
    if ctx.author.bot:
        return
    resp = ['Living the dream!',
            'Alive and kicking!',
            'Yes, but dead inside :(',
            'We\'re all gonna die anyway',
            'What\'s the point?']
    embed = discord.Embed(
        title='Alive',
        description=resp[random.randint(0, len(resp) - 1)],
        colour=vars_.colour_success
    )
    await ctx.send(embed=embed)


def setup(bot):
    info.Info(
        name='alive',
        brief="this is for you to see if I'm alive",
        usage='`alive`',
        category='Info',
    ).export(vars_.info_)

    bot.add_command(alive)
