import discord
import os
import time
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
client = discord.Client()
bot = commands.Bot(command_prefix='b!')

def change_braincell_count(count: int):
    import requests
    import time
    headers = {
        'authority': 'discordapp.com',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzgyLjAuNDA2OS4wIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiI4Mi4wLjQwNjkuMCIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo1NTA0MSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
        'authorization': os.getenv('USER_TOKEN'),
        'accept-language': 'en-US',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4069.0 Safari/537.36',
        'content-type': 'application/json',
        'accept': '*/*',
        'origin': 'https://discordapp.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://discordapp.com/channels/@me',
        'cookie': '__cfduid=d198f079f20644b40f6af9f0e74a1212b1582682742; locale=en-US; __cfruid=31d0a638dfd4c53d085bd13bac0fa9b82057044a-1582682742',
    }

    status = '{"custom_status":{"text":"Status Changed Yet Again"}}'
    response = requests.patch('https://discordapp.com/api/v6/users/@me/settings', headers=headers, data=status);


@commands.command()
async def status(ctx):
    print('hello')
    await ctx.send(f"Current Braincell Count: {open('braincell_count','r').read()}")

bot.add_command(status)

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
                        os.system(f'py ChangeBraincellCount.py {count}')
                        last_change = time.time()
                    with open('braincell_count', 'w') as f:
                        f.write(str(count))
                    await message.channel.send('Braincell Counter successfully updated.')


client.run(TOKEN)
