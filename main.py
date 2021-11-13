import asyncio
import aiohttp
from imdb import get_imdb_ratings

def get_kinopoisk_ratings():
    pass





async def main():
    async with aiohttp.ClientSession() as client:
        imdb_ratings = await get_imdb_ratings(client,
                                              'https://www.imdb.com/user/ur58128213/ratings')
        print(imdb_ratings)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
