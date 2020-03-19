from discord.ext import commands
from mods import firestore, info


@commands.command()
async def whitelist(ctx, command, user):
    if type(user) is str:
        user = ctx.message.mentions[0]
    uid = str(user.id)
    whitelist_ = (await firestore.get_command(uid, command))['whitelist']
    whitelist_.append(user.id)
    await firestore.update_command(uid, command, 'whitelist', whitelist_)


def setup(bot):
    info.Help(
        name='whitelist',
        description='allow another user to use a command',
        usage='`whitelist <command> <user>`'
    )
    bot.add_command(whitelist)
