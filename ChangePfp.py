async def change_pfp(img_link):
    import aiohttp
    import os
    import time
    import json
    import base64

    from dotenv import load_dotenv

    file_ext = img_link.split('.')[-1]

    if file_ext != 'png' and file_ext != 'jpg':
        return 'Image type not supported!'

    load_dotenv()

    token = os.getenv('USER_TOKEN')
    print(img_link)
    # {username, email, password, avatar (data:image/png;base64), discriminator: null, new_password: null}

    headers = {
        'authority': 'discordapp.com',
        'authorization': token,
        'accept-language': 'en-US',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/82.0.4069.0 Safari/537.36',
        'content-type': 'application/json',
        'accept': '*/*',
        'origin': 'https://discordapp.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://discordapp.com/channels/@me',
        'cookie': '__cfduid=d4185c519c0c003f171d470e8372045f81582145613; locale=en-GB; '
                  '__cfruid=e6fb6661f362159e16facf1165ed63368e2de94b-1582851317',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwiYnJvd3Nlcl91c2VyX2FnZW50'
                              'IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChL'
                              'SFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzgwLjAuMzk4Ny4xMjIgU2FmYXJpLzUzNy4zNiBFZGcvODAuMC4zNjEu'
                              'NjIiLCJicm93c2VyX3ZlcnNpb24iOiI4MC4wLjM5ODcuMTIyIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIi'
                              'OiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5f'
                              'Y3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjU1MjM2'
                              'LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=='
    }

    async with aiohttp.ClientSession() as session:
        resp = await session.get(img_link)
        img_base64 = base64.b64encode(await resp.read()).decode()
        payload = {
            "username": os.getenv('USER_NAME'),
            "email": os.getenv('USER_EMAIL'),
            "password": os.getenv('USER_PWD'),
            "avatar": f"data:{resp.content_type};base64,{img_base64}",
            "discriminator": None,
            "new_password": None
        }
        time.sleep(2)
        payload = json.dumps(payload, separators=(',', ':'))
        # print(payload)
        response = await session.patch('https://discordapp.com/api/v6/users/@me',
                                       headers=headers,
                                       data=payload)
        # print(response)
        if response.status == 200:
            return 'Avatar successfully updated!'
        else:
            return 'Something funky wonky happened :('
