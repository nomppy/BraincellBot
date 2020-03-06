async def change_status(message):
    import aiohttp
    import os
    import json
    from dotenv import load_dotenv

    load_dotenv()

    token = os.getenv('USER_TOKEN')
    print(message)
    headers = {
        'authority': 'discordapp.com',
        'authorization': token,
        'accept-language': 'en-US',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/82.0.4069.0 Safari/537.36',
        'content-type': 'application/json',
        'accept': '*/*',
        'origin': 'https://discordapp.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://discordapp.com/channels/@me'
    }
    # status = '{"custom_status":{"text":' + message + '}}}'
    status = {
        "custom_status": {
            "text": message
        }
    }
    status_str = json.dumps(status, separators=(',', ':'))
    # status_str = '{"custom_status":{"text":"' + message + '"}}'
    # print(status_str)
    async with aiohttp.ClientSession() as session:
        response = await session.patch('https://discordapp.com/api/v6/users/@me/settings',
                                       headers=headers,
                                       data=status_str)

    # response = requests.patch('https://discordapp.com/api/v6/users/@me/settings', headers=headers, data=status_str)
