from discord.ext import commands
from mods import token


@commands.command()
async def unregister(ctx):
    user = ctx.author
    uid = user.id
    token.delete_user(uid)


def setup(bot):
    bot.add_command(unregister)