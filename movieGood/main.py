import asyncio
import aiohttp
import kinopoisk
import imdb


async def main():
    imdb_movies = await imdb.get_movies('https://www.imdb.com/user/ur58128213/ratings')
    print(imdb_movies)
        #ratings = await kinopoisk.get_movies(client, 'https://www.kinopoisk.ru/user/95268254/votes/')
        #print(ratings)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
