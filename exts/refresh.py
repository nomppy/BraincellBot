from discord.ext import commands
from mods import token, info, vars_, firestore


@commands.command()
async def refresh(ctx):
    uid = str(ctx.author.id)
    token_ = token.refresh_custom_token(uid).decode('utf-8')
    await firestore.update_user_field(uid, 'token', token_)
    await ctx.author.send('Here\'s your freshly minted token!'
                          f'```{token_}```')


def setup(bot):
    info.Info(
        name='refresh',
        brief='refreshes your custom token',
        description='if you chose to self-host and your token has expired, run this command to get a new one',
        usage='`refresh`',
        category='Account',
    ).export(vars_.info_)

    bot.add_command(refresh)
