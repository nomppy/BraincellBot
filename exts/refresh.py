from discord.ext import commands
from mods import token
from mods import firestore


@commands.command()
async def refresh(ctx):
    token_ = token.create_custom_token(str(ctx.author.id)).decode('utf-8')
    await ctx.author.send('Here\'s your freshly minted token!'
                          f'```{token_}```')


def setup(bot):
    bot.add_command(refresh)
