async def fetch(client, url):
    print(f'fetching {url}')
    async with client.get(url) as resp:
        return await resp.text()
