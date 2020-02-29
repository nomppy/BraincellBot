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
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwiYnJvd3Nlcl91c2VyX2FnZW50'
                              'IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChL'
                              'SFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzgyLjAuNDA2OS4wIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNp'
                              'b24iOiI4Mi4wLjQwNjkuMCIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFp'
                              'biI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNl'
                              'X2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo1NTA0MSwiY2xpZW50X2V2ZW50X3NvdXJj'
                              'ZSI6bnVsbH0=',
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
        'referer': 'https://discordapp.com/channels/@me',
        'cookie': '__cfduid=d198f079f20644b40f6af9f0e74a1212b1582682742; locale=en-US; '
                  '__cfruid=31d0a638dfd4c53d085bd13bac0fa9b82057044a-1582682742 '
    }
    # status = '{"custom_status":{"text":' + message + '}}}'
    status = {
        "custom_status": {
            "text": message
        }
    }
    status_str = json.dumps(status, separators=(',', ':'))
    # status_str = '{"custom_status":{"text":"' + message + '"}}'
    print(status_str)
    async with aiohttp.ClientSession() as session:
        response = await session.patch('https://discordapp.com/api/v6/users/@me/settings',
                                       headers=headers,
                                       data=status_str)

    # response = requests.patch('https://discordapp.com/api/v6/users/@me/settings', headers=headers, data=status_str)
