import discord
from discord.ext import commands

from mods import vars_, firestore, util, core, info


@commands.command()
async def status(ctx, *, st=None):
    embed = discord.Embed(
        title='Status',
        colour=ctx.guild.me.colour,
    ).set_footer(text=vars_.default_footer_text)
    uid = str(ctx.author.id)
    if not st:
        st = ''
        embed.description = 'Cleared'
    await firestore.update_command_field(uid, 'counter', 'status', st)
    user_ = await firestore.get_user(uid)
    if user_['self']:
        await util.flash_flag(uid, 'counter')
        embed.description = 'Updated'
    else:
        resp = await core.change_status(user_['token'], st)
        if resp.status != 200:
            embed.description = 'Update failed'
            embed.colour = vars_.colour_error
        else:
            embed.description = 'Updated'
    await ctx.send(embed=embed)


def setup(bot):
    info.Info(
        name='status',
        brief='sets status to something',
        description='clears status if run with no arguments',
        usage='status [status message]',
        category='Core',
    ).export(vars_.info_)

    bot.add_command(status)
