import time
import os
import random

from dotenv import load_dotenv
from keep_alive import keep_alive
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from google.cloud import monitoring_v3
import firebase_admin
from firebase_admin import auth

load_dotenv()
BOT_PREFIX = 'b!'
bot = commands.Bot(command_prefix='b!')

BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = 585948652644859904
USER_ID = 179701226995318785
ROLE_ID = 681628171778785281

stop_timer = False


# TODO write server code to receive register requests
# TODO server code to write to database
# TODO migrate to cogs


@commands.command()
@commands.cooldown(1, 3, BucketType.member)
async def alive(ctx):
    resp = ['Living the dream!', 'Alive and kicking!', 'Yes, but dead inside :(', 'We\'re all gonna die anyway']
    await ctx.send(resp[random.randint(0, len(resp) - 1)])


@alive.error
async def alive_error(ctx):
    await ctx.send('This command is on cooldown, but I guess I must be alive!')


bot.add_command(alive)

# set and load all extensions
extensions = ['cogs.UptimeCheck',
              'cogs.Core']
if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


last_braincell = time.mktime(time.gmtime(0))
last_meow = time.mktime(time.gmtime(0))
just_tried = False


@bot.event
async def on_message(message):
    global last_braincell
    global last_meow
    global just_tried
    server = bot.get_guild(GUILD_ID)
    spes = server.get_member(USER_ID)
    if message.channel == server.get_channel(681628374158147692):
        if server.get_role(681628171778785281) in message.author.roles:  # if author has the role
            if 'braincells--' in message.content.lower() or 'braincells++' in message.content.lower():
                if (time.time() - last_braincell) < 600 and message.author != spes:
                    await message.channel.send('Give his braincells a break! Wait '
                                               f'{600 - int(time.time() - last_braincell)} '
                                               'seconds')
                elif len(message.mentions) != 1 or message.mentions[0].id != USER_ID:
                    await message.channel.send('Invalid mentions!')
                else:
                    with open('braincell_count', 'r') as f:
                        count = int(f.read())
                    print(f'Current Braincell Count: {count}')
                    async with message.channel.typing():
                        if 'braincells++' in message.content.lower():
                            count = count + 1
                        elif 'braincells--' in message.content.lower():
                            count = count - 1
                        await change_status(f"Braincell Counter: {count}")
                        last_braincell = time.time()
                    with open('braincell_count', 'w') as f:
                        f.write(str(count))
                    await message.channel.send('Braincell Counter successfully updated.')
    await bot.process_commands(message)


keep_alive()
bot.run(BOT_TOKEN)
