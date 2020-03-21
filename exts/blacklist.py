from discord.ext import commands

from exts import whitelist
from mods import info, vars_


@commands.command()
async def blacklist(ctx, command=None, user=None):
    if not user:
        await ctx.send('You must provide both a command and a user!')
        return
    r = await whitelist.whitelist(ctx, command, user, True)
    if r:
        await ctx.send(r)


def setup(bot):
    info.Info(
        name='blacklist',
        brief='removes a user from the whitelist',
        usage='`blacklist <user>`'
    ).export(vars_.info_)

    bot.add_command(blacklist)
