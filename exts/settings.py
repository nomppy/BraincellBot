from discord.ext import commands
from mods import firestore


@commands.command()
async def settings(ctx, command=None, field=None, value=None):
    uid = str(ctx.author.id)

    await firestore.update_command(uid, command, field, value)


def setup(bot):
    bot.add_command(settings)
