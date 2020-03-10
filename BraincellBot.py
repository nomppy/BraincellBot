import os
import time

from discord.ext import commands
from dotenv import load_dotenv

from Core import change_status
from keep_alive import keep_alive

load_dotenv()
BOT_PREFIX = 'b!'
bot = commands.Bot(command_prefix='b!')

BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = 671052553705750580
USER_ID = 179701226995318785
ROLE_ID = 681628171778785281


# TODO write server code to receive register requests
# TODO server code to write to database
# TODO replace messages with embeds


@commands.command()
@commands.is_owner()
async def reload(ctx, module):
    bot.reload_extension(f'commands.{module}')
    await ctx.send(f'Reloaded {module}')


@reload.error
async def reload_error(ctx, err):
    await ctx.send(err)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    # load all commands
    d = './commands/'
    for file in os.listdir(d):
        if file.endswith('.py'):
            bot.load_extension('commands.' + file.split('.')[0])
            print(f"Loaded {file.split('.')[0]}")


last_braincell = time.mktime(time.gmtime(0))
last_meow = time.mktime(time.gmtime(0))
just_tried = False
bot.add_command(reload)


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
