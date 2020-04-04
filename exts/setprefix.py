import discord
from discord.ext import commands

from mods import firestore, info, vars_


@commands.command(aliases=['prefix'])
async def setprefix(ctx, prefix=''):
    embed = discord.Embed(title='Prefix')
    if ctx.author.bot:
        return

    if prefix == '':
        embed.colour = vars_.colour_error
        embed.description = 'Please don\'t make the prefix nothing'
    else:
        await firestore.update_user_field(str(ctx.author.id), 'prefix', prefix)
        embed.colour = vars_.colour_success
        embed.description = f'Your prefix has been changed to `{prefix}`'
    await ctx.send(embed=embed)


def setup(bot):
    info.Info(
        name='setprefix',
        brief='change your prefix',
        usage='`setprefix <new_prefix>`',
        category='Access Control',
        aliases=['prefix'],
    ).export(vars_.info_)

    bot.add_command(setprefix)
