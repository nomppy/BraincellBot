import re

import discord
from discord.ext import commands
from mods import firestore, info, vars_


@commands.command()
async def whitelist(ctx, command=None, user=None, remove=False):
    async def send():
        await ctx.send(embed=embed)

    embed = discord.Embed(title='Whitelist')
    if not command:
        embed.description = 'You must provide at least a command'
        embed.colour = vars_.colour_error
        await send()
        return
    if not user:
        embed.description = 'TODO send whitelist for command here'
        embed.colour = vars_.colour_warning
        await send()
        return
    match = re.search(r"[0-9]+", user)
    if match:
        uid = match.group(0)
    else:
        embed.description = 'Invalid user.'
        embed.colour = vars_.colour_error
        await send()
        return
    uid_ = str(ctx.author.id)
    command_ = await firestore.get_command(uid_, command)
    if not command_:
        embed.description = 'Command does not exist'
        embed.colour = vars_.colour_error
        await send()
        return

    whitelist_ = command_['whitelist']

    if not whitelist_:
        embed.description = 'Command does not have whitelist'
        embed.colour = vars_.colour_warning
        await send()
        return
    if remove:
        if uid not in whitelist_:
            embed.description = 'User not in whitelist'
            embed.colour = vars_.colour_error
            await send()
        whitelist_.remove(uid)
        await firestore.update_command_field(uid_, command, 'whitelist', whitelist_)
        return 'User removed from whitelist'
    if uid in whitelist_:
        embed.description = 'User already in whitelist'
        embed.colour = vars_.colour_warning
        await send()
        return
    whitelist_.append(uid)
    await firestore.update_command_field(uid_, command, 'whitelist', whitelist_)
    embed.description = 'User added to whitelist'
    embed.colour = vars_.colour_success
    await send()


def setup(bot):
    info.Info(
        name='whitelist',
        brief='allow another user to use a command',
        usage='`whitelist <command> <user>`',
        category='Access Control',
    ).export(vars_.info_)
    bot.add_command(whitelist)
