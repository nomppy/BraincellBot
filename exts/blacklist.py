from discord.ext import commands
from mods import firestore, info


@commands.command()
async def blacklist(ctx, command, user):
    if type(user) is str:
        user = ctx.message.mentions[0]
    uid = str(user.id)
    whitelist_ = (await firestore.get_command(uid, command))['whitelist']
    whitelist_.remove(user.id)
    await firestore.update_command(uid, command, 'whitelist', whitelist_)


def setup(bot):
    info.Help(
        name='blacklist',
        description='removes a user from the whitelist of a command',
        usage='`blacklist <command> <user>`'
    )
    bot.add_command(blacklist)
