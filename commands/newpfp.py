from discord.ext import commands


@commands.command()
async def newpfp(self, ctx, arg='random'):
    async with ctx.typing():
        result = await new_avatar(ctx, arg)
        await ctx.send(result)

@newpfp.error
async def newpfp_error(self, ctx, err):
    await ctx.send(err)

async def new_avatar(ctx, arg):
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
