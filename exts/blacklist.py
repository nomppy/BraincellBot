import discord
from discord.ext import commands

from exts import whitelist
from mods import info, vars_


@commands.command()
async def blacklist(ctx, command=None, user=None):
    embed = discord.Embed(title='Blacklist')
    if not user:
        embed.colour = vars_.colour_error
        embed.description = 'You must provide a command.'
        await ctx.send(embed=embed)
        return
    r = await whitelist.whitelist(ctx, command, user, True)
    embed.colour = vars_.colour_success
    embed.description = r
    await ctx.send(embed=embed)


def setup(bot):
    info.Info(
        name='blacklist',
        brief='removes a user from the whitelist',
        usage='`blacklist <user>`',
        category='Access Control'
    ).export(vars_.info_)

    bot.add_command(blacklist)
