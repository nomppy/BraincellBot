import os
import re
import time

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

from mods import firestore
from mods import admin
from mods.core import change_status
from keep_alive import keep_alive
from exts import register

BOT_PREFIX = 'b!'
bot = commands.Bot(command_prefix=commands.when_mentioned_or(''))

BOT_TOKEN = os.getenv('TEST_BOT_TOKEN')
GUILD_ID = 671052553705750580
USER_ID = 179701226995318785
ROLE_ID = 681628171778785281


# TODO write server code to receive register requests
# TODO server code to write to database
# TODO replace messages with embeds


@commands.command()
@commands.is_owner()
async def reload(ctx, modext=None):
    if modext in ['-a', 'all', '--all']:
        st = await admin.reload_all(bot, mods, ignore)
    elif not modext:
        st = 'TODO: send list of modules/extensions here'
    else:
        try:
            mods[modext], st = await admin.reload_load(modext, mods=mods)
        except ModuleNotFoundError:
            try:
                st = await admin.reload_load(modext, bot=bot)
            except commands.ExtensionNotFound:
                st = f'Cannot find {modext}'

    await ctx.send(st)


bot.add_command(reload)
mods = {'_': '_'}
ignore = ['_', 'uptimecheck.py']  # ignore on loading phase; for debugging purposes


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await admin.reload_all(bot, mods, ignore)


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

    if re.match(r"^<@!?[0-9]+> braincells[+\-]{2}$", message.content):
        mentioned = message.mentions[0]
        uid = str(mentioned.id)
        mentioned_ = await firestore.get_user(uid)
        counter_ = await firestore.get_command(uid, 'counter')
        if not mentioned_:
            await message.channel.send(f'The user you mentioned isn\'t registered.')
            return
        elif message.author.id not in counter_['whitelist']:
            await message.channel.send(f"You're not allowed to change {mentioned.name}'s counter. "
                                       f"Ask them to add you to the whitelist with `whitelist <mention>`")
        elif not counter_['enabled']:
            await message.channel.send(f"{mentioned.name} currently has this command disabled. "
                                       f"They can re-enable it with `settings counter enable`.")
        count_ = counter_['c']
        if 'braincells++' in message.content:
            count_ += 1
        else:
            count_ -= 1
        template = counter_['template']
        await firestore.update_command(uid, 'counter', 'c', count_)
        status = template.replace('$COUNTER$', count_)
        await firestore.update_command(uid, 'counter', 'status', status)
        if not mentioned_['self']:
            await change_status(mentioned_['token'], status)

        return

    if re.match(rf"^<@!?{bot.user.id}>$", message.content):
        if user_:
            await message.channel.send(f'Hewwo {message.author.mention} your prefix is '
                                       f"**{user_['prefix']}**")
            return
        await message.channel.send("You're not registered. \U0001F641 Run `b!register` to register.")
        return

    if message.content == 'b!register':
        await bot.get_command('register')(await bot.get_context(message))
        return
    if not user_ and message.content.startswith('b!'):
        await message.channel.send("You're not registered. \U0001F641 Run `b!register` to register.")
        return
    if user_:  # if user not in database or account inactive
        if not user_['active'] and message.guild is not None:
            await message.channel.send("Your account is deactivated. Activate it by running `register`.")
            return
        else:
            prefix = user_['prefix']
            if message.content.startswith(prefix):
                message.content = message.content[len(prefix):]
                await bot.process_commands(message)


keep_alive()
bot.run(BOT_TOKEN)
