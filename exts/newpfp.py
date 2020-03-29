import discord
from discord.ext import commands

from mods import firestore, info, vars_
from mods.core import get_cat_link
from mods.core import change_avatar


@commands.command()
async def newpfp(ctx, arg='random'):
    if ctx.author.bot:
        return

    async with ctx.typing():

        uid = str(ctx.author.id)
        user_ = await firestore.get_user(uid)
        attachments = ctx.message.attachments
        embed = discord.Embed(title='Newpfp')
        if attachments and attachments[0].filename.lower().split('.')[-1] in ['png', 'jpg']:
            arg = attachments[0].url
        elif arg in ['last', '^', '_']:
            arg = (await firestore.get_command(uid, 'meow'))['_last']
        elif arg == 'random':
            arg = await get_cat_link()

        if user_['self']:
            # handle self-hosting here
            await firestore.update_command_field(uid, 'newpfp', 'link', arg)
            await firestore.update_command_field(uid, 'newpfp', 'flag', True)
            await firestore.update_user_field(uid, 'flag', True)
            embed.description = "I've told your slave to update your avatar"
            embed.colour = vars_.colour_success
            await ctx.send(embed=embed)
            await firestore.update_command_field(uid, 'newpfp', 'flag', False)
            await firestore.update_user_field(uid, 'flag', False)
            return

        result, success = await _new_avatar(ctx, user_, arg)
        if success:
            embed.colour = vars_.colour_success
        else:
            embed.colour = vars_.colour_error
        embed.description = result
        await ctx.send(embed=embed)


@newpfp.error
async def newpfp_error(ctx, err):
    e = discord.Embed(title="Newpfp", colour=vars_.colour_error, description=err)
    await ctx.send(embed=e)


async def _new_avatar(ctx, user_: dict, arg):
    if arg[-3:] in ['jpg', 'png']:
        img_link = arg
    elif len(ctx.message.attachments) == 1:
        img_link = ctx.message.attachments[0].url
    elif arg == 'random':
        img_link = await get_cat_link()
    else:
        result = 'Are you sure you called the command correctly?'
        return result, False
    # print(img_link)
    return await change_avatar(user_, img_link)


def setup(bot):
    info.Info(
        name='newpfp',
        brief='changes your avatar to a random cat',
        description='use `settings newpfp timer <minutes>` to set a timer',
        usage='`newpfp [last|^|_]`',
        category='Core',
        settings={
            'timer': 'automatically change your pfp every ... (minutes)',
            'enabled': 'none',
        },
        defaults={
            'timer': 0,  # off,
            'enabled': True,
        }
    ).export(vars_.info_)

    bot.add_command(newpfp)
