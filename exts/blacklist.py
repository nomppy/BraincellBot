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
    info.Help(
        name='blacklist',
        description='removes a user from the whitelist of a command',
        usage='`blacklist <command> <user>`'
    )
    bot.add_command(blacklist)
