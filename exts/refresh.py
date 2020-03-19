from discord.ext import commands
from mods import token, info, vars_


@commands.command()
async def refresh(ctx):
    token_ = token.create_custom_token(str(ctx.author.id)).decode('utf-8')
    await ctx.author.send('Here\'s your freshly minted token!'
                          f'```{token_}```')


def setup(bot):
    info.Info(
        name='refresh',
        brief='refreshes your custom token',
        description='if you chose to self-host and your token has expired, run this command to get a new one',
        usage='`refresh`'
    ).export(vars_.info_)

    bot.add_command(refresh)
