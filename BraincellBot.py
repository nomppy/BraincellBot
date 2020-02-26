import discord
import os
import time
from dotenv import load_dotenv
from ChangeStatus import change_status

load_dotenv()
client = discord.Client()

TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = 585948652644859904
USER_ID = 179701226995318785
ROLE_ID = 681628171778785281


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


last_change = time.mktime(time.gmtime(0))


@client.event
async def on_message(message):
    global last_change
    server = client.get_guild(GUILD_ID)

    if message.channel == server.get_channel(681628374158147692):
        if server.get_role(681628171778785281) in message.author.roles:  # if author has the role
            if 'braincells--' in message.content.lower() or 'braincells++' in message.content.lower():
                if (time.time() - last_change) < 600:
                    await message.channel.send(f'Give his braincells a break! Wait {600-int(time.time()-last_change)} seconds')
                elif len(message.mentions) != 1 or message.mentions[0].id != USER_ID:
                    await message.channel.send('Invalid mentions!')
                else:
                    spes = server.get_member(USER_ID)
                    with open('braincell_count', 'r') as f:
                        count = int(f.read())
                    print(f'Current Braincell Count: {count}')
                    async with message.channel.typing():
                        if 'braincells++' in message.content.lower():
                            count = count + 1
                        elif 'braincells--' in message.content.lower():
                            count = count - 1
                        change_status(f"Braincell Counter: {count}")
                        last_change = time.time()
                    with open('braincell_count', 'w') as f:
                        f.write(str(count))
                    await message.channel.send('Braincell Counter successfully updated.')


client.run(TOKEN)
