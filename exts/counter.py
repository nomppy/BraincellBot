from discord.ext import commands
from mods import firestore
from mods.core import change_status
from mods import info


@commands.command()
async def counter(ctx, user):
    if type(user) is str:
        user = ctx.message.mentions[0]
    uid = str(user.id)
    user_ = await firestore.get_user(uid)
    counter_ = await firestore.get_command(uid, 'counter')
    if not user_:
        await ctx.send(f'The user you mentioned isn\'t registered.')
        return
    elif str(ctx.author.id) not in counter_['whitelist']:
        await ctx.send(f"You're not allowed to change {user.name}'s counter. "
                       f"Ask them to add you to the whitelist with `whitelist <mention>`")
        return
    elif not counter_['enabled']:
        await ctx.send(f"{user.name} currently has this command disabled. "
                       f"They can re-enable it with `settings counter enable`.")
        return
    count_ = counter_['c']
    if '++' in ctx.message.content:
        count_ += 1
    elif '--' in ctx.message.content:
        count_ -= 1
    template = counter_['template']
    await firestore.update_command(uid, 'counter', 'c', count_)
    status = template.replace('$COUNTER$', str(count_))
    await firestore.update_command(uid, 'counter', 'status', status)
    if not user_['self']:
        resp = await change_status(user_['token'], status)
        if resp.status != 200:
            await ctx.send("Something wonky happened.")
        else:
            await ctx.send(f"I've updated {user.name}'s counter.")
        return
    await ctx.send("I've instructed their slave to change their status.")
    return


def setup(bot):
    info.Info(
        name='counter',
        brief='counts things',
        description='allows other people to increase or decrease the counter in your status',
        usage='`counter <user> [+|-]` or `<user> braincells[++|--]`',
        settings={
            'default': ['none', 'all'],
            'template': str,
            'enabled': bool
        }
    )
    bot.add_command(counter)
