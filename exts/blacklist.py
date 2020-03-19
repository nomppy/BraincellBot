from discord.ext import commands

from exts import whitelist
from mods import info


@commands.command()
async def blacklist(ctx, command=None, user=None):
    if not user:
        await ctx.send('You must provide both a command and a user!')
    r = await whitelist.whitelist(ctx, command, user, True)
    await ctx.send(r)


def setup(bot):

    bot.add_command(blacklist)
