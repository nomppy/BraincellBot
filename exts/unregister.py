from discord.ext import commands
from firebase_admin.auth import UserNotFoundError

from mods import firestore
from mods import token


@commands.command()
async def unregister(ctx):
    user = ctx.author
    uid = str(user.id)
    try:
        token.delete_user(uid)
        firestore.update_user(uid, self_=False)
        await ctx.send('Your account has been deactivated.')
    except UserNotFoundError:
        await ctx.send('Your account couldn\'t be found.')


def setup(bot):
    bot.add_command(unregister)
