import discord
from discord.ext import commands
from mods import firestore, vars_
from mods.core import change_status
from mods import info


@commands.command()
async def counter(ctx, user=None):
    async def send():
        await ctx.send(embed=embed)

    if not user:
        user = ctx.message.author
    if type(user) is str:
        user = ctx.message.mentions[0]
    uid = str(user.id)
    user_ = await firestore.get_user(uid)
    counter_ = await firestore.get_command(uid, 'counter')
    embed = discord.Embed(title='Counter')
    if not user_:
        embed.description = "The user you mentioned isn't registered"
        embed.colour = vars_.colour_error
        await send()
        return
    elif str(ctx.author.id) not in counter_['whitelist']:
        embed.description = f"You're not allowed to change {user.name}'s counter. " \
                            f"Ask them to add you to the whitelist with `whitelist <mention>`"
        embed.colour = colour = vars_.colour_error
        await send()
        return
    elif not counter_['enabled']:
        embed.description = f"{user.name} currently has this command disabled. " \
                            f"They can re-enable it with `settings counter enable`."
        embed.colour = vars_.colour_error
        await send()
        return
    count_ = int(counter_['c'])
    if '++' in ctx.message.content:
        count_ += 1
    elif '--' in ctx.message.content:
        count_ -= 1
    template = counter_['template']
    await firestore.update_command_field(uid, 'counter', 'c', count_)
    status = template.replace('$COUNTER$', str(count_))
    await firestore.update_command_field(uid, 'counter', 'status', status)
    if not user_['self']:
        resp = await change_status(user_['token'], status)
        if resp.status != 200:
            embed.description = 'Something wonky happened'
            embed.colour = vars_.colour_error
            await send()
            return
        else:
            embed.description = f"I've updated {user.name}'s counter"
            embed.colour = vars_.colour_success
            await send()
            return
    await firestore.update_command_field(uid, 'counter', 'flag', True)
    await firestore.update_user_field(uid, 'flag', True)
    embed.description = "I've instructed their slave to change their status"
    embed.description = vars_.colour_success
    await send()
    await firestore.update_command_field(uid, 'counter', 'flag', False)
    await firestore.update_user_field(uid, 'flag', False)
    return


def setup(bot):
    info.Info(
        name='counter',
        brief='counts things',
        description='allows other people to increase or decrease the counter in your status',
        usage='`counter <user> [+|-]` or `<user> braincells[++|--]`',
        category='Core',
        settings={
            'template': 'any',
            'enabled': None,
            'c': int,
            'status': 'any',
        },
        defaults={
            'template': 'Braincell Counter: $COUNTER$',
            'whitelist': 'self',
            'enabled': True,
            'c': 0,
            'status': 'Braincell Counter: 0',
        }
    ).export(vars_.info_)

    bot.add_command(counter)
