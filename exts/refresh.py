from discord.ext import commands
from mods import token


@commands.command()
async def refresh(ctx):
    try:

    ctx.send('Are you sure you want to refresh your custom token?\n'
             'You will have to replace the token in your .env file.')
    token_ = token.create_custom_token(ctx.author.id)