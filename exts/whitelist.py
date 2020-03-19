import re

from discord.ext import commands
from mods import firestore, info


@commands.command()
async def whitelist(ctx, command=None, user=None, remove=False):
    if not user:
        await ctx.send('You must provide both a command and a user!')
    if re.match(r"<@!?[0-9]+>", user):
        user = ctx.message.mentions[0]
        uid = str(user.id)
    elif re.match(r"[0-9]+", user):
        uid = user
    else:
        return 'Invalid mention.'
    uid_ = str(ctx.author.id)
    whitelist_ = (await firestore.get_command(uid_, command))['whitelist']
    if remove:
        whitelist_.remove(uid)
        await firestore.update_command(uid_, command, 'whitelist', whitelist_)
        return 'User removed from whitelist'
    whitelist_.append(uid)
    await firestore.update_command(uid_, command, 'whitelist', whitelist_)
    ctx.send('User added to whitelist.')


def setup(bot):
    info.Help(
        name='whitelist',
        description='allow another user to use a command',
        usage='`whitelist <command> <user>`'
    )
    bot.add_command(whitelist)
