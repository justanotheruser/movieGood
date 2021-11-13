async def fetch(client, url):
    print(f'fetching {url}')
    async with client.get(url) as resp:
        assert resp.status == 200
        return await resp.text()
