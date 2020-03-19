from discord.ext import commands

from mods import firestore, info


@commands.command(aliases=['prefix'])
async def setprefix(ctx, prefix):
    if ctx.author.bot:
        return

    if prefix == '':
        await ctx.send('Plz don\'t make the prefix nothing')
        return
    await firestore.update_field(str(ctx.author.id), 'prefix', prefix)
    # bot_.command_prefix = prefix
    await ctx.send(f'Your prefix has been changed to `{prefix}`')


def setup(bot):
    info.Info(
        name='setprefix',
        brief='change your prefix',
        usage='`[set]prefix <new_prefix>`'
    )

    bot.add_command(setprefix)
