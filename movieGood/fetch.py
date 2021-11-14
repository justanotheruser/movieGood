

async def fetch(client, url):
    print(f'fetching {url}')
    async with client.get(url) as resp:
        #if resp.status != 200:
        #   raise
        return await resp.text()
