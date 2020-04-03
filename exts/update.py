import os

from discord.ext import commands
from exts import restart


@commands.command()
@commands.is_owner()
async def update(ctx, arg=None):
    if arg in ['-r', 'reset', '--reset']:
        await ctx.send('resetting to origin/master')
        os.system('git reset --hard origin/master')
    await ctx.send('Pulling changes from origin/master...')
    os.system('git pull')
    await restart.restart(ctx)


def setup(bot):
    bot.add_command(update)
