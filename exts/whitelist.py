import re

from discord.ext import commands
from mods import firestore, info, vars_


@commands.command()
async def whitelist(ctx, command=None, user=None, remove=False):
    if not user:
        await ctx.send('You must provide both a command and a user!')
        return
    match = re.search(r"[0-9]+", user)
    if match:
        uid = match.group(0)
    else:
        await ctx.send('Invalid mention.')
        return
    uid_ = str(ctx.author.id)
    command_ = await firestore.get_command(uid_, command)
    if not command_:
        await ctx.send('This command does not exist')
        return

    whitelist_ = command_['whitelist']

    if not whitelist_:
        await ctx.send('This command does not have a whitelist')
        return
    if remove:
        if uid not in whitelist_:
            await ctx.send("User not in whitelist")
            return
        whitelist_.remove(uid)
        await firestore.update_command_field(uid_, command, 'whitelist', whitelist_)
        return 'User removed from whitelist'
    if uid in whitelist_:
        await ctx.send("User already in whitelist")
        return
    whitelist_.append(uid)
    await firestore.update_command_field(uid_, command, 'whitelist', whitelist_)
    await ctx.send('User added to whitelist.')


def setup(bot):
    info.Info(
        name='whitelist',
        brief='allow another user to use a command',
        usage='`whitelist <command> <user>`',
        category='Access Control',
    ).export(vars_.info_)
    bot.add_command(whitelist)
