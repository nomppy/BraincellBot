from discord.ext import commands
from mods import firestore
from mods import token


@commands.command()
async def revoke(ctx):
    if ctx.author.bot:
        return

    user = ctx.author
    uid = str(user.id)
    try:
        self_ = firestore.get_user(uid)['self']
        if self_:
            token.revoke_refresh_tokens(uid)
            await ctx.send('I have revoked your access token, it will become invalid within an hour.')
            # TODO embed Learn More to firebase tokens page
        else:
            ctx.send('You\'re not registered to self-host. If you want to switch to self-hosting do `register`')
    except TypeError:
        await ctx.send('You\'re not registered at all! Use `register` to begin the process')
