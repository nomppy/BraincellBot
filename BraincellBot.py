import inspect
import os
import re
import time

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv

load_dotenv()

from mods import firestore, vars_
from mods import admin

BOT_PREFIX = 'b!'
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(''),
)

mods = vars_.mods
ignore = vars_.ignore
BOT_TOKEN = os.getenv('BOT_TOKEN')


@commands.command()
@commands.is_owner()
async def reload(ctx, modext=None):
    st = discord.Embed(
        title='Reload',
    ).set_thumbnail(url=bot.user.avatar_url).set_footer(text=vars_.default_footer_text)
    if modext in ['-a', 'all', '--all']:
        st.description = await admin.reload_all(bot, mods, ignore)
        st.colour = vars_.colour_success
    elif modext in ['-c', 'complete', '--complete']:
        # Reloads twice to ensure all dependencies are reloaded
        st.description = await admin.reload_all(bot, mods, ignore)
        await admin.reload_all(bot, mods, ignore)
        st.colour = vars_.colour_success
    elif not modext:
        st.description = "Here's a list of reloadable modules/extensions"
        _ = ', '.join([str(mod) for mod in vars_.mods if str(mod) != '_'])
        [
            st.add_field(
                name=cat,
                value=', '.join([
                    f'`{str(set_)}`'
                    for set_ in vars_.info_[cat].keys()
                ]),
                inline=False)
            for cat in vars_.info_.keys()
        ]
        st.add_field(
            name='Modules',
            value=', '.join(
                [
                    f'`{str(mod)}`'
                    for mod in list(vars_.mods.keys())[1:]
                ]
            ),
            inline=False)
        st.colour = ctx.guild.me.colour
    else:
        try:
            mods[modext], st.description = await admin.reload_load(modext, mods=mods)
            st.colour = vars_.colour_success
        except ModuleNotFoundError:
            try:
                st.description = await admin.reload_load(modext, bot=bot)
                st.colour = vars_.colour_success
            except commands.ExtensionNotFound:
                st.description = f'Cannot find {modext}'
                st.colour = vars_.colour_error

    await ctx.send(embed=st)


bot.add_command(reload)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await admin.reload_all(bot, mods, ignore)
    await bot.get_user(int(os.getenv('OWNER'))).send("I'm online!")


last_braincell = time.mktime(time.gmtime(0))
last_meow = time.mktime(time.gmtime(0))
just_tried = False


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    user = message.author
    uid = str(user.id)
    user_ = await firestore.get_user(uid)

    # TODO change regex to match the template in database
    if re.match(r"^<@!?[0-9]+> braincells[+\-]{2}", message.content):
        mentioned = message.mentions[0]
        await bot.get_command('counter')(await bot.get_context(message), mentioned.mention)
        return

    if re.match(rf"^<@!?{bot.user.id}>$", message.content):
        if user_:
            await message.channel.send(f'Hello {message.author.mention} your prefix is '
                                       f"**{user_['prefix']}**")
            return
        await message.channel.send("You're not registered. \U0001F641 Run `b!register` to register.")
        return

    if message.content[:2] == 'b!' and message.content.split(' ')[0][2:] in vars_.unregistered.keys():
        c = bot.get_command(message.content[2:])
        ctx = await bot.get_context(message)
        if vars_.unregistered[c.name] and 'arg' in vars_.unregistered[c.name]:
            u = message.content.split(' ')[1] if len(message.content.split(' ')) > 1 else None
            await c(ctx, u)
            return
        await c(ctx)
        return
    if not user_ and message.content.startswith('b!'):
        await message.channel.send("You're not registered. \U0001F641 Run `b!register` to register.")
        return
    if user_:  # if user not in database or account inactive
        if not user_['active'] and message.guild is not None:
            await message.channel.send("Your account is deactivated. Activate it by running `b!register`.")
            return
        else:
            prefix = user_['prefix']
            if message.content.startswith(prefix):
                message.content = message.content[len(prefix):]
                try:
                    await bot.process_commands(message)
                except CommandNotFound:
                    await message.channel.send("That command doesn't exist.")
                    return


bot.run(BOT_TOKEN)
