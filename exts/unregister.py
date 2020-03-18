from discord.ext import commands
from google.api_core.exceptions import NotFound

from mods import firestore


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
            await firestore.update_user(uid, self_=False, new_token=None, new_pwd=None, new_email=None, active=False)
        await ctx.send(st)
    except NotFound:
        await ctx.send('Your account couldn\'t be found.')


def setup(bot):
    bot.add_command(unregister)
