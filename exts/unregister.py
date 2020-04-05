import discord
from discord.ext import commands
from google.api_core.exceptions import NotFound

from mods import firestore, info, vars_


@commands.command()
async def unregister(ctx, arg=None):
    user = ctx.author
    uid = str(user.id)
    embed = discord.Embed(title='Unregister').set_footer(text=vars_.default_footer_text)
    try:
        if arg in ['-d', 'delete']:
            await firestore.delete_user(uid)
            embed.description = 'I have deleted all records of your account.'
            embed.colour = vars_.colour_success
        else:
            embed.description = 'Your account has been deactivated. '\
                 'I still have all your preferences saved should you like to reactive your account.\n ' \
                 'Run `b!unregister -d` to completely delete your account.\n ' \
                 'To reactivate your account, run `b!register` again.'
            embed.colour = vars_.colour_warning
            await firestore.update_user(uid, self_=False, active=False, prefix='b!')
        await ctx.send(embed=embed)
    except NotFound:
        embed.colour = vars_.colour_error
        embed.description = "Your account couldn't be found"
        await ctx.send(embed=embed)


def setup(bot):
    info.Info(
        name='unregister',
        brief='deactivates your account',
        description='call with no arguments to deactivate, append `-d` to delete all data',
        usage='`unregister [-d|delete]`',
        category='Account'
    ).export(vars_.info_)
    bot.add_command(unregister)
