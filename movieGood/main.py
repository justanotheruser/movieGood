import asyncio
import aiohttp
from imdb import get_imdb_ratings
import kinopoisk


async def main():
    async with aiohttp.ClientSession() as client:
        # imdb_ratings = await get_imdb_ratings(client,
        #                                      'https://www.imdb.com/user/ur58128213/ratings')
        # print(imdb_ratings)
        ratings = await kinopoisk.get_movies(client, 'https://www.kinopoisk.ru/user/95268254/votes/')
        print(ratings)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
