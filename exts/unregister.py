from discord.ext import commands
from google.api_core.exceptions import NotFound

from mods import firestore, info, vars_


@commands.command()
async def unregister(ctx, arg=None):
    user = ctx.author
    uid = str(user.id)
    try:
        if arg in ['-d', 'delete']:
            await firestore.delete_user(uid)
            st = 'I have deleted all records of your account.'
        else:
            st = 'Your account has been deactivated. '\
                 'I still have all your preferences saved should you like to reactive your account.\n ' \
                 'Run `unregister -d` to completely delete your account.'
            await firestore.update_user(uid, self_=False, active=False)
        await ctx.send(st)
    except NotFound:
        await ctx.send('Your account couldn\'t be found.')


def setup(bot):
    info.Info(
        name='unregister',
        brief='deactivates your account',
        description='call with no arguments to deactivate, append `-d` to delete all data',
        usage='`unregister [-d|delete]`',
        category='Account'
    ).export(vars_.info_)
    bot.add_command(unregister)
