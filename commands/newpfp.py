from discord.ext import commands
from Core import get_cat_link
from Core import change_avatar


@commands.command()
async def newpfp(ctx, arg='random'):
    async with ctx.typing():
        result = await _new_avatar(ctx, arg)
        await ctx.send(result)


@newpfp.error
async def newpfp_error(ctx, err):
    await ctx.send(err)


async def _new_avatar(ctx, arg):
    if arg[-3:] in ['jpg', 'png']:
        img_link = arg
    elif len(ctx.message.attachments) == 1:
        img_link = ctx.message.attachments[0].url
    elif arg == 'random':
        img_link = await get_cat_link()
    else:
        result = 'Are you sure you called the command correctly?'
        return result
    # print(img_link)
    result = await change_avatar(img_link)
    return result


def setup(bot):
    bot.add_command(newpfp)
